#include <alpr.h>
#include <iostream>
#include <string>

int main(int argc, char* argv[]) {
    // OpenALPR 객체 생성
    alpr::Alpr openalpr("us", "c:\\Users\\jaeho\\Downloads\\openalpr-master\\openalpr-master\\config\\openalpr.conf");

    // OpenALPR 라이브러리 로드 여부 확인
    if (!openalpr.isLoaded()) {
        std::cerr << "Error loading OpenALPR" << std::endl;
        return 1;
    }

    // 인식 결과 상위 20개 설정
    openalpr.setTopN(20);
    // 기본 지역 설정
    openalpr.setDefaultRegion("kr");

    // 이미지 파일에서 번호판 인식
    std::string imagePath = "c:\\Users\\jaeho\\Downloads\\1000002375.jpg";
    alpr::AlprResults results = openalpr.recognize(imagePath);

    // 인식된 번호판 출력
    if (results.plates.size() > 0) {
        std::cout << "License Plate: " << results.plates[0].bestPlate.characters << std::endl;
    } else {
        std::cout << "No license plate detected" << std::endl;
    }

    // OpenALPR 종료
    openalpr.unload();
    return 0;
}
