#include "remove_outliers.h"

void filter_img(std::string in_path,std::string out_path){
  cv::Mat image = cv::imread(in_path,CV_LOAD_IMAGE_GRAYSCALE);
  pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud=img_to_pcl(image);
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_filtered=radius_filter(pcloud);
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_filtered2=sigma_filter(cloud_filtered);  
  pcl::PointXYZ dim=translate(cloud_filtered2);
  cv::Mat image2=pcl_to_img(cloud_filtered2,dim);
  cv::Mat image3=rescale(image2);
  cv::imwrite(out_path,image3);
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

pcl::PointCloud<pcl::PointXYZ>::Ptr radius_filter(pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud){
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_filtered (new pcl::PointCloud<pcl::PointXYZ>);
  pcl::RadiusOutlierRemoval<pcl::PointXYZ> outrem;
    // build the filter
  outrem.setInputCloud(pcloud);
  outrem.setRadiusSearch(10.0);
  outrem.setMinNeighborsInRadius (20);
  outrem.filter (*cloud_filtered);
  return cloud_filtered;
}

pcl::PointCloud<pcl::PointXYZ>::Ptr sigma_filter(pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud){
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_filtered (new pcl::PointCloud<pcl::PointXYZ>);
  pcl::StatisticalOutlierRemoval<pcl::PointXYZ> sor;
  sor.setInputCloud (pcloud);
  sor.setMeanK (50);
  sor.setStddevMulThresh (1.0);
  sor.filter (*cloud_filtered);
  return cloud_filtered;
}

cv::Mat pcl_to_img(pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud,pcl::PointXYZ dim){
  cv::Mat img=cv::Mat::zeros(dim.x,dim.y,CV_8UC1);
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

pcl::PointXYZ translate(pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud){
  pcl::PointXYZ min_pt;
  pcl::PointXYZ max_pt;
  pcl::PointXYZ dim;
  pcl::getMinMax3D  (*pcloud,min_pt,max_pt );   
  dim.x=max_pt.x-min_pt.x;
  dim.y=max_pt.y-min_pt.y;
  dim.z=0;
  Eigen::Matrix4f transform_1 = Eigen::Matrix4f::Identity();
  std::cout << dim.x << " " << dim.y <<"\n";
  transform_1 (0,3) = -min_pt.x;
  transform_1 (1,3) = -min_pt.y;
  pcl::transformPointCloud (*pcloud, *pcloud, transform_1);
  return dim;
}

cv::Mat rescale(cv::Mat img){
  cv::Mat dst=cv::Mat::zeros(90,40,CV_8UC1);
  cv::resize(img,dst, dst.size(), 0, 0);//,cv::INTER_LINEAR );
  return dst;
}

int main(int argc,char ** argv)
{ 
  if(argc <3){
    std::cout << "Too few arguments" <<std::endl;
    return 1;
  }
  std::string in_path(argv[1]);
  std::string out_path(argv[2]);
  std::cout << in_path << " " << out_path << std::endl;
  filter_img(in_path,out_path);
} 