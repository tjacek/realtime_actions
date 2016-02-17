#include "remove_planes.h"

void filter_img(std::string in_path,std::string out_path){
  cv::Mat image = cv::imread(in_path,CV_LOAD_IMAGE_GRAYSCALE);
  pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud=img_to_pcl(image);
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_filtered=find_planes(pcloud);
  cv::Mat image2=pcl_to_img(cloud_filtered,image.rows,image.cols);
  cv::imwrite(out_path,image2);
}

pcl::PointCloud<pcl::PointXYZ>::Ptr find_planes(pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud){
  pcl::ModelCoefficients::Ptr coefficients (new pcl::ModelCoefficients);
  pcl::PointIndices::Ptr inliers (new pcl::PointIndices);
  pcl::SACSegmentation<pcl::PointXYZ> seg;
  seg.setOptimizeCoefficients (true);
  seg.setModelType (pcl::SACMODEL_PLANE);
  seg.setMethodType (pcl::SAC_RANSAC);
  seg.setDistanceThreshold (10.0);
  seg.setInputCloud (pcloud);
  seg.segment (*inliers, *coefficients);
  std::cout << inliers->indices.size();
  return extract_cloud(*inliers,pcloud);
}

pcl::PointCloud<pcl::PointXYZ>::Ptr extract_cloud(pcl::PointIndices cls,pcl::PointCloud<pcl::PointXYZ>::Ptr cloud){
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_cluster (new pcl::PointCloud<pcl::PointXYZ>);
  pcl::ExtractIndices<pcl::PointXYZ> extract;
  extract.setInputCloud (cloud);
  extract.setIndices (cls);
  extract.setNegative (false);
  extract.filter (* cloud_cluster);
  /*pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_cluster (new pcl::PointCloud<pcl::PointXYZ>);
  for (int i=0;i<cls.indices.size();i++){
    int point_index=cls.indices[i];
    cloud_cluster->points.push_back (cloud->points[point_index]);
  }
  cloud_cluster->width = cloud_cluster->points.size ();
  cloud_cluster->height = 1;
  cloud_cluster->is_dense = true;*/
  return cloud_cluster;
}

pcl::PointCloud<pcl::PointXYZ>::Ptr img_to_pcl(cv::Mat img){
  std::cout << img.rows <<" " << img.cols << "\n";
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud (new pcl::PointCloud<pcl::PointXYZ>);
  for(int i=0;i<img.rows;i++){
    for(int j=0;j<img.cols;j++){
      float z= (float) img.at<uchar>(i,j);
      if(z>10.0){
        pcl::PointXYZ point((float)i, (float) j,z);
        cloud->push_back (point);
      }
    }
  }
  return cloud;
} 

cv::Mat pcl_to_img(pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud,int width,int height){
  cv::Mat img=cv::Mat::zeros(width,height,CV_8UC1);
  for (size_t i = 0; i < pcloud->points.size (); ++i)
  {
    int x=(int) pcloud->points[i].x ;
    int y=(int) pcloud->points[i].y;
    uchar z=(uchar) pcloud->points[i].z;
    img.at<uchar>(x,y)=z;
    if(x<10){
    }
  }
  return img;
}

int main(int argc,char ** argv){
  filter_img("/home/user/reps/realtime_actions/ransac/depth.jpg",
                "/home/user/reps/realtime_actions/ransac/out.jpg");
}