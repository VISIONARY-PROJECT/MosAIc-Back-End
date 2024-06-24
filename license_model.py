import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import uuid

def detect_license(img):

    # 모델 로드
    model = tf.keras.models.load_model('my_mnist_model.h5')

    # 이미지 로드 및 전처리
    img_file = cv2.imread(img)  # 이미지 경로에 맞게 수정

    height, width, _ = img_file.shape

    gray = cv2.cvtColor(img_file, cv2.COLOR_BGR2GRAY)

    img_blurred = cv2.GaussianBlur(gray, ksize=(5, 5), sigmaX=0)
    img_blur_thresh = cv2.adaptiveThreshold(
        img_blurred,
        maxValue=255.0,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv2.THRESH_BINARY_INV,
        blockSize=55,
        C=7
    )

    contours, _ = cv2.findContours(
        img_blur_thresh,
        mode=cv2.RETR_LIST,
        method=cv2.CHAIN_APPROX_SIMPLE
    )

    temp_result_with_boxes = img_file.copy()

    # 작은 사각형만 남기는 함수
    def filter_contours(contours):
        filtered_contours = []
        for i, contour in enumerate(contours):
            x, y, w, h = cv2.boundingRect(contour)
            is_small_contour = True
            for j, other_contour in enumerate(contours):
                if i != j:
                    x_other, y_other, w_other, h_other = cv2.boundingRect(other_contour)
                    if x <= x_other and y <= y_other and x + w >= x_other + w_other and y + h >= y_other + h_other:
                        is_small_contour = False
                        break
            if is_small_contour:
                filtered_contours.append(contour)
        return filtered_contours

    # 숫자 예측 및 처리
    filtered_contours = filter_contours(contours)
    for contour in filtered_contours:
        x, y, w, h = cv2.boundingRect(contour)
        digit_roi = gray[y:y+h, x:x+w]  # contour에서 roi 추출

        # 모델 입력 형식에 맞게 조정 (차원 확장 및 정규화)
        digit_roi_for_predict = cv2.resize(digit_roi, (28, 28))  # MNIST 이미지 크기에 맞게 리사이즈
        digit_roi_for_predict = digit_roi_for_predict.astype('float32') / 255.0  # 0~1 사이 값으로 정규화
        digit_roi_for_predict = np.expand_dims(digit_roi_for_predict, axis=-1)  # 채널 차원 추가
        digit_roi_for_predict = np.expand_dims(digit_roi_for_predict, axis=0)   # 배치 차원 추가

        # 모델 예측
        prediction = model.predict(digit_roi_for_predict)
        predicted_class = np.argmax(prediction)

        # 모자이크 크기 설정 (조정)
        mosaic_scale = 0.05  # 모자이크 크기를 박스 크기보다 작게 설정
        mosaic_size = (max(1, int(w * mosaic_scale)), max(1, int(h * mosaic_scale)))  # 모자이크 크기 계산, 최소 크기를 1로 설정

        # 모자이크 처리: 작은 크기로 줄였다가 다시 원래 크기로 확대
        digit_roi_mosaic = cv2.resize(digit_roi, mosaic_size, interpolation=cv2.INTER_AREA)
        digit_roi_mosaic = cv2.resize(digit_roi_mosaic, (w, h), interpolation=cv2.INTER_NEAREST)

        # 모자이크 처리된 숫자 영역을 원본 이미지에 적용
        img_file[y:y+h, x:x+w] = cv2.cvtColor(digit_roi_mosaic, cv2.COLOR_GRAY2BGR)

        # 박스 그리기
        cv2.rectangle(temp_result_with_boxes, pt1=(x, y), pt2=(x+w, y+h), color=(0, 255, 0), thickness=2)

        # 예측 결과 표시
        cv2.putText(temp_result_with_boxes, str(predicted_class), (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 최종 이미지 저장
    id = str(uuid.uuid4())[:12]
    cv2.imwrite("static/img/{}.jpeg".format(id), img_file)
    return id
