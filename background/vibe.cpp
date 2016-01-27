#include "vibe.h"

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
    image = imread(filename,CV_64F);
    frames.push_back(image);
    cout << filename << "\n";
  }
  Mat first=frames[0];
  width=first.rows;
  height=first.cols;
}

BackgroundModel Action::create_background(){
  BackgroundModel model=Mat::zeros(width,height,CV_64F);
  return model;
}

Mat Action::operator[](int i){
  return frames[i];
}

void vibe(string in_path){
  vector<std::string> filenames=read_lines(in_path);
  Action action(filenames);
  for(int t=0;t<action.length;t++){
  	Mat frame=action[t];
  	for(int x_i=0;x_i<action.width;x_i++){
  	  for(int y_i=0;y_i<action.height;y_i++){
  	    double value=frame.at<double>(x_i,y_i);
        cout << value << "\n";
      }
    }
  }
}

VibeParams::VibeParams(){
    this->nbSamples = 10;                  
    this->reqMatches = 1;                   
    this->radius = 2;                     
    this->subsamplingFactor = 17;  
}

int VibeParams::getRand(){
	return std::rand() % subsamplingFactor;
}

bool VibeParams::decideUpdate(){
	 return getRand()==0;
}

int main(int argc,char ** argv)
{
  //vector<std::string> filenames=read_lines("/home/user/reps/vibe.txt");
  //Action action(filenames);
  vibe("/home/user/reps/vibe.txt");
}