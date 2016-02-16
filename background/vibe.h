#include "tools.h"
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui_c.h>

using namespace std;
using namespace cv;

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
    BackgroundModel(int size,Action& action);
  	int compare(int x,int y,uchar point ,VibeParams & vibeParams);
  	void updateNeighbor(int x,int y,uchar point ,VibeParams & vibeParams);
  	void update(int x,int y,uchar point ,VibeParams & vibeParams);
   
  private:
  	vector<Mat> samples;
};

extern BackgroundModel * create_background(VibeParams &params,Action &action);