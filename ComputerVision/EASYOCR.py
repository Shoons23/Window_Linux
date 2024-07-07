import easyocr
from PIL import Image, ImageDraw, ImageFont

# OCR 객체 생성
reader = easyocr.Reader(['ko'])

# 이미지 파일 경로
image_path = r'c:\Users\jaeho\Downloads\1000002373.jpg'

# 이미지 읽기
image = Image.open(image_path)
draw = ImageDraw.Draw(image)

# 이미지에서 텍스트 추출
result = reader.readtext(image_path)

# 추출된 텍스트 출력 및 이미지에 표시
for detection in result:
    bbox = detection[0]  # 텍스트 박스 좌표
    text = detection[1]  # 인식된 텍스트

    # 텍스트가 인식된 영역에 사각형 그리기
    x_min, y_min = bbox[0][0], bbox[0][1]
    x_max, y_max = bbox[1][0], bbox[1][1]
    draw.rectangle([x_min, y_min, x_max, y_max], outline="green", width=2)

    # 텍스트 출력
    font = ImageFont.truetype("arial.ttf", size=24)  # 폰트와 사이즈 설정
    draw.text((x_min, y_min - 30), text, font=font, fill="green")

    # 추출된 텍스트와 위치 정보 출력
    print(f"Detected text: {text}, Bounding box: {bbox}")

# 이미지 출력
image.show()
