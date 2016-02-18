#include "pc_tools.h"

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

cv::Mat pcl_to_img(pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud){
  pcl::PointXYZ dim(350,350,255);
  return pcl_to_img(pcloud,dim);
}

cv::Mat pcl_to_img(pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud,pcl::PointXYZ dim){
  std::cout << dim.x;
  cv::Mat img=cv::Mat::zeros(dim.x,dim.y,CV_8UC1);
  for (size_t i = 0; i < pcloud->points.size (); ++i)
  {
    int x=(int) pcloud->points[i].x ;
    int y=(int) pcloud->points[i].y;
    float z=(float) pcloud->points[i].z;
    z= ( z/(dim.z+3) )*255.0;
    z= 255.0-z;
    if(x<dim.x && y<dim.y){
      img.at<uchar>(x,y)=(uchar) z;
    }
  }
  return img;
}