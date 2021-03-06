#include "remove_outliers.h"
#include "clusters.h"

void filter_img(std::string in_path,std::string out_path){
  cv::Mat image = cv::imread(in_path,CV_LOAD_IMAGE_GRAYSCALE);
  pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud=img_to_pcl(image);
  /*pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_filtered=radius_filter(pcloud);
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_filtered2=sigma_filter(cloud_filtered); 
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_filtered3= euclidean_clusters( cloud_filtered2 ); */
  //std::vector <pcl::PointIndices> points=growth_segmentation( pcloud);

  std::vector <pcl::PointIndices> points=euclidean_clusters( pcloud);

  //pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_filtered3=largest_cluster(points,pcloud);

  std::vector<Cluster> clusters=to_clouds(points,pcloud);
  pcl::PointXYZ dim(image.rows,image.cols,255);
  save_clusters(out_path,clusters,dim);

  /*normalize_z(cloud_filtered3,-1);

  cv::Mat image2=pcl_to_img( cloud_filtered3,dim,true);
  cv::imwrite(out_path,image2);*/
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

pcl::PointXYZ translate(pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud){
  pcl::PointXYZ min_pt;
  pcl::PointXYZ max_pt;
  pcl::PointXYZ dim;
  pcl::getMinMax3D  (*pcloud,min_pt,max_pt );   
  dim.x=max_pt.x-min_pt.x;
  dim.y=max_pt.y-min_pt.y;
  dim.z=max_pt.z-min_pt.z;
  Eigen::Matrix4f transform_1 = Eigen::Matrix4f::Identity();
  //std::cout << "Dim "<< dim.x << " " << dim.y << " " << dim.z<<"\n";
  transform_1 (0,3) = -min_pt.x;
  transform_1 (1,3) = -min_pt.y;
  transform_1 (2,3) = -min_pt.z;
  pcl::transformPointCloud (*pcloud, *pcloud, transform_1);
  return dim;
}

cv::Mat rescale(cv::Mat img){
  //cv::GaussianBlur( img, img, cv::Size( 5, 5 ), 0, 0 );
  //std::cout << "Transpose "<< img.cols-img.rows  <<"\n";
  bool rescale=false;
  if(rescale && (img.rows-img.cols)<20 ){//img.cols>img.rows){
    //std::cout << "Transpose "<< img.rows-img.cols  <<"\n";
    cv::transpose(img,img);
  }
  cv::Mat dst=cv::Mat::zeros(90,40,CV_8UC1);
  cv::resize(img,dst, dst.size(), 0, 0);//,cv::INTER_LINEAR );
  return dst;
}

std::vector<pcl::PointIndices>  euclidean_clusters(pcl::PointCloud<pcl::PointXYZ>::Ptr cloud){
  pcl::search::KdTree<pcl::PointXYZ>::Ptr tree (new pcl::search::KdTree<pcl::PointXYZ>);
  tree->setInputCloud (cloud);
  std::vector<pcl::PointIndices> clusters;
  pcl::EuclideanClusterExtraction<pcl::PointXYZ> ec;
  ec.setClusterTolerance (1); // 2cm
  ec.setMinClusterSize (10);
  ec.setMaxClusterSize (25000);
  ec.setSearchMethod (tree);
  ec.setInputCloud (cloud);
  ec.extract (clusters);
  
  return clusters;
}


std::vector <pcl::PointIndices> growth_segmentation( pcl::PointCloud<pcl::PointXYZ>::Ptr cloud ){
  //cout << cloud->points.size() <<"\n";
  pcl::search::Search<pcl::PointXYZ>::Ptr tree = boost::shared_ptr<pcl::search::Search<pcl::PointXYZ> > (new pcl::search::KdTree<pcl::PointXYZ>);
  pcl::PointCloud <pcl::Normal>::Ptr normals (new pcl::PointCloud <pcl::Normal>);
  pcl::NormalEstimation<pcl::PointXYZ, pcl::Normal> normal_estimator;
  normal_estimator.setSearchMethod (tree);
  normal_estimator.setInputCloud (cloud);
  normal_estimator.setKSearch (50);
  normal_estimator.compute (*normals);

  pcl::IndicesPtr indices (new std::vector <int>);
  pcl::PassThrough<pcl::PointXYZ> pass;
  pass.setInputCloud (cloud);
  pass.setFilterFieldName ("z");
  pass.setFilterLimits (0.0, 1.0);
  pass.filter (*indices);

  pcl::RegionGrowing<pcl::PointXYZ, pcl::Normal> reg;
  reg.setMinClusterSize (30);
  reg.setMaxClusterSize (1000000);
  reg.setSearchMethod (tree);
  reg.setNumberOfNeighbours (10);
  reg.setInputCloud (cloud);
  //reg.setIndices (indices);
  reg.setInputNormals (normals);
  reg.setSmoothnessThreshold (30.0 / 180.0 * M_PI);
  reg.setCurvatureThreshold (20.0);

  std::vector <pcl::PointIndices> clusters;
  reg.extract (clusters);
  return clusters;
}

int main(int argc,char ** argv)
{ 
  if(argc <3){
     filter_img("/home/user/reps/realtime_actions/filter/depth.jpg",
                "/home/user/reps/realtime_actions/filter/out.jpg");
    //std::cout << "Too few arguments" <<std::endl;
    return 1;
  }
  
  std::string in_path(argv[1]);
  std::string out_path(argv[2]);
  std::cout << in_path << " " << out_path << std::endl;
  /*if(argc==3){
    filter_img(in_path,out_path);
  }*/
  if(argc>2){
    std::string cloud_path(argv[2]);
    cloud_path+=".pcd";
    filter_img(in_path,out_path);
  }
} 