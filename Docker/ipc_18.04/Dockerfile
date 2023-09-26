FROM nvidia/cuda:11.0.3-cudnn8-devel-ubuntu18.04

ENV DEBIAN_FRONTEND noninteractive
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV ROS_DISTRO melodic
ARG GAZ=gazebo9
###################################### user #####################################

ENV SHELL=/bin/bash \
    NB_USER=arg \
    NB_UID=1000 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER} 

RUN echo "root:root" | chpasswd
RUN echo "${NB_USER}:111111" | chpasswd

ENV HOME=/home/${NB_USER}

##################################### basic tools #####################################
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF


RUN apt-get -o Acquire::ForceIPv4=true update && apt-get -yq dist-upgrade \
    && apt-get -o Acquire::ForceIPv4=true install -yq --no-install-recommends \
    vim \
    wget \
    sudo \
    cmake \
    gedit \
    gnupg2 \
    gtk+-3.0 \
    locales \
    dirmngr \
    mercurial \
    net-tools \
    lsb-release \
    openssh-client \
    build-essential \
    libcanberra-gtk-module \
    libcanberra-gtk3-module \
    libpcap-dev \
    libusb-1.0 \
    tzdata \
    libglfw3-dev \
    libmetis-dev \
    python-gtk2 \
    python-gobject \
    python-tk \
    software-properties-common \
    ruby \
    python3-pip \
    python3-setuptools \
    python3-numpy \
    python3-empy  \
    python3-opencv \
    python3-dbg \
    python3-venv \
    python3-dev \
    python3-tk \
    python3-yaml \
    libfltk1.3-dev \ 
    freeglut3-dev \ 
    libpng-dev \ 
    libjpeg-dev \
    libxft-dev \ 
    libxinerama-dev \ 
    libtiff5-dev \ 
    netbase \ 
    fluid \
    xterm \
    scrot \
    qtbase5-dev \
    && apt-get update && apt-get install -y git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Fixing TimeZone problem reported in VRX 2019
RUN export DEBIAN_FRONTEND=noninteractive \
 && apt update \
 && apt install -y \
    tzdata \
 && ln -fs /usr/share/zoneinfo/America/Los_Angeles /etc/localtime \
 && dpkg-reconfigure --frontend noninteractive tzdata \
 && apt clean


###################################### ROS #####################################

# setup sources.list
RUN echo "deb http://packages.ros.org/ros/ubuntu `lsb_release -sc` main" > /etc/apt/sources.list.d/ros-latest.list \
    && echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list

# setup keys
RUN apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654 
RUN wget http://packages.osrfoundation.org/gazebo.key -O - | apt-key add -


# install bootstrap tools
RUN apt-get -o Acquire::ForceIPv4=true update && apt-get -o Acquire::ForceIPv4=true install --no-install-recommends -y \
    ${GAZ} \
    lib${GAZ}-dev \
    ros-$ROS_DISTRO-desktop-full \
    ros-$ROS_DISTRO-rosbridge-suite \
    ros-$ROS_DISTRO-mavros \
    ros-$ROS_DISTRO-mavros-extras \
    ros-$ROS_DISTRO-octomap-* \
    ros-$ROS_DISTRO-gazebo-plugins \
    ros-$ROS_DISTRO-gazebo-ros \
    ros-$ROS_DISTRO-gazebo-ros-control \
    ros-$ROS_DISTRO-gazebo-ros-pkgs \
    ros-$ROS_DISTRO-effort-controllers \
    ros-$ROS_DISTRO-geographic-info \
    ros-$ROS_DISTRO-hector-gazebo-plugins \
    ros-$ROS_DISTRO-joint-state-controller \
    ros-$ROS_DISTRO-joint-state-publisher \
    ros-$ROS_DISTRO-joy \
    ros-$ROS_DISTRO-joy-teleop \
    ros-$ROS_DISTRO-kdl-parser-py \
    ros-$ROS_DISTRO-key-teleop \
    ros-$ROS_DISTRO-move-base \
    ros-$ROS_DISTRO-robot-localization \
    ros-$ROS_DISTRO-robot-state-publisher \
    ros-$ROS_DISTRO-rqt \
    ros-$ROS_DISTRO-rqt-common-plugins \
    ros-$ROS_DISTRO-rqt-robot-plugins \
    ros-$ROS_DISTRO-teleop-tools \
    ros-$ROS_DISTRO-teleop-twist-joy \
    ros-$ROS_DISTRO-teleop-twist-keyboard \
    ros-$ROS_DISTRO-tf2-geometry-msgs \
    ros-$ROS_DISTRO-tf2-tools \
    ros-$ROS_DISTRO-urdfdom-py \
    ros-$ROS_DISTRO-velodyne-gazebo-plugins \
    ros-$ROS_DISTRO-xacro \
    ros-$ROS_DISTRO-pointcloud-to-laserscan \
    ros-$ROS_DISTRO-spacenav-node \
    ros-$ROS_DISTRO-tf2-sensor-msgs \
    ros-$ROS_DISTRO-twist-mux \
    ros-$ROS_DISTRO-velodyne-simulator \
    ros-$ROS_DISTRO-soem \
    ros-$ROS_DISTRO-openslam-gmapping \
    ros-$ROS_DISTRO-geodesy \
    ros-$ROS_DISTRO-ddynamic-reconfigure \
    ros-$ROS_DISTRO-rviz-imu-plugin \
    python-catkin-tools \
    python-rosdep \
    python-rosinstall \
    python-rosinstall-generator \
    python-wstool \
    python-vcstool \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

##################################### PIP2 ######################################
RUN wget https://bootstrap.pypa.io/pip/2.7/get-pip.py \
    && python2 get-pip.py

RUN pip2 install --upgrade pip setuptools

RUN pip2 install \
    scipy 

RUN rosdep init \ 
    && rosdep update


##################################### PIP ######################################
RUN pip3 -V 

RUN pip3 install --upgrade pip setuptools

RUN pip3 install \
    gym \
    matplotlib \
    pandas \
    pypozyx \
    requests \
    jupyter \
    jupyter_http_over_ws \
    rospkg \
    catkin-tools \
    scikit-image \
    scikit-learn \
    zerorpc \
    gdown \
    seaborn \
    pybind11-global \
    pyautogui


######################################## Gazebo env & PX4 ########################################
RUN apt-get -o Acquire::ForceIPv4=true update && apt-get -o Acquire::ForceIPv4=true install --no-install-recommends -y \
    ros-$ROS_DISTRO-mavros \
    ros-$ROS_DISTRO-mavros-extras \
    libpcl1 \
    ros-$ROS_DISTRO-octomap-* \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-ugly \
    libgstreamer-plugins-base1.0-dev \
    geographiclib-tools \
    libgeographic-dev \
    libpcl1 \
    ros-$ROS_DISTRO-octomap-* \
    ros-$ROS_DISTRO-stereo-image-proc \
    ros-$ROS_DISTRO-image-view

RUN wget https://raw.githubusercontent.com/mavlink/mavros/master/mavros/scripts/install_geographiclib_datasets.sh
RUN chmod +x install_geographiclib_datasets.sh
RUN sudo ./install_geographiclib_datasets.sh
RUN pip3 install --user toml

##################################### Settings #####################################

RUN echo "root ALL=(ALL)  ALL" >> /etc/sudoers \
    && echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ${HOME}/.bashrc 


# Support of nvidia-docker 2.0
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=all