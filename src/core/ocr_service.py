import json
import random
import time
from typing import List, Tuple
from ..models.order_item import OrderItem
from ..config.settings import app_settings


class MockOCRService:
    """개발용 모킹 OCR 서비스"""
    
    MOCK_RESPONSES = [
        [
            {"품번": "DMCA-4N-SA", "수량": 22},
            {"품번": "DMCA-8N-SA", "수량": 7},
            {"품번": "DMCA-12N-SA", "수량": 15},
        ],
        [
            {"품번": "PART-001", "수량": 10},
            {"품번": "PART-002", "수량": 5},
        ],
        [
            {"품번": "ABC-123", "수량": 30},
            {"품번": "XYZ-456", "수량": 12},
            {"품번": "DEF-789", "수량": 8},
            {"품번": "GHI-012", "수량": 25},
        ]
    ]
    
    def process_image(self, image_path: str) -> Tuple[List[OrderItem], float]:
        """이미지에서 OCR 처리 (모킹)"""
        # 개발용 지연 시뮬레이션
        time.sleep(random.uniform(0.5, 1.5))
        
        # 랜덤한 응답 선택
        mock_data = random.choice(self.MOCK_RESPONSES)
        
        # OrderItem 리스트로 변환
        items = [OrderItem.from_dict(item_data) for item_data in mock_data]
        
        # 모킹 비용 (실제 API 비용과 유사하게)
        mock_cost = random.uniform(0.001, 0.01)
        
        print(f"[MOCK] 이미지 처리 완료: {len(items)}개 항목 추출, 비용: ${mock_cost:.4f}")
        
        return items, mock_cost


class RealOCRService:
    """실제 OpenAI API를 사용하는 OCR 서비스"""
    
    def __init__(self):
        self.api_url = "https://api.openai.com/v1/chat/completions"
    
    def process_image(self, image_path: str) -> Tuple[List[OrderItem], float]:
        """이미지에서 OCR 처리 (실제 API)"""
        if not app_settings.api_key:
            raise ValueError("OpenAI API 키가 설정되지 않았습니다.")
        
        # 실제 API 호출 로직은 기존 코드 참조
        # 여기서는 간단한 구현만 제공
        raise NotImplementedError("실제 API 연동은 추후 구현")


class OCRService:
    """OCR 서비스 팩토리"""
    
    def __init__(self):
        # 모킹 모드이거나 API 키가 없으면 모킹 서비스 사용
        if app_settings.mock_mode or not app_settings.api_key:
            self.service = MockOCRService()
            print("[OCR Service] 모킹 모드로 실행 중")
        else:
            self.service = RealOCRService()
            print("[OCR Service] 실제 API 모드로 실행 중")
    
    def process_image(self, image_path: str) -> Tuple[List[OrderItem], float]:
        """이미지 OCR 처리"""
        return self.service.process_image(image_path)