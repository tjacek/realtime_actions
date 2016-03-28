#include "extract_feats.h"

std::vector<float> extract_features(const char * in_path){
  cv::Mat depth_img=cv::imread(in_path);
  pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud= img_to_pcl(depth_img);
  pcl::PointCloud<pcl::Normal>::Ptr normals=compute_normals(pcloud);
  return compute_VFHS_features(pcloud,normals);
}

 pcl::PointCloud<pcl::Normal>::Ptr compute_normals(pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud){
  pcl::NormalEstimation<pcl::PointXYZ, pcl::Normal> ne;
  ne.setInputCloud (pcloud);
  pcl::search::KdTree<pcl::PointXYZ>::Ptr tree (new pcl::search::KdTree<pcl::PointXYZ> ());
  ne.setSearchMethod (tree);

  // Output datasets
  pcl::PointCloud<pcl::Normal>::Ptr cloud_normals (new pcl::PointCloud<pcl::Normal>);

  // Use all neighbors in a sphere of radius 3cm
  ne.setRadiusSearch (5.0);
  ne.compute (*cloud_normals);
  return  cloud_normals;
}


std::vector<float> compute_VFHS_features( pcl::PointCloud<pcl::PointXYZ>::Ptr cloud,pcl::PointCloud<pcl::Normal>::Ptr normals ){

  pcl::VFHEstimation<pcl::PointXYZ, pcl::Normal, pcl::VFHSignature308> vfh;
  vfh.setInputCloud (cloud);
  vfh.setInputNormals (normals);
  // alternatively, if cloud is of type PointNormal, do vfh.setInputNormals (cloud);

  // Create an empty kdtree representation, and pass it to the FPFH estimation object.
  // Its content will be filled inside the object, based on the given input dataset (as no other search surface is given).
  pcl::search::KdTree<pcl::PointXYZ>::Ptr tree (new pcl::search::KdTree<pcl::PointXYZ> ());
  vfh.setSearchMethod (tree);

  // Output datasets
  pcl::PointCloud<pcl::VFHSignature308>::Ptr vfhs (new pcl::PointCloud<pcl::VFHSignature308> ());

  // Compute the features
  vfh.compute (*vfhs);
  pcl::VFHSignature308 value=vfhs->points[0];
  std::cout << value;
  std::vector<float> histogram;
  for(int i=0;i< value.descriptorSize();i++){
    histogram.push_back(value.histogram[i]);
  }
  return histogram;
}

void compute_PFH_features( pcl::PointCloud<pcl::PointXYZ>::Ptr cloud,pcl::PointCloud<pcl::Normal>::Ptr normals ){

  pcl::PFHEstimation<pcl::PointXYZ, pcl::Normal, pcl::PFHSignature125> pfh;
  pfh.setInputCloud (cloud);
  pfh.setInputNormals (normals);
  
  pcl::search::KdTree<pcl::PointXYZ>::Ptr tree (new pcl::search::KdTree<pcl::PointXYZ> ());
  pfh.setSearchMethod (tree);

  pcl::PointCloud<pcl::PFHSignature125>::Ptr pfhs (new pcl::PointCloud<pcl::PFHSignature125> ());

  pfh.setRadiusSearch (10.0);

  pfh.compute (*pfhs);

}

int main(){
  extract_features("in.jpg");
  return 0;
}
