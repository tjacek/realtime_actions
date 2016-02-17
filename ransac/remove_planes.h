#include <iostream>
#include <pcl/ModelCoefficients.h>
#include <pcl/io/pcd_io.h>
#include <pcl/point_types.h>
#include <pcl/sample_consensus/method_types.h>
#include <pcl/sample_consensus/model_types.h>
#include <pcl/segmentation/sac_segmentation.h>
#include <pcl/filters/extract_indices.h>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include "opencv2/imgproc/imgproc.hpp"

extern pcl::PointCloud<pcl::PointXYZ>::Ptr img_to_pcl(cv::Mat depth_img);
extern cv::Mat pcl_to_img(pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud,int width,int height);
extern pcl::PointCloud<pcl::PointXYZ>::Ptr extract_cloud(pcl::PointIndices cls,pcl::PointCloud<pcl::PointXYZ>::Ptr cloud);
extern pcl::PointCloud<pcl::PointXYZ>::Ptr find_planes(pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud);
