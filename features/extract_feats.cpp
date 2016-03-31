#include "extract_feats.h"

std::vector<float> extract_features(const char * in_path){
  cv::Mat depth_img=cv::imread(in_path);
  pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud= img_to_pcl(depth_img);
  pcl::io::savePCDFileASCII ("mycloud", *pcloud);
  //pcl::PointCloud<pcl::Normal>::Ptr normals=compute_normals(pcloud);
  return compute_MOI_features(pcloud);//,normals);
}

void save_histogram(const char * in_file,const char * out_file, std::vector<float> histogram){
  std::ofstream myfile;
  myfile.open (out_file,std::ios::app);
  myfile << in_file<<"#";
  for(int i=0;i<histogram.size();i++){
    myfile << histogram[i] <<",";
  }
  myfile <<"\n";
  myfile.close();
}

pcl::PointCloud<pcl::Normal>::Ptr compute_normals(pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud){
  pcl::NormalEstimation<pcl::PointXYZ, pcl::Normal> ne;
  ne.setInputCloud (pcloud);
  pcl::search::KdTree<pcl::PointXYZ>::Ptr tree (new pcl::search::KdTree<pcl::PointXYZ> ());
  ne.setSearchMethod (tree);

  // Output datasets
  pcl::PointCloud<pcl::Normal>::Ptr cloud_normals (new pcl::PointCloud<pcl::Normal>);

  // Use all neighbors in a sphere of radius 3cm
  ne.setRadiusSearch (7.0);
  ne.compute (*cloud_normals);
  return  cloud_normals;
}

std::vector<float> compute_MOI_features( pcl::PointCloud<pcl::PointXYZ>::Ptr cloud){
  //pcl::PointCloud<pcl::Normal>::Ptr normals ){
  pcl::MomentOfInertiaEstimation <pcl::PointXYZ> feature_extractor;
  feature_extractor.setInputCloud (cloud);
  feature_extractor.compute ();

  std::vector <float> moment_of_inertia;
  std::vector <float> eccentricity;
  pcl::PointXYZ min_point_AABB;
  pcl::PointXYZ max_point_AABB;
  pcl::PointXYZ min_point_OBB;
  pcl::PointXYZ max_point_OBB;
  pcl::PointXYZ position_OBB;
  Eigen::Matrix3f rotational_matrix_OBB;
  float major_value, middle_value, minor_value;
  Eigen::Vector3f major_vector, middle_vector, minor_vector;
  Eigen::Vector3f mass_center;

  feature_extractor.getMomentOfInertia (moment_of_inertia);
  feature_extractor.getEccentricity (eccentricity);
  feature_extractor.getAABB (min_point_AABB, max_point_AABB);
  feature_extractor.getOBB (min_point_OBB, max_point_OBB, position_OBB, rotational_matrix_OBB);
  feature_extractor.getEigenValues (major_value, middle_value, minor_value);
  feature_extractor.getEigenVectors (major_vector, middle_vector, minor_vector);
  feature_extractor.getMassCenter (mass_center);
  std::cout << moment_of_inertia;
  return moment_of_inertia;
}


std::vector<float> compute_VFHS_features( pcl::PointCloud<pcl::PointXYZ>::Ptr cloud,pcl::PointCloud<pcl::Normal>::Ptr normals ){

  pcl::VFHEstimation<pcl::PointXYZ, pcl::Normal, pcl::VFHSignature308> vfh;
  vfh.setInputCloud (cloud);
  vfh.setInputNormals (normals);

  pcl::search::KdTree<pcl::PointXYZ>::Ptr tree (new pcl::search::KdTree<pcl::PointXYZ> ());
  vfh.setSearchMethod (tree);

  pcl::PointCloud<pcl::VFHSignature308>::Ptr vfhs (new pcl::PointCloud<pcl::VFHSignature308> ());

  vfh.compute (*vfhs);
  pcl::VFHSignature308 value=vfhs->points[0];
  std::cout << value;
  std::vector<float> histogram;
  for(int i=0;i< value.descriptorSize();i++){
    histogram.push_back(value.histogram[i]);
  }
  return histogram;
}

void compute_PFH_features( pcl::PointCloud<pcl::PointXYZ>::Ptr cloud,pcl::PointCloud<pcl::Normal>::Ptr normals ){

  pcl::PFHEstimation<pcl::PointXYZ, pcl::Normal, pcl::PFHSignature125> pfh;
  pfh.setInputCloud (cloud);
  pfh.setInputNormals (normals);
  
  pcl::search::KdTree<pcl::PointXYZ>::Ptr tree (new pcl::search::KdTree<pcl::PointXYZ> ());
  pfh.setSearchMethod (tree);

  pcl::PointCloud<pcl::PFHSignature125>::Ptr pfhs (new pcl::PointCloud<pcl::PFHSignature125> ());

  pfh.setRadiusSearch (15.0);

  pfh.compute (*pfhs);

}

int main(int argc,char ** argv){
  if(argc < 3){
    std::vector<float> histogram=extract_features("in.jpg");
    save_histogram("in.jpg","out.txt", histogram);
  }else{
    std::vector<float> histogram=extract_features(argv[1]);
    save_histogram(argv[1],argv[2], histogram);
    std::cout << argv[2]<<"\n";
  }
  return 0;
}
