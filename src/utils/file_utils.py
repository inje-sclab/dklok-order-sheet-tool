import os
import json
import datetime
from typing import Dict, Any


def is_pdf_file(file_path: str) -> bool:
    """파일이 PDF인지 확인"""
    return file_path.lower().endswith('.pdf')


def is_image_file(file_path: str) -> bool:
    """파일이 이미지인지 확인"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif'}
    _, ext = os.path.splitext(file_path.lower())
    return ext in image_extensions


def save_json_result(data: Dict[str, Any], original_file_path: str) -> str:
    """OCR 결과를 JSON 파일로 저장"""
    # 파일 이름 생성 (원본 문서 이름 + 타임스탬프)
    doc_name = os.path.basename(original_file_path).split('.')[0]
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{doc_name}_ocr_{timestamp}.json"
    
    # JSON 파일로 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return output_file


def load_json_result(file_path: str) -> Dict[str, Any]:
    """JSON 파일에서 OCR 결과 불러오기"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_file_size_mb(file_path: str) -> float:
    """파일 크기를 MB 단위로 반환"""
    size_bytes = os.path.getsize(file_path)
    return size_bytes / (1024 * 1024)


def ensure_directory_exists(dir_path: str) -> None:
    """디렉토리가 존재하지 않으면 생성"""
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)