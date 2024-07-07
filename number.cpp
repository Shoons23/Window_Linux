#include <iostream>
#include <fstream>
#include <opencv2/opencv.hpp>
#include <tesseract/baseapi.h>
#include <leptonica/allheaders.h>

using namespace cv;
using namespace std;

Mat preprocessImage(const string& imagePath) {
    // 이미지 읽기
    Mat image = imread(imagePath, IMREAD_COLOR);
    if (image.empty()) {
        throw runtime_error("Image file not found at the specified path: " + imagePath);
    }

    // 이미지를 회색조로 변환
    Mat gray;
    cvtColor(image, gray, COLOR_BGR2GRAY);

    // 블러링을 통해 노이즈 제거
    medianBlur(gray, gray, 5);

    // 경계선 감지
    Mat edges;
    Canny(gray, edges, 100, 200);

    return edges;
}

void detectPlate(const string& imagePath) {
    Mat edges = preprocessImage(imagePath);
    Mat image = imread(imagePath, IMREAD_COLOR);

    // 컨투어(윤곽선) 찾기
    vector<vector<Point>> contours;
    findContours(edges, contours, RETR_TREE, CHAIN_APPROX_SIMPLE);

    // Tesseract 초기화
    tesseract::TessBaseAPI tess;
    if (tess.Init(nullptr, "eng")) {
        throw runtime_error("Could not initialize tesseract.");
    }

    // 번호판 후보 영역 찾기
    for (const auto& contour : contours) {
        // 윤곽선의 외곽 사각형 그리기
        Rect rect = boundingRect(contour);
        double aspectRatio = static_cast<double>(rect.width) / rect.height;
        if (aspectRatio > 2 && aspectRatio < 5) {  // 번호판 비율 조건 (적절하게 조정 가능)
            Mat plate = image(rect);

            // OCR을 사용해 번호판 텍스트 추출
            tess.SetImage(plate.data, plate.cols, plate.rows, 3, plate.step);
            string plateText = tess.GetUTF8Text();
            if (!plateText.empty()) {  // 텍스트가 있는 경우
                cout << "Detected license plate: " << plateText << endl;
                // 번호판 영역 표시
                rectangle(image, rect, Scalar(0, 255, 0), 2);
                putText(image, plateText, Point(rect.x, rect.y - 10), FONT_HERSHEY_SIMPLEX, 0.9, Scalar(0, 255, 0), 2);
            }
        }
    }

    // 결과 이미지 출력
    imshow("Detected License Plates", image);
    waitKey(0);
    destroyAllWindows();
}

int main() {
    // 이미지 파일 경로
    string imagePath = "C:\\Users\\jaeho\\Desktop\\workspace\\Ros\\data\\test.png";

    // 파일 경로 확인
    ifstream ifs(imagePath);
    if (!ifs) {
        cerr << "Image file not found at the specified path: " << imagePath << endl;
        return 1;
    }

    try {
        detectPlate(imagePath);
    } catch (const exception& ex) {
        cerr << "Error: " << ex.what() << endl;
    }

    return 0;
}
