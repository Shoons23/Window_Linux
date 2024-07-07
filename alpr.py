from openalpr import Alpr
import cv2

def process_image(image_path):
    # OpenALPR 객체 초기화
    alpr = Alpr("us", "/path/to/openalpr.conf", "/path/to/runtime_data")
    if not alpr.is_loaded():
        print("Error loading OpenALPR")
        return
    
    alpr.set_top_n(5)
    alpr.set_default_region("md")

    # 이미지 읽기
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Unable to read image from {image_path}")
        return

    # 원본 이미지 복사
    result_img = img.copy()

    # OpenALPR로 라이센스 플레이트 인식
    results = alpr.recognize_file(image_path)

    for plate in results['results']:
        # 감지된 플레이트의 좌표
        x1, y1 = plate['coordinates'][0]['x'], plate['coordinates'][0]['y']
        x2, y2 = plate['coordinates'][2]['x'], plate['coordinates'][2]['y']
        
        # 감지된 영역에 사각형 그리기
        cv2.rectangle(result_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # 인식된 텍스트
        text = plate['plate']
        confidence = plate['confidence']
        print(f"Detected license plate: {text} (Confidence: {confidence:.2f}%)")
        
        # 인식된 텍스트를 이미지에 추가
        cv2.putText(result_img, text, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

    # 결과 이미지 저장
    output_path = 'result_license_plate.jpg'
    cv2.imwrite(output_path, result_img)
    print(f"Result image saved as {output_path}")

    # OpenALPR 객체 해제
    alpr.unload()

if __name__ == "__main__":
    # 이미지 파일 경로 지정
    image_path = r"c:\Users\jaeho\Downloads\1000002373.jpg"  # 여기에 실제 이미지 파일 경로를 입력하세요
    process_image(image_path)