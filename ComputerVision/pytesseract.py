import cv2
import pytesseract
from pytesseract import Output
import os
from PIL import Image

# Tesseract OCR 실행 파일 경로 설정
# pytesseract.pytesseract.tesseract_cmd = r'c:\Users\jaeho\Downloads\tesseract-ocr-w64-setup-5.4.0.20240606.exe'

def preprocess_image(image_path):
    # 이미지 읽기
    print(f"Reading image from: {image_path}")
    image = cv2.imread(image_path)
    
    if image is None:
        raise FileNotFoundError(f"Image file not found at the specified path: {image_path}")

    # 이미지를 회색조로 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 블러링을 통해 노이즈 제거
    gray = cv2.medianBlur(gray, 5)

    # 경계선 감지
    edges = cv2.Canny(gray, 100, 200)

    return edges, image

def detect_plate(image_path):
    edges, image = preprocess_image(image_path)

    # 컨투어(윤곽선) 찾기
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 번호판 후보 영역 찾기
    for contour in contours:
        # 윤곽선의 외곽 사각형 그리기
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / h
        if 2 < aspect_ratio < 5:  # 번호판 비율 조건 (적절하게 조정 가능)
            plate = image[y:y+h, x:x+w]

            # OCR을 사용해 번호판 텍스트 추출
            plate_text = pytesseract.image_to_string(plate, config='--psm 8 -l kor')
            if plate_text.strip():  # 텍스트가 있는 경우
                print(f"Detected license plate: {plate_text.strip()}")
                # 번호판 영역 표시
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(image, plate_text.strip(), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # 결과 이미지 저장
    result_image_path = r'c:\Users\jaeho\Downloads\result_image.jpg'
    cv2.imwrite(result_image_path, image)

    # PIL을 사용하여 이미지 표시
    img = Image.open(result_image_path)
    img.show()

# 이미지 파일 경로
image_path = r'c:\Users\jaeho\Downloads\1000002372.jpg'

# 파일 경로 확인
if not os.path.isfile(image_path):
    raise FileNotFoundError(f"Image file not found at the specified path: {image_path}")

detect_plate(image_path)
