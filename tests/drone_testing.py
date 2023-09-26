#!/usr/bin/python2
import pytest
import math
import rospy
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import TwistStamped, PoseStamped
from mavros_msgs.srv import CommandBool, SetMode, ParamSet, ParamGet
from mavros_msgs.msg import State, ParamValue



class TestDrone:
    @classmethod
    def setup_class(cls):
        # Initialize ROS node
        rospy.init_node('pytest_drone')


    def setup_method(self):
        # Publisher for sending drone movement commands
        self.pub_cmd_vel = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel', TwistStamped, queue_size=1)

        # Subscriber for receiving drone state updates
        self.sub_state = rospy.Subscriber('/mavros/state', State, self.state_callback)

        # Subscriber for receiving drone position updates
        self.sub_local_pose = rospy.Subscriber('/mavros/local_position/pose', PoseStamped, self.local_pose_callback)

        # Service for px4 param setting
        rospy.wait_for_service('/mavros/param/set')
        self.srv_set_px4_param = rospy.ServiceProxy('/mavros/param/set', ParamSet)

        rospy.wait_for_service('/mavros/param/get')
        self.srv_get_px4_param = rospy.ServiceProxy('/mavros/param/get', ParamGet)

        # Service for arming the drone
        rospy.wait_for_service('/mavros/cmd/arming')
        self.srv_arming = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)

        # Service for setting the flight mode
        rospy.wait_for_service('/mavros/set_mode')
        self.srv_set_mode = rospy.ServiceProxy('/mavros/set_mode', SetMode)

        rospy.sleep(1)

    def state_callback(self, state):
        self.current_state = state

    def local_pose_callback(self, pose):
        self.current_pose = pose  
        quaternion_matrix = [
            self.current_pose.pose.orientation.x,
            self.current_pose.pose.orientation.y,
            self.current_pose.pose.orientation.z,
            self.current_pose.pose.orientation.w
        ]
        (roll, pitch, yaw) = euler_from_quaternion(quaternion_matrix)
        self.current_yaw = yaw

    def set_flight_mode(self, mode):
        # Set the flight mode of the drone
        self.srv_set_mode(0, mode)

    def send_twist_command(self, linear_x, linear_y, linear_z, angular_z, duration=0):
        twist = TwistStamped()
        twist.twist.linear.x = linear_x
        twist.twist.linear.y = linear_y
        twist.twist.linear.z = linear_z
        twist.twist.angular.z = angular_z

        self.pub_cmd_vel.publish(twist)

        rospy.sleep(duration)

        # Stop the drone when the duration is reached
        if duration != 0:
            twist.twist.linear.x = 0
            twist.twist.linear.y = 0
            twist.twist.linear.z = 0
            twist.twist.angular.z = 0
            self.pub_cmd_vel.publish(twist)

    def test_px4_param_ignore_rc_loss(self):
        '''
        Due to there is no RC signal in simulation's, and process autonomous mode (OFFBOARD) without 
        RC control is serious fatal when UAV lost control.
        So, if you're test autonomous mode (OFFBOARD) in real world, always remember to enable your RC in whole procedure.
        But we need to ignore this safety check in simulation for the sake of efficiency, so here is the px4 param that
        let you to process autonomous mode (OFFBOARD) without RC input. 

        *** DO NOT RUN THIS COMMAND IN REAL WORLD, THAT WILL BE A FATAL OPERATION ***
        '''
        # Set COM_RCL_EXCEPT to 4 in order to ignore RC input during OFFBOARD mode
        msg = ParamValue()
        msg.integer = 4
        msg.real = 0.0
        self.srv_set_px4_param("COM_RCL_EXCEPT", msg)
        rospy.sleep(1)
        assert self.srv_get_px4_param("COM_RCL_EXCEPT").value.integer == 4

    def test_px4_param_offboard_loss_duration(self):
        # Set COM_OBL_ACT to -1 in order to disable the related mode swith when the cmd_vel is discontious during OFFBOARD mode
        msg = ParamValue()
        msg.integer = -1
        msg.real = 0.0
        self.srv_set_px4_param("COM_OBL_ACT", msg)
        rospy.sleep(1)
        assert self.srv_get_px4_param("COM_OBL_ACT").value.integer == -1


    def test_offboard(self):
        # Tet the offboard mode of the drone
        while self.current_state.mode != "OFFBOARD":
            # 
            self.srv_set_mode(0, "OFFBOARD")
            self.send_twist_command(0, 0, 0, 0)

        assert self.current_state.mode == "OFFBOARD"

    def test_arming(self):
        # Test arming service
        while self.srv_arming(True).success == False:
            pass
        rospy.sleep(1)
        assert self.current_state.armed == True

    
    def test_linear_z_upward(self):
        # Test the drone ability to fly upward

        self.srv_set_mode(0, "OFFBOARD")

        while self.srv_arming(True).success == False:
            pass
        rospy.sleep(1)

        init_z = self.current_pose.pose.position.z

        while init_z + 7 > self.current_pose.pose.position.z:
            self.send_twist_command(0, 0, 1, 0)
        
        end_z = self.current_pose.pose.position.z
        
        self.send_twist_command(0, 0, 0, 0)
        
        assert abs(end_z - init_z - 7) < 0.5


    def test_linear_z_downward(self):
        # Test the drone ability to fly downward

        init_z = self.current_pose.pose.position.z

        while init_z - 2 < self.current_pose.pose.position.z:
            self.send_twist_command(0, 0, -1, 0)

        end_z = self.current_pose.pose.position.z

        self.send_twist_command(0, 0, 0, 0)
        
        assert abs(init_z - end_z - 2) < 0.5


    def test_linear_x_forward(self):
        # Test the drone ability to fly forward

        init_x = self.current_pose.pose.position.x
        init_y = self.current_pose.pose.position.y

        while math.sqrt(pow(init_x - self.current_pose.pose.position.x, 2) + pow(init_y - self.current_pose.pose.position.y, 2)) < 2:
            self.send_twist_command(1, 0, 0, 0)

        
        end_x = self.current_pose.pose.position.x

        self.send_twist_command(0, 0, 0, 0)
        
        assert abs(math.sqrt(pow(init_x - self.current_pose.pose.position.x, 2) + pow(init_y - self.current_pose.pose.position.y, 2)) - 2) < 0.5


    def test_linear_x_backward(self):
        # Test the drone ability to fly backward

        init_x = self.current_pose.pose.position.x
        init_y = self.current_pose.pose.position.y

        while math.sqrt(pow(init_x - self.current_pose.pose.position.x, 2) + pow(init_y - self.current_pose.pose.position.y, 2)) < 2:
            self.send_twist_command(-1, 0, 0, 0)

        end_x = self.current_pose.pose.position.x

        self.send_twist_command(0, 0, 0, 0)
        
        assert abs(math.sqrt(pow(init_x - self.current_pose.pose.position.x, 2) + pow(init_y - self.current_pose.pose.position.y, 2)) - 2) < 0.5


    def test_linear_y_leftward(self):
        # Test the drone ability to fly leftward

        init_x = self.current_pose.pose.position.x
        init_y = self.current_pose.pose.position.y

        while math.sqrt(pow(init_x - self.current_pose.pose.position.x, 2) + pow(init_y - self.current_pose.pose.position.y, 2)) < 2:
            self.send_twist_command(0, 1, 0, 0)

        end_x = self.current_pose.pose.position.x

        self.send_twist_command(0, 0, 0, 0)
        
        assert abs(math.sqrt(pow(init_x - self.current_pose.pose.position.x, 2) + pow(init_y - self.current_pose.pose.position.y, 2)) - 2) < 0.5


    def test_linear_y_rightward(self):
        # Test the drone ability to fly rightward

        init_x = self.current_pose.pose.position.x
        init_y = self.current_pose.pose.position.y

        while math.sqrt(pow(init_x - self.current_pose.pose.position.x, 2) + pow(init_y - self.current_pose.pose.position.y, 2)) < 2:
            self.send_twist_command(0, -1, 0, 0)

        end_x = self.current_pose.pose.position.x

        self.send_twist_command(0, 0, 0, 0)
        
        assert abs(math.sqrt(pow(init_x - self.current_pose.pose.position.x, 2) + pow(init_y - self.current_pose.pose.position.y, 2)) - 2) < 0.5


    def test_angular_z_rotation(self):
        # Tet the drone ability to rotate

        init_yaw = self.current_yaw 

        self.send_twist_command(0, 0, 0, 1, duration=2)

        end_yaw = self.current_yaw 

        assert abs(init_yaw - end_yaw) > 0.2


    def test_landing(self):
        # Tet the land mode of the drone
        while self.current_state.mode != "AUTO.LAND":
            self.srv_set_mode(0, "AUTO.LAND")

        assert self.current_state.mode == "AUTO.LAND"

# Run the tests with pytest
if __name__ == '__main__':
    pytest.main(['-s', '-v', __file__])
