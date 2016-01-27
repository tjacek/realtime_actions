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
  for(vector<std::string>::iterator it = names.begin(); it != names.end(); ++it){
    std::string filename=*it;
    Mat image;
    image = imread(filename, CV_LOAD_IMAGE_COLOR);
    frames.push_back(image);
    cout << filename << "\n";
  }
}

int main(int argc,char ** argv)
{
  vector<std::string> filenames=read_lines("/home/user/reps/vibe.txt");
  Action action(filenames);
}