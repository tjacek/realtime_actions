cmake_minimum_required(VERSION 2.8 FATAL_ERROR)

project(remove_planes)

find_package(PCL 1.2 REQUIRED)
find_package( OpenCV REQUIRED )

include_directories(${PCL_INCLUDE_DIRS})
link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})

add_executable (remove_planes remove_planes.cpp pc_tools.cpp)
target_link_libraries (remove_planes ${PCL_LIBRARIES})
target_link_libraries( remove_planes ${OpenCV_LIBS} )
