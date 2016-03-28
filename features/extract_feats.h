#include <iostream>
#include <fstream>
#include <ios>
#include <pcl/point_types.h>
#include <pcl/features/pfh.h>
#include <pcl/features/normal_3d.h>
#include <pcl/features/vfh.h>
#include "pc_tools.h"

extern void save_histogram(const char * in_file,const char * out_file, std::vector<float> histogram);
extern std::vector<float> extract_features(const char * in_path);
extern pcl::PointCloud<pcl::Normal>::Ptr compute_normals(pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud);
extern void compute_PFH_features( pcl::PointCloud<pcl::PointXYZ>::Ptr cloud,pcl::PointCloud<pcl::Normal>::Ptr normals); 
extern std::vector<float>  compute_VFHS_features( pcl::PointCloud<pcl::PointXYZ>::Ptr cloud,pcl::PointCloud<pcl::Normal>::Ptr normals );