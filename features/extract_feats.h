#include <pcl/point_types.h>
#include <pcl/features/pfh.h>
#include <pcl/features/normal_3d.h>
#include "pc_tools.h"

extern void extract_features(const char * in_path);
extern pcl::PointCloud<pcl::Normal>::Ptr compute_normals(pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud);
extern void compute_features( pcl::PointCloud<pcl::PointXYZ>::Ptr cloud,pcl::PointCloud<pcl::Normal>::Ptr normals); 
