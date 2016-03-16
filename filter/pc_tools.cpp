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

void normalize_z(pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud,int z_max){
  pcl::PointXYZ min_pt;
  pcl::PointXYZ max_pt;
  pcl::getMinMax3D(*pcloud,min_pt,max_pt );
  pcl::PointXYZ dim; 
  dim.x=max_pt.x-min_pt.x;
  dim.y=max_pt.y-min_pt.y;
  dim.z=max_pt.z-min_pt.z;
  /*min_pt.z=max_pt.z;
  for (size_t i = 0; i < pcloud->points.size (); ++i)
  {
    float z=pcloud->points[i].z;

  }*/

  for (size_t i = 0; i < pcloud->points.size (); ++i)
  {
    float raw_z=pcloud->points[i].z;
   // std::cout << (raw_z-min_pt.z+1.0) /dim.z << "\n";
    pcloud->points[i].z=((raw_z-min_pt.z+1.0) /dim.z)*255.0;
  }
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
   // z= 255.0-z;
    if(x<dim.x && y<dim.y){
      img.at<uchar>(x,y)=(uchar) z;
    }
  }
  return img;
}

cv::Mat pcl_to_proj(pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud,pcl::PointXYZ dim){
  std::cout << dim.x;
  cv::Mat img=cv::Mat::zeros(dim.x,3*dim.y,CV_8UC1);
  for (size_t i = 0; i < pcloud->points.size (); ++i)
  {
    int x=(int) pcloud->points[i].x ;
    int y=(int) pcloud->points[i].y;
    float z=(float) pcloud->points[i].z;
    z= ( z/(dim.z+3) )*dim.y;
   // z= 255.0-z;
    if(x<dim.x && y<dim.y){
      
      img.at<uchar>(x,y)=(uchar) z;
      img.at<uchar>(z,y+dim.y)=100; //x;
      img.at<uchar>(z+1,y+dim.y)=100; //x;
      img.at<uchar>(z-1,y+dim.y)=100; //x;
      img.at<uchar>(x,z+2*dim.y)=100;
      img.at<uchar>(x,z-1+2*dim.y)=100;
      img.at<uchar>(x,z+1+2*dim.y)=100;
    }
  }
  return img;
}