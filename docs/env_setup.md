# DroneEnv

## Prerequisites
setup a ubuntu-22.04 using
- [WSL2](https://documentation.ubuntu.com/wsl/latest/howto/install-ubuntu-wsl2/)
- [VirtualBox](https://ubuntu.com/tutorials/how-to-run-ubuntu-desktop-on-a-virtual-machine-using-virtualbox)

## Install ROS 2 Humble
``` bash
sudo apt update && sudo apt upgrade -y

locale  # check for UTF-8

sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

locale  # verify settings

sudo apt install software-properties-common
sudo add-apt-repository universe

sudo apt update && sudo apt install curl -y
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb

sudo apt update && sudo apt upgrade -y

sudo apt install -y build-essential cmake git wget curl python3-pip python3-venv python3-colcon-common-extensions python3-rosdep python3-vcstool lsb-release gnupg software-properties-common 
  
sudo apt install -y ros-humble-desktop
sudo apt install ros-humble-mavros ros-humble-mavros-extras -y
```

### Source ROS:
``` bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### Init rosdep:
``` bash
sudo rosdep init
rosdep update
```

## Install ArduPilot SITL
``` bash
cd ~
git clone --recurse-submodules https://github.com/ArduPilot/ardupilot.git
cd ardupilot


Tools/environment_install/install-prereqs-ubuntu.sh -y
. ~/.profile
```

### Build SITL:
``` bash
cd ~/ardupilot
./waf configure --board sitl
./waf copter
```

### Install MAVSDK (Python)
``` bash
pip install mavsdk
```

## Run ArduPilot SITL
``` bash
sim_vehicle.py -v ArduCopter --frame hexa --console --map --out=udp:127.0.0.1:14540
```

### Test SITL
``` python
# ~/test_mavsdk.py

import asyncio
from mavsdk import System

async def run():
    drone = System()
    await drone.connect(system_address="udpin://0.0.0.0:14540")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone connected!")
            break

asyncio.run(run())
```
#### Run
``` bash
python3 ~/test_mavsdk.py
```
It should give
``` bash
Drone connected!
```

## QGroundControl Setup
Run QGroundControl on Windows, if on wsl
Download: [QGC](https://qgroundcontrol.com/)

