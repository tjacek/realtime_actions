#include "clusters.h"

void save_clusters(std::string out_path,std::vector <pcl::PointIndices> clusters){
  std::cout << "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%";
  for(int i=0; i<clusters.size();i++){
    std::stringstream ss;
    ss << i;
    std::string s = ss.str();
    s+=".jpg";
    s="out"+s;
    std::string full_path=out_path+"/"+s;//out_path.replace(;);
    std::cout << full_path << "\n"; 

    //cv::Mat pcl_to_img(pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud,pcl::PointXYZ dim
  }
}

pcl::PointCloud<pcl::PointXYZ>::Ptr largest_cluster(std::vector<pcl::PointIndices> clusters,
                                                    pcl::PointCloud<pcl::PointXYZ>::Ptr cloud){
  int max_cls=max_component(clusters);
  //,pcl::PointCloud<pcl::PointXYZ>::Ptr cloud){
  /*pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_cluster (new pcl::PointCloud<pcl::PointXYZ>);
  int min_cls_size=100;
  for(int i=0;i<clusters.size();i++){
    pcl::PointIndices cls=clusters[i];
    if(min_cls_size<cls.indices.size()){
      //std::cout << "cloud added size:" << cls.indices.size() <<"\n";
      for (int j=0;j<cls.indices.size();j++){
        int point_index=cls.indices[j];
        cloud_cluster->points.push_back (cloud->points[point_index]);
      } 
    }
  }*/
  return extract_cloud(clusters[max_cls],cloud);;
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
