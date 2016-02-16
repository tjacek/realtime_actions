#include "mediana.h"

cv::Mat mediana_image(string in_path,string out_path){
  vector<std::string> filenames=read_lines(in_path);
  Action action(filenames);
  vector<uchar> series;
  cv::Mat reference_frame=action.empty_frame();//Mat::zeros(action.width,height,CV_8UC1);
  for(int i=0;i<action.width;i++){
  	for(int j=0;j<action.height;j++){
  	  for(int t=0;t<action.length;t++){
  	    uchar value=action[t].at<uchar>(i,j);
  	    series.push_back(value);
  	  }
      reference_frame.at<uchar>(i,j)=mediana(series);
  	}
  }
  return reference_frame;
}

uchar mediana(vector<uchar> &series){
  sort(series.begin(), series.end());
  int size=series.size();
  int midpoint,value;
  if( (size % 2) == 0){
    midpoint=size/2;
    return (series[midpoint]+ series[midpoint])/2;
  }else{
  	midpoint=size/2 +1;
    return series[midpoint];
  }
}

int main(){
  return 0;	
}