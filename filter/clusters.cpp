#include "clusters.h"

pcl::PointCloud<pcl::PointXYZ>::Ptr large_clusters(std::vector<pcl::PointIndices> clusters,pcl::PointCloud<pcl::PointXYZ>::Ptr cloud){
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_cluster (new pcl::PointCloud<pcl::PointXYZ>);
  int min_cls_size=100;
  for(int i=0;i<clusters.size();i++){
    pcl::PointIndices cls=clusters[i];
    if(min_cls_size<cls.indices.size()){
      std::cout << "cloud added size:" << cls.indices.size() <<"\n";
      for (int j=0;j<cls.indices.size();j++){
        int point_index=cls.indices[j];
        cloud_cluster->points.push_back (cloud->points[point_index]);
      } 
    }
  }
  return cloud_cluster;
}

pcl::PointCloud<pcl::PointXYZ>::Ptr extract_cloud(pcl::PointIndices cls,pcl::PointCloud<pcl::PointXYZ>::Ptr cloud){
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_cluster (new pcl::PointCloud<pcl::PointXYZ>);
  for (int i=0;i<cls.indices.size();i++){
  //std::vector<int>::const_iterator pit = ind->indices.begin (); pit != ind->indices.end (); ++pit){
    int point_index=cls.indices[i];
    cloud_cluster->points.push_back (cloud->points[point_index]);
  }
  cloud_cluster->width = cloud_cluster->points.size ();
  cloud_cluster->height = 1;
  cloud_cluster->is_dense = true;
  return cloud_cluster;//cloud_filtered ;
}

int max_component(std::vector <pcl::PointIndices> clusters){
  int max=0;
  int max_cls=0;
  for(int i=0;i<clusters.size();i++){
    if( max<clusters[i].indices.size()){
      max=clusters[i].indices.size();
      max_cls=i;
    }
  }
  return max_cls;
}
