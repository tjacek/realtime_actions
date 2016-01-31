#include "remove_outliers.h"

pcl::PointCloud<pcl::PointXYZ>::Ptr img_to_pcl(cv::Mat img){
  std::cout << img.rows <<" " << img.cols << "\n";
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud (new pcl::PointCloud<pcl::PointXYZ>);
  for(int i=0;i<img.rows;i++){
    for(int j=0;j<img.cols;j++){
      float z= (float) img.at<uchar>(i,j);
      if(z!=0.0){
        pcl::PointXYZ point((float)i, (float) j,z);
        cloud->push_back (point);
      }
    }
  }
  return cloud;
}

cv::Mat pcl_to_img(pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud){
  cv::Mat img=cv::Mat::zeros(350,350,CV_8UC1);
  for (size_t i = 0; i < pcloud->points.size (); ++i)
  {
    uchar x=(uchar) pcloud->points[i].x ;
    uchar y=(uchar) pcloud->points[i].y;
    uchar z=pcloud->points[i].z;
    img.at<uchar>(x,y)=z;
  }
  return img;
}

int main(int argc,char ** argv)
{
  
  cv::Mat image = cv::imread("test.jpg",CV_LOAD_IMAGE_GRAYSCALE);
  pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud=img_to_pcl(image);
  //pcl::io::savePCDFileASCII ("test_pcd.pcd", *pcloud);
  cv::Mat image2=pcl_to_img(pcloud);
  cv::imwrite("result.jpg",image2);
 /*if (argc != 2)
  {
    std::cerr << "please specify command line arg '-r' or '-c'" << std::endl;
    exit(0);
  }
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud (new pcl::PointCloud<pcl::PointXYZ>);
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_filtered (new pcl::PointCloud<pcl::PointXYZ>);

  // Fill in the cloud data
  cloud->width  = 5;
  cloud->height = 1;
  cloud->points.resize (cloud->width * cloud->height);

  for (size_t i = 0; i < cloud->points.size (); ++i)
  {
    cloud->points[i].x = 1024 * rand () / (RAND_MAX + 1.0f);
    cloud->points[i].y = 1024 * rand () / (RAND_MAX + 1.0f);
    cloud->points[i].z = 1024 * rand () / (RAND_MAX + 1.0f);
  }

  if (strcmp(argv[1], "-r") == 0){
    pcl::RadiusOutlierRemoval<pcl::PointXYZ> outrem;
    // build the filter
    outrem.setInputCloud(cloud);
    outrem.setRadiusSearch(0.8);
    outrem.setMinNeighborsInRadius (2);
    // apply filter
    outrem.filter (*cloud_filtered);
  }
  else if (strcmp(argv[1], "-c") == 0){
    // build the condition
    pcl::ConditionAnd<pcl::PointXYZ>::Ptr range_cond (new
      pcl::ConditionAnd<pcl::PointXYZ> ());
    range_cond->addComparison (pcl::FieldComparison<pcl::PointXYZ>::ConstPtr (new
      pcl::FieldComparison<pcl::PointXYZ> ("z", pcl::ComparisonOps::GT, 0.0)));
    range_cond->addComparison (pcl::FieldComparison<pcl::PointXYZ>::ConstPtr (new
      pcl::FieldComparison<pcl::PointXYZ> ("z", pcl::ComparisonOps::LT, 0.8)));
    // build the filter
    pcl::ConditionalRemoval<pcl::PointXYZ> condrem (range_cond);
    condrem.setInputCloud (cloud);
    condrem.setKeepOrganized(true);
    // apply filter
    condrem.filter (*cloud_filtered);
  }
  else{
    std::cerr << "please specify command line arg '-r' or '-c'" << std::endl;
    exit(0);
  }
  std::cerr << "Cloud before filtering: " << std::endl;
  for (size_t i = 0; i < cloud->points.size (); ++i)
    std::cerr << "    " << cloud->points[i].x << " "
                        << cloud->points[i].y << " "
                        << cloud->points[i].z << std::endl;
  // display pointcloud after filtering
  std::cerr << "Cloud after filtering: " << std::endl;
  for (size_t i = 0; i < cloud_filtered->points.size (); ++i)
    std::cerr << "    " << cloud_filtered->points[i].x << " "
                        << cloud_filtered->points[i].y << " "
                        << cloud_filtered->points[i].z << std::endl;
  return (0);*/
} 
