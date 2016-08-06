#include <iostream>
#include <opencv2/opencv.hpp>
 
using namespace std;
using namespace cv;

class Transformation
{
public:
    Mat call(Mat img);
    void transform(string in_path,string out_path);

};


Mat Transformation::call(Mat img){
  img+=50.0;
  return img;
}

void Transformation::transform(string in_path,string out_path){
    cv::Mat img = cv::imread(in_path,CV_LOAD_IMAGE_GRAYSCALE);
    cv::Mat img2=this->call(img);
    cv::imwrite(out_path,img2);
}

 
int main (int argc, const char * argv[])
{   

    Transformation trans;
    string in_path="in.jpg";
    string out_path="out_path.jpg";
    trans.transform(in_path,out_path);
 
    /*Mat img;
    HOGDescriptor hog;
    hog.setSVMDetector(HOGDescriptor::getDefaultPeopleDetector());
 
    while (true)
    {
        cap >> img;
        if (!img.data)
            continue;
 
        vector<Rect> found, found_filtered;
        hog.detectMultiScale(img, found, 0, Size(8,8), Size(32,32), 1.05, 2);
 
        size_t i, j;
        for (i=0; i<found.size(); i++)
        {
            Rect r = found[i];
            for (j=0; j<found.size(); j++)
                if (j!=i && (r & found[j])==r)
                    break;
            if (j==found.size())
                found_filtered.push_back(r);
        }
        for (i=0; i<found_filtered.size(); i++)
        {
	    Rect r = found_filtered[i];
            r.x += cvRound(r.width*0.1);
	    r.width = cvRound(r.width*0.8);
	    r.y += cvRound(r.height*0.06);
	    r.height = cvRound(r.height*0.9);
	    rectangle(img, r.tl(), r.br(), cv::Scalar(0,255,0), 2);
	}
        imshow("video capture", img);
        if (waitKey(20) >= 0)
            break;
    }*/
    return 0;
}