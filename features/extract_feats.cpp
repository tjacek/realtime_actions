#include "extract_feats.h"

void extract_features(const char * in_path){
  cv::Mat depth_img=cv::imread(in_path);
  pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud= img_to_pcl(depth_img);
  pcl::PointCloud<pcl::Normal>::Ptr normals=compute_normals(pcloud);
  extract_features(pcloud,normals);
}

 pcl::PointCloud<pcl::Normal>::Ptr compute_normals(pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud){
  pcl::NormalEstimation<pcl::PointXYZ, pcl::Normal> ne;
  ne.setInputCloud (pcloud);
  pcl::search::KdTree<pcl::PointXYZ>::Ptr tree (new pcl::search::KdTree<pcl::PointXYZ> ());
  ne.setSearchMethod (tree);

  // Output datasets
  pcl::PointCloud<pcl::Normal>::Ptr cloud_normals (new pcl::PointCloud<pcl::Normal>);

  // Use all neighbors in a sphere of radius 3cm
  ne.setRadiusSearch (0.03);
  ne.compute (*cloud_normals);
  return  cloud_normals;
}

void compute_features( pcl::PointCloud<pcl::PointXYZ>::Ptr cloud,pcl::PointCloud<pcl::Normal>::Ptr normals ){

  // Create the PFH estimation class, and pass the input dataset+normals to it
  pcl::PFHEstimation<pcl::PointXYZ, pcl::Normal, pcl::PFHSignature125> pfh;
  pfh.setInputCloud (cloud);
  pfh.setInputNormals (normals);
  // alternatively, if cloud is of tpe PointNormal, do pfh.setInputNormals (cloud);

  // Create an empty kdtree representation, and pass it to the PFH estimation object.
  // Its content will be filled inside the object, based on the given input dataset (as no other search surface is given).
  pcl::search::KdTree<pcl::PointXYZ>::Ptr tree (new pcl::search::KdTree<pcl::PointXYZ> ());
  //pcl::KdTreeFLANN<pcl::PointXYZ>::Ptr tree (new pcl::KdTreeFLANN<pcl::PointXYZ> ()); -- older call for PCL 1.5-
  pfh.setSearchMethod (tree);

  // Output datasets
  pcl::PointCloud<pcl::PFHSignature125>::Ptr pfhs (new pcl::PointCloud<pcl::PFHSignature125> ());

  // Use all neighbors in a sphere of radius 5cm
  // IMPORTANT: the radius used here has to be larger than the radius used to estimate the surface normals!!!
  pfh.setRadiusSearch (0.05);

  // Compute the features
  pfh.compute (*pfhs);

  // pfhs->points.size () should have the same size as the input cloud->points.size ()*
}

int main(){
  extract_feature("in.jpg");
  return 0;
}
