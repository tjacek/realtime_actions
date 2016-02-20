#ifndef PC_TOOLS
#define PC_TOOLS
#include <pcl/common/common.h>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <pcl/visualization/cloud_viewer.h>
#include <pcl/io/io.h>
#include <pcl/io/pcd_io.h>

extern pcl::PointCloud<pcl::PointXYZ>::Ptr img_to_pcl(cv::Mat depth_img);
extern cv::Mat pcl_to_img(pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud,pcl::PointXYZ dim);
extern cv::Mat pcl_to_img(pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud);
extern void show_clouds(pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud);
#endif