cmake_minimum_required(VERSION 3.8)
project(cmeresearch_environments)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
find_package(rosidl_default_generators REQUIRED)

if(BUILD_TESTING)
    find_package(ament_lint_auto REQUIRED)
    # the following line skips the linter which checks for copyrights
    # comment the line when a copyright and license is added to all source files
    set(ament_cmake_copyright_FOUND TRUE)
    # the following line skips cpplint (only works in a git repo)
    # comment the line when this package is in a git repo and when
    # a copyright and license is added to all source files
    set(ament_cmake_cpplint_FOUND TRUE)
    ament_lint_auto_find_test_dependencies()
endif()

## Mark other files for installation (e.g. launch and bag files, etc.)
install(FILES
  envs/house/map.pgm
  envs/house/map.png
  envs/house/map.yaml
  envs/house/map.posegraph
  envs/house/map.data
  DESTINATION share/${PROJECT_NAME}/envs/house/
)

install(FILES
  envs/laboriii/map.pgm
  envs/laboriii/map.png
  envs/laboriii/map.yaml
  envs/laboriii/map.posegraph
  envs/laboriii/map.data
  DESTINATION share/${PROJECT_NAME}/envs/laboriii/
)

ament_package()