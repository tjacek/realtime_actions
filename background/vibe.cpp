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
    cv::GaussianBlur( image, image, Size( 7, 7 ), 0, 0 );
    frames.push_back(image);
    cout << filename << "\n";
  }
  Mat first=frames[0];
  width=first.rows;
  height=first.cols;
}

 Mat Action::empty_frame(){
   return Mat::zeros(width,height,CV_8UC1);
 }

uchar Action::get_rvalue(int i,int j){
  int t=std::rand() % frames.size();
  uchar value=frames[t].at<uchar>(i,j);
  return value;   
}

BackgroundModel * create_background(VibeParams &params,Action &action){
  return new BackgroundModel(params.nbSamples,action);
}

void vibe(string in_path,string out_path){
  VibeParams params;
  vector<std::string> filenames=read_lines(in_path);
  Action action(filenames);
  BackgroundModel * model=create_background(params,action);
  vector<Mat> foreground;
  for(int t=0;t<action.length;t++){
  	Mat frame=action[t];
  	Mat new_frame=action.empty_frame();
  	for(int i=0;i<action.width;i++){
  	  for(int j=0;j<action.height;j++){
  	    uchar value=frame.at<uchar>(i,j);
  	    
        int count=model->compare(i,j,value,params);
		bool isInBackground=  (count >= params.reqMatches);
		if(isInBackground){
		  if(params.decideUpdate()){
		    model->update(i,j,value ,params);
		  }
		  if(params.decideUpdate()){
			model->updateNeighbor(i,j,value ,params);
		  }

        }else{
          //show_value(value);
          new_frame.at<uchar>(i,j)=value;	
        }
      }
    }
    foreground.push_back(new_frame);
  }
  save_action(out_path,foreground);
}

BackgroundModel::BackgroundModel(int size,int width,int height){
  for(int t=0;t<size;t++){
    Mat sample_frame=Mat::zeros(width,height,CV_8UC1);
    samples.push_back(sample_frame);
  }
}

BackgroundModel::BackgroundModel(int size,Mat prototype){
  for(int t=0;t<size;t++){
    Mat sample_frame=prototype.clone();
    samples.push_back(sample_frame);
  }
}

BackgroundModel::BackgroundModel(int size,Action& action){
  for(int t=0;t<size;t++){
    Mat sample_frame=Mat::zeros(action.width,action.height,CV_8UC1);
    for(int i=0;i<action.width;i++){
      for(int j=0;j<action.height;j++){
        sample_frame.at<uchar>(i,j)=action.get_rvalue(i,j);
      }
    }
    samples.push_back(sample_frame);
  } 
}

Mat Action::operator[](int i){
  return frames[i];
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

void BackgroundModel::updateNeighbor(int x,int y,uchar point ,VibeParams & vibeParams){
    int randn= rand() % 3;
	int x0 = randn-1;//nearX[randn];
    randn= rand() % 3;
	int y0 = randn-1;//nearY[randn];

	x0+= x;
	y0+= y;
	update(x0,y0,point ,vibeParams);
}

void BackgroundModel::update(int x,int y,uchar point ,VibeParams & vibeParams){
  if(x<0 || y<0){
    return;
  }
  if(x>samples[0].rows-1 || y>samples[0].cols-1){
    return;
  }
  samples[vibeParams.getRand()].at<uchar>(x,y)=point;
}

VibeParams::VibeParams(){
  this->nbSamples = 10;                  
  this->reqMatches = 3;                   
  this->radius = 30;                     
  this->subsamplingFactor = 5;  
}

int VibeParams::getRand(){
  return std::rand() % nbSamples;//subsamplingFactor;
}

bool VibeParams::decideUpdate(){
  int n=std::rand() % subsamplingFactor;
  return n==0;
}

void show_value(uchar x){
  int n=(int) x;
  cout << n <<"\n";
}

void save_action(string out_path,vector<Mat> action){
  for(int t=0;t<action.size();t++){
  	string full_out_path=out_path+"frame"+std::to_string(t)+".jpg";
    imwrite(full_out_path,action[t]);
  }	
}

int main(int argc,char ** argv)
{
  if(argc < 3){
    std::cout << "Too few arguments " << std::endl;
    return 1;
  }

  string in_path(argv[1]);
  string out_path(argv[2]);
  vibe(in_path,out_path);
}