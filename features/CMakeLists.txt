cmake_minimum_required(VERSION 2.8 FATAL_ERROR)

project(extract_feats)

find_package(PCL 1.2 REQUIRED)
find_package( OpenCV REQUIRED )

include_directories(${PCL_INCLUDE_DIRS})
link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})

add_executable (extract_feats extract_feats.cpp pc_tools.cpp)

target_link_libraries( extract_feats ${PCL_LIBRARIES})
target_link_libraries( extract_feats ${OpenCV_LIBS} )