#include "tools.h"

vector<std::string> read_lines(string name){
  std::string line;
  ifstream infile;
  infile.open(name.c_str());
  vector<std::string> str_vector;	
  while (std::getline(infile, line))
  {
    str_vector.push_back(line);
  }
  return str_vector;
 }

Action::Action(vector<std::string> names){
  length=names.size();
  for(vector<std::string>::iterator it = names.begin(); it != names.end(); ++it){
    std::string filename=*it;
    Mat image;
    image = imread(filename,CV_LOAD_IMAGE_GRAYSCALE);
    //cv::GaussianBlur( image, image, Size( 7, 7 ), 0, 0 );
    frames.push_back(image);
    cout << filename << "\n";
  }
  Mat first=frames[0];
  width=first.rows;
  height=first.cols;
}

 Mat Action::empty_frame(){
   return Mat::zeros(width,height,CV_8UC1);
 }

uchar Action::get_rvalue(int i,int j){
  int t=std::rand() % frames.size();
  uchar value=frames[t].at<uchar>(i,j);
  return value;   
}

Mat Action::operator[](int i){
  return frames[i];
}

void show_value(uchar x){
  int n=(int) x;
  cout << n <<"\n";
}

void save_action(string out_path,vector<Mat> action){
  for(int t=0;t<action.size();t++){
    string full_out_path=out_path+"frame"+std::to_string(t)+".jpg";
    imwrite(full_out_path,action[t]);
  } 
}