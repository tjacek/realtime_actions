#include "vibe.h"

vector<string> read_lines(string name){
  std::string line;
  ifstream infile;
  infile.open(name.c_str());
  vector<string> str_vector;	
  while (std::getline(infile, line))
  {
  	cout << line <<"\n";
  	str_vector.push_back(line);

  }
  return str_vector;
 }

int main(int argc,char ** argv)
{
  read_lines("/home/user/reps/vibe.txt");
}