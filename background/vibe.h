#include <sstream>
#include <fstream>
#include <string>
#include <iostream>
#include <vector>
#include <cmath> 
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

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
  private:
  	vector<cv::Mat> frames;
};

class VibeParams{
  public:
   int nbSamples;                   
   int reqMatches;                   
   int radius;                      
   int subsamplingFactor; 

   VibeParams();
//   VibeParams(int nbSamples, reqMatches,uchar radius,uchar subsamplingFactor);

   int getRand();
   bool decideUpdate();
};

class BackgroundModel{
  public:
  	BackgroundModel(int size,int width,int height);
  	BackgroundModel(int size,Mat prototype);
  	int compare(int x,int y,uchar point ,VibeParams & vibeParams);
  	void updateNeighbor(int x,int y,uchar point ,VibeParams & vibeParams);
  	void update(int x,int y,uchar point ,VibeParams & vibeParams);
   
  private:
  	vector<Mat> samples;
};

extern vector<std::string> read_lines(std::string name);
extern BackgroundModel * create_background(VibeParams &params,Action &action);
extern void save_action(string out_path,vector<Mat> action);
extern void show_value(uchar x);