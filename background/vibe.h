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

class Action
{
  public:
  	vector<cv::Mat> frames;
	Action(vector<std::string> str);
	//~vibe();
};