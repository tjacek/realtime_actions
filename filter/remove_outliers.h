#include "pc_tools.h"
#include <pcl/io/pcd_io.h>
#include <pcl/point_types.h>
#include <pcl/filters/radius_outlier_removal.h>
#include <pcl/filters/conditional_removal.h>
#include <pcl/filters/statistical_outlier_removal.h>
#include <pcl/common/transforms.h>
#include <pcl/search/search.h>
#include <pcl/search/kdtree.h>
#include <pcl/features/normal_3d.h>
#include <pcl/filters/passthrough.h>
#include <pcl/filters/extract_indices.h>
#include <pcl/segmentation/region_growing.h>
#include <pcl/segmentation/extract_clusters.h>


extern void filter_img(std::string in_path,std::string out_path);
extern pcl::PointCloud<pcl::PointXYZ>::Ptr radius_filter(pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud);
extern pcl::PointCloud<pcl::PointXYZ>::Ptr sigma_filter(pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud);
extern pcl::PointXYZ translate(pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud);
extern pcl::PointCloud<pcl::PointXYZ>::Ptr growth_segmentation( pcl::PointCloud<pcl::PointXYZ>::Ptr cloud );
extern pcl::PointCloud<pcl::PointXYZ>::Ptr euclidean_clusters(pcl::PointCloud<pcl::PointXYZ>::Ptr cloud);
extern int max_component(std::vector <pcl::PointIndices> clusters);
extern pcl::PointCloud<pcl::PointXYZ>::Ptr extract_cloud(pcl::PointIndices,pcl::PointCloud<pcl::PointXYZ>::Ptr cloud);
extern pcl::PointCloud<pcl::PointXYZ>::Ptr large_clusters(std::vector<pcl::PointIndices> clusters,pcl::PointCloud<pcl::PointXYZ>::Ptr cloud);
extern cv::Mat rescale(cv::Mat image);