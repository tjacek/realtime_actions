#include <sstream>
#include <fstream>
#include <string>
#include <iostream>
#include <vector>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace std;
using namespace cv;
extern vector<std::string> read_lines(std::string name);

typedef Mat BackgroundModel;

class Action
{
  public:
  	int length;
  	int width;
  	int height;
  	
	Action(vector<std::string> str);
	BackgroundModel create_background();
	Mat operator[](int i);
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