#include "pc_tools.h"
#include <pcl/ModelCoefficients.h>
#include <pcl/io/pcd_io.h>
#include <pcl/point_types.h>
#include <pcl/sample_consensus/method_types.h>
#include <pcl/sample_consensus/model_types.h>
#include <pcl/segmentation/sac_segmentation.h>
#include <pcl/filters/extract_indices.h>
#include <pcl/segmentation/progressive_morphological_filter.h>

extern pcl::PointCloud<pcl::PointXYZ>::Ptr simple_ransac(pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud);
extern pcl::PointCloud<pcl::PointXYZ>::Ptr extract_cloud(pcl::PointIndices::Ptr cls,pcl::PointCloud<pcl::PointXYZ>::Ptr cloud);
extern pcl::PointCloud<pcl::PointXYZ>::Ptr find_planes(pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud,Eigen::Vector3f axsis, 
	                                                     float threshold,float angle);
extern pcl::PointCloud<pcl::PointXYZ>::Ptr find_background(pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud);
