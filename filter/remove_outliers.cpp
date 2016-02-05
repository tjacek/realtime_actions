#include "remove_outliers.h"

void filter_img(std::string in_path,std::string out_path){
  cv::Mat image = cv::imread(in_path,CV_LOAD_IMAGE_GRAYSCALE);
  pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud=img_to_pcl(image);
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_filtered=radius_filter(pcloud);
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_filtered2=sigma_filter(cloud_filtered); 
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_filtered3= euclidean_clusters( cloud_filtered2 ); 
  pcl::PointXYZ dim=translate(cloud_filtered3);
  cv::Mat image2=pcl_to_img(cloud_filtered3,dim);
  //cv::Mat image3=rescale(image2);
  cv::imwrite(out_path,image2);
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
    uchar z=(uchar) pcloud->points[i].z;
    if(x<dim.x && y<dim.y){
      img.at<uchar>(x,y)=z;
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
  std::cout << "Dim "<< dim.x << " " << dim.y <<"\n";
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

pcl::PointCloud<pcl::PointXYZ>::Ptr euclidean_clusters(pcl::PointCloud<pcl::PointXYZ>::Ptr cloud){
  pcl::search::KdTree<pcl::PointXYZ>::Ptr tree (new pcl::search::KdTree<pcl::PointXYZ>);
  tree->setInputCloud (cloud);
  std::vector<pcl::PointIndices> clusters;
  pcl::EuclideanClusterExtraction<pcl::PointXYZ> ec;
  ec.setClusterTolerance (20); // 2cm
  ec.setMinClusterSize (10);
  ec.setMaxClusterSize (25000);
  ec.setSearchMethod (tree);
  ec.setInputCloud (cloud);
  ec.extract (clusters);
  int max_cls=max_component(clusters);
  return extract_cloud(clusters[max_cls], cloud);//large_clusters(clusters,cloud);
}


pcl::PointCloud<pcl::PointXYZ>::Ptr growth_segmentation( pcl::PointCloud<pcl::PointXYZ>::Ptr cloud ){
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
  reg.setNumberOfNeighbours (20);
  reg.setInputCloud (cloud);
  //reg.setIndices (indices);
  reg.setInputNormals (normals);
  reg.setSmoothnessThreshold (3.0 / 180.0 * M_PI);
  reg.setCurvatureThreshold (1.0);

  std::vector <pcl::PointIndices> clusters;
  reg.extract (clusters);

  return large_clusters(clusters,cloud);//extract_cloud(clusters[max_cmp], cloud);
}

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
  filter_img(in_path,out_path);
} 