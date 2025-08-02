# CME Research Environments

This package contains environment maps for robot navigation and simulation in ROS2.

## Overview

The `cmeresearch_environments` package provides map data for various environments used in robotics research and development at CME Robotics. These maps can be used for navigation, localization, and simulation purposes.


# ROS Distro Support #


|         |                                            melodic                                            |      noetic      |                  rolling                  |
|:-------:|:---------------------------------------------------------------------------------------------:|:----------------:|:-----------------------------------------:|
| Branch  | [`melodic_dev`](https://bitbucket.org/cme-robotics/cmeresearch_environments/src/melodic_dev/) |                  |   [`rolling_dev`] |
| Status  |                                           supported                                           |  not supported   |  supported |
| Version |                                        no yet released                                        | not yet released |    not yet released |




## Available Environments

### House Environment
A simulated house environment with rooms and corridors.
- Map files: PGM, PNG, YAML, and posegraph data

### Labor III Environment
A laboratory environment for testing and development.
- Map files: PGM, PNG, and YAML

## Installation

```bash
# Clone the repository into your ROS2 workspace
cd ~/ros2_ws/src
git clone https://github.com/cmerobotics/cmeresearch_environments.git

# Build the package
cd ~/ros2_ws
colcon build --packages-select cmeresearch_environments
```

## Usage

To use these maps with the ROS navigation stack. Posegraph and map.data is created with Slam Toolbox https://github.com/SteveMacenski/slam_toolbox .

## License

This package is licensed under the GNU General Public License v3.0 (GPLv3).


## Contact

For more information, please contact:
- Email: info@cme-robotics.com
- Website: https://cme-robotics.com