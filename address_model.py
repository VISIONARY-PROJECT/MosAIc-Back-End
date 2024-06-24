import cv2
import numpy as np
import pytesseract
import uuid

def detect_address(img):
    # Tesseract 경로 설정 (경로에 맞게 수정)

    # 이미지 로드
    img_file = cv2.imread(img)

    # 그레이스케일로 변환
    gray = cv2.cvtColor(img_file, cv2.COLOR_BGR2GRAY)

    # Tesseract를 사용하여 글자 영역 인식
    detection_data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)

    # 모든 박스를 그릴 원본 이미지 복사본
    all_boxes_img = img_file.copy()

    # 각 사각형의 좌표와 크기를 저장할 리스트
    boxes = []

    # 모든 인식된 박스 그리기
    n_boxes = len(detection_data['level'])
    for i in range(n_boxes):
        if detection_data['text'][i].strip() != '':
            (x, y, w, h) = (detection_data['left'][i], detection_data['top'][i], detection_data['width'][i], detection_data['height'][i])
            boxes.append((x, y, x + w, y + h))
            cv2.rectangle(all_boxes_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # 박스 처리된 이미지 생성
    boxed_img = img_file.copy()
    n_boxes = len(detection_data['level'])
    for i in range(n_boxes):
        if detection_data['text'][i] is not None:
            (x, y, w, h) = (detection_data['left'][i], detection_data['top'][i], detection_data['width'][i], detection_data['height'][i])

            # 인식된 박스 그리기
            cv2.rectangle(boxed_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # 큰 사각형이 포함하는 작은 사각형을 확인하여 필요 없는 큰 사각형 제거
    keep_boxes = []
    for i in range(len(boxes)):
        (x_i1, y_i1, x_i2, y_i2) = boxes[i]
        is_contained = False
        for j in range(len(boxes)):
            if i != j:
                (x_j1, y_j1, x_j2, y_j2) = boxes[j]
                # 사각형 i가 사각형 j에 포함되는지 확인
                if x_i1 >= x_j1 and y_i1 >= y_j1 and x_i2 <= x_j2 and y_i2 <= y_j2:
                    is_contained = True
                    break
        # 포함되지 않는 경우에만 리스트에 추가
        if not is_contained:
            keep_boxes.append(boxes[i])

    # 줄어든 박스를 그린 이미지
    reduced_boxes_img = img_file.copy()
    for (x1, y1, x2, y2) in keep_boxes:
        cv2.rectangle(reduced_boxes_img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # 모자이크 처리된 최종 이미지 생성
    mosaic_img = img_file.copy()
    for (x1, y1, x2, y2) in keep_boxes:
        roi = mosaic_img[y1:y2, x1:x2]
        roi = cv2.resize(roi, (int((x2 - x1) / 17), int((y2 - y1) / 17)), interpolation=cv2.INTER_LINEAR)
        roi = cv2.resize(roi, (x2 - x1, y2 - y1), interpolation=cv2.INTER_NEAREST)
        mosaic_img[y1:y2, x1:x2] = roi

    # 모자이크 처리된 이미지를 파일로 저장
    id = str(uuid.uuid4())[:12]
    cv2.imwrite("static/img/{}.jpeg".format(id), mosaic_img)
    return id