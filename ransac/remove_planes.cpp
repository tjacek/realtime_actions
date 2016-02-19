#include "remove_planes.h"

void filter_img(std::string in_path,std::string out_path){
  cv::Mat image = cv::imread(in_path,CV_LOAD_IMAGE_GRAYSCALE);
  pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud=img_to_pcl(image);
  int iter=1;
  //for(int i=0;i<iter;i++){
 // Eigen::Vector3f z_axsis =Eigen::Vector3f(0.0,0.0,1.0);  
 // pcloud=find_planes(pcloud,z_axsis,5.0,5.0);
 // Eigen::Vector3f y_axsis =Eigen::Vector3f(1.0,0.0,0.0);  
 // pcloud=find_planes(pcloud,y_axsis,10.0,1.0);
  pcl::PointXYZ dim(image.rows,image.cols,255);
 // cv::Mat image2=pcl_to_img(pcloud,dim);
 // cv::imwrite(out_path,image2);
}

pcl::PointCloud<pcl::PointXYZ>::Ptr find_planes(pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud,Eigen::Vector3f axsis,
                                                float threshold,float angle){
  pcl::ModelCoefficients::Ptr coefficients (new pcl::ModelCoefficients);
  pcl::PointIndices::Ptr inliers (new pcl::PointIndices);
  pcl::SACSegmentation<pcl::PointXYZ> seg;
 // Eigen::Vector3f axsis =Eigen::Vector3f(0.0,0.0,1.0);
  seg.setAxis(axsis);
  seg.setEpsAngle((angle*3.14)/180.0);
  seg.setOptimizeCoefficients (true);
  seg.setModelType (pcl::SACMODEL_PLANE);
  seg.setMethodType (pcl::SAC_RANSAC);
  seg.setDistanceThreshold (threshold);
  seg.setInputCloud (pcloud);
  seg.segment (*inliers, *coefficients);
  std::cout << inliers->indices.size();
  return extract_cloud(inliers,pcloud);
}

pcl::PointCloud<pcl::PointXYZ>::Ptr extract_cloud(pcl::PointIndices::Ptr cls,pcl::PointCloud<pcl::PointXYZ>::Ptr cloud){
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_cluster (new pcl::PointCloud<pcl::PointXYZ>);
  pcl::ExtractIndices<pcl::PointXYZ> extract;
  extract.setInputCloud (cloud);
  extract.setIndices (cls);
  extract.setNegative (true);
  extract.filter (* cloud_cluster);
  return cloud_cluster;
}

int main(int argc,char ** argv){
  if(argc <3){
    filter_img("/home/user/reps/realtime_actions/ransac/depth.jpg",
                "/home/user/reps/realtime_actions/ransac/out.jpg");
    return 1;
  }
  std::string in_path(argv[1]);
  std::string out_path(argv[2]);
  std::cout << in_path << " " << out_path << std::endl;
  filter_img(in_path,out_path);
}