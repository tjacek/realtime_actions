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
    image = imread(filename,CV_LOAD_IMAGE_GRAYSCALE);
    frames.push_back(image);
    cout << filename << "\n";
  }
  Mat first=frames[0];
  width=first.rows;
  height=first.cols;
}

BackgroundModel * create_background(VibeParams &params,Action &action){
  return new BackgroundModel(params.nbSamples,action.width,action.height);
}

Mat Action::operator[](int i){
  return frames[i];
}

void vibe(string in_path){
  VibeParams params;
  vector<std::string> filenames=read_lines(in_path);
  Action action(filenames);
  BackgroundModel * model=create_background(params,action);
  for(int t=0;t<action.length;t++){
  	Mat frame=action[t];
  	for(int i=0;i<action.width;i++){
  	  for(int j=0;j<action.height;j++){
  	    uchar value=frame.at<uchar>(i,j);
  	    show_value(value);
        int count=model->compare(i,j,value,params);
		bool isInBackground=  (count >= params.reqMatches);
		if(isInBackground){
		  if(params.decideUpdate()){
		   // model->update(i,j,point ,params);
		  }
		  if(params.decideUpdate()){
			//model->updateNeighbor(i,j,point ,params);
		  }
        }
      }
    }
  }
}

BackgroundModel::BackgroundModel(int size,int width,int height){
  for(int t=0;t<size;t++){
    Mat sample_frame=Mat::zeros(width,height,CV_8UC1);
    samples.push_back(sample_frame);
  }
}

int BackgroundModel::compare(int x,int y,uchar point ,VibeParams & vibeParams){
	int count = 0,index=0;
	while ((count < vibeParams.reqMatches) && (index < vibeParams.nbSamples)){
		uchar sample = samples[index].at<uchar>(x,y);
		uchar distance=abs(point-sample);
		if(distance < vibeParams.radius){
			count++;
		}
		index++;
	}
	return count;
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

void show_value(uchar x){
  int n=(int) x;
  cout << n <<"\n";
}

int main(int argc,char ** argv)
{
  //vector<std::string> filenames=read_lines("/home/user/reps/vibe.txt");
  //Action action(filenames);
  vibe("/home/user/reps/vibe.txt");
}