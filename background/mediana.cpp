#include "mediana.h"

void mediana_image(string in_path,string out_path){
  vector<std::string> filenames=read_lines(in_path);
  Action action(filenames);
  cv::Mat background=get_background(action);
  for(int i=0;i<action.width;i++){
  	for(int j=0;j<action.height;j++){
  	  int mediana_xy=background.at<uchar>(i,j);
  	  for(int t=0;t<action.length;t++){
  	  	int value=action[t].at<uchar>(i,j);
        if(value!=0){
          int diff=abs(value-mediana_xy);
          if(diff<10){
          	action[t].at<uchar>(i,j)=0;
          }
        }
  	  }
  	}
  }
  save_action(out_path,action.frames);

}

cv::Mat get_background(Action & action){
  vector<uchar> series;
  cv::Mat reference_frame=action.empty_frame();//Mat::zeros(action.width,height,CV_8UC1);
  for(int i=0;i<action.width;i++){
  	for(int j=0;j<action.height;j++){
  	  series.clear();	
  	  for(int t=0;t<action.length;t++){
  	    uchar value=action[t].at<uchar>(i,j);
  	    //if(value!=0){
  	      series.push_back(value);
  	    //}
  	  }
      reference_frame.at<uchar>(i,j)=mediana(series);
  	}
  }
  return reference_frame;
}

uchar mediana(vector<uchar> &series){
  sort(series.begin(), series.end());
  int size=series.size();
  if(size==0){
  	return 0;
  }
  int midpoint,value;
  if( (size % 2) == 0){
    midpoint=size/2;
    return (series[midpoint]+ series[midpoint])/2;
  }else{
  	midpoint=size/2 +1;
    return series[midpoint];
  }
}

int main(int argc,char ** argv){
   if(argc < 3){
    std::cout << "Too few arguments " << std::endl;
    return 1;
  }

  string in_path(argv[1]);
  string out_path(argv[2]);
  mediana_image(in_path,out_path);
}