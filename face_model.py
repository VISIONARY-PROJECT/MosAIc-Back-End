import numpy as np
import cv2
import uuid
def blur_with_feathering(image, x, y, w, h, ksize=15, fade_width=5):
    if w > 0 and h > 0:
        # 블러 처리할 ROI 추출
        roi = image[y:y+h, x:x+w]
        
        # ROI에 대해 가우시안 블러 적용
        blurred_roi = cv2.GaussianBlur(roi, (ksize, ksize), 0)
        
        # 원본과 블러 처리된 이미지를 위한 마스크 생성
        mask = np.zeros((h, w, 3), dtype=np.uint8)
        cv2.rectangle(mask, (fade_width, fade_width), (w-fade_width, h-fade_width), (255, 255, 255), thickness=-1)
        
        # 가우시안 블러로 마스크의 경계 부분을 부드럽게 만들기
        mask = cv2.GaussianBlur(mask, (ksize, ksize), 0)
        
        # 알파 블렌딩을 위한 알파 마스크 계산
        alpha_mask = mask.astype(float) / 255
        
        # 알파 블렌딩을 통해 블러 처리된 이미지와 원본 이미지 합성
        for c in range(0, 3):
            roi[:, :, c] = roi[:, :, c] * (1 - alpha_mask[:, :, c]) + blurred_roi[:, :, c] * alpha_mask[:, :, c]
        
        # 블렌딩된 이미지를 원본 이미지에 적용
        image[y:y+h, x:x+w] = roi


def detect_face(img):
    frontal_face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    profile_face_cascade = cv2.CascadeClassifier("haarcascade_profileface.xml")
    eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
    eyetree_cascade = cv2.CascadeClassifier("haarcascade_eye_tree_eyeglasses.xml")

    image = cv2.imread(img) #이미지 불러오기
    image_gs = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #이미지 그레이스케일로 처리하기

    frontal_faces = frontal_face_cascade.detectMultiScale(image_gs, 1.1, 4)
    print("정면 얼굴 감지된 사람:", str(len(frontal_faces)))

    profile_faces = profile_face_cascade.detectMultiScale(image_gs, 1.1, 4)
    print("옆면 얼굴 감지된 사람:", str(len(profile_faces)))

    eye = eye_cascade.detectMultiScale(image_gs, 1.2, 4)
    print("눈 감지된 사람:", str(len(eye)))

    eyetree = eye_cascade.detectMultiScale(image_gs, 1.2, 4)
    print("눈(안경에 가려진것도 포함) 감지된 사람:", str(len(eyetree)))

    ksize = 25
    fade_width = 5

    total = []

    total.extend(frontal_faces)
    total.extend(profile_faces)
    total.extend(eye)
    total.extend(eyetree)

    if len(total) > 0:
        for (x, y, w, h) in total:
            blur_with_feathering(image, x, y, w, h, ksize=ksize, fade_width=fade_width)
        id = str(uuid.uuid4())[:12]
        cv2.imwrite("static/img/{}.jpeg".format(id),image)
        return id
    else:
        print("No face detected")
        return None
    
        