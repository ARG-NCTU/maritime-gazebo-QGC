# How to Deploy `USV-Service`

This deployment guide will help you set up and deploy the `USV-Service`. This process involves setting up Docker containers and launching the deployment service.

## Step 1: Docker Deployment
To deploy the `USV-Service` Docker container, use the following command:

```bash
source docker_deploy_run.sh
```

This will pull and run the argnctu/usv-service:ipc-deploy Docker image.

## Step 2: Running the Launch File

To run the launch file for example (or you can run your own launch file):

```bash
roslaunch usv_utils joy_to_sim_real_bin.launch
```

You can deactivate real or simulated messages by specifying arguments: joy2real and joy2sim (True or False, default = True)\
ex.

```bash
roslaunch usv_utils joy_to_sim_real_bin.launch joy2real:=False joy2sim:=False
```