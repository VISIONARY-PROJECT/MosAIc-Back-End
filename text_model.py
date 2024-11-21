#basic code
import pytesseract
import cv2
from transformers import BartTokenizer, BartForConditionalGeneration

def simple(path):
    image = cv2.imread(path)
    
    #OCR
    text = pytesseract.image_to_string(image, lang = 'kor+eng')

    #result
    print(text)

    return text

# 텍스트 요약
def summarize_text(img_src):

    # BART 모델 로드
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

    text = simple(img_src)

    # 텍스트를 토큰화
    inputs = tokenizer.encode(text, return_tensors='pt', max_length=1024, truncation=True)
    
    # 요약 생성
    summary_ids = model.generate(inputs, max_length=150, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
    
    # 요약 결과 디코딩
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary