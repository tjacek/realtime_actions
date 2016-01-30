#include <iostream>
#include <pcl/io/pcd_io.h>
#include <pcl/point_types.h>
#include <pcl/filters/radius_outlier_removal.h>
#include <pcl/filters/conditional_removal.h>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

extern pcl::PointCloud<pcl::PointXYZ>* img_to_pcl(cv::Mat depth_img);