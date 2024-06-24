import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from tensorflow.keras import layers, models

# CNN 모델 정의
def create_cnn_model():
    model = models.Sequential([
        # 첫 번째 Convolutional Layer
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        layers.MaxPooling2D((2, 2)),
        # 두 번째 Convolutional Layer
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        # 완전 연결 계층 (Fully Connected Layer)
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(10, activation='softmax')  # 출력층, 분류 문제라면 클래스 수에 맞춰 변경
    ])
    return model

# 모델 생성
model = create_cnn_model()

# 모델 구조 출력
model.summary()



# MNIST 데이터셋 로드 및 전처리
(train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()
train_images = train_images.reshape((60000, 28, 28, 1))
train_images = train_images.astype('float32') / 255

test_images = test_images.reshape((10000, 28, 28, 1))
test_images = test_images.astype('float32') / 255

# 모델 생성 및 컴파일
model = create_cnn_model()
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# 모델 학습
model.fit(train_images, train_labels, epochs=5, batch_size=64, validation_data=(test_images, test_labels))


model.save('my_mnist_model.h5')
