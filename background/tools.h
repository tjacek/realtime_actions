#include <algorithm>
#include <sstream>
#include <fstream>
#include <string>
#include <iostream>
#include <vector>
#include <cmath> 
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui_c.h>
using namespace std;
using namespace cv;

class Action
{
  public:
  	int length;
  	int width;
  	int height;
  	
	Action(vector<std::string> str);
	Mat operator[](int i);
	Mat empty_frame();
    uchar get_rvalue(int i,int j);
  	vector<cv::Mat> frames;
};

extern vector<std::string> read_lines(std::string name);
extern void save_action(string out_path,vector<Mat> action);
extern void show_value(uchar x);