import cv2
import pytesseract
from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont


yolo_model = YOLO(r"c:\Users\jaeho\Downloads\Automatic-License-Plate-Recognition-using-YOLOv8-main\Automatic-License-Plate-Recognition-using-YOLOv8-main\license_plate_detector.pt")  


image_path = r"c:\Users\jaeho\Downloads\1000002373.jpg"
image = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# YOLO 모델을 사용해 번호판 검출
results = yolo_model(image_rgb)

# PIL 이미지로 변환
image_pil = Image.fromarray(image_rgb)
draw = ImageDraw.Draw(image_pil)

# YOLO 결과를 순회하며 번호판 영역 추출 및 OCR 수행
for result in results:
    boxes = result.boxes
    for box in boxes:
        # 클래스가 번호판인 경우에만 처리 (클래스 ID는 모델에 따라 다를 수 있음)
        if int(box.cls) == 0:  # 번호판 클래스 ID를 확인하고 수정해야 합니다
            x_min, y_min, x_max, y_max = map(int, box.xyxy[0])

            # 번호판 영역 이미지 추출
            license_plate_img = image_rgb[y_min:y_max, x_min:x_max]

            # 이미지 전처리 (OCR 정확도 향상을 위해)
            gray = cv2.cvtColor(license_plate_img, cv2.COLOR_RGB2GRAY)
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

            # OCR을 사용해 텍스트 추출
            plate_text = pytesseract.image_to_string(thresh, config='--psm 8 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            plate_text = plate_text.strip()  # 불필요한 공백 제거

            print(f"Detected license plate: {plate_text}")

            # 검출된 번호판 영역에 사각형 그리기
            draw.rectangle([x_min, y_min, x_max, y_max], outline="green", width=2)
            # 검출된 텍스트 추가
            draw.text((x_min, y_min - 20), plate_text, fill="green", font=ImageFont.truetype("arial", 15))

# 결과 이미지 표시
image_pil.show()