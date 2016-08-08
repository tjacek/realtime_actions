#ifndef PC_CLUSTERS
#define PC_CLUSTERS
#include <pcl/common/common.h>
#include <pcl/search/search.h>
#include <pcl/search/kdtree.h>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include "opencv2/imgproc/imgproc.hpp"

extern pcl::PointCloud<pcl::PointXYZ>::Ptr extract_cloud(pcl::PointIndices,pcl::PointCloud<pcl::PointXYZ>::Ptr cloud);
extern pcl::PointCloud<pcl::PointXYZ>::Ptr largest_cluster(std::vector<pcl::PointIndices> clusters,pcl::PointCloud<pcl::PointXYZ>::Ptr cloud);
	//,pcl::PointCloud<pcl::PointXYZ>::Ptr cloud);
extern int max_component(std::vector <pcl::PointIndices> clusters);
extern void save_clusters(std::string out_path,std::vector <pcl::PointIndices> clusters);

#endif