import pytest
from src.core.ocr_service import MockOCRService, OCRService
from src.models.order_item import OrderItem


def test_mock_ocr_service():
    """모킹 OCR 서비스 테스트"""
    service = MockOCRService()
    items, cost = service.process_image("dummy_path.jpg")
    
    assert len(items) > 0
    assert cost > 0
    assert isinstance(items[0], OrderItem)


def test_ocr_service_factory():
    """OCR 서비스 팩토리 테스트"""
    service = OCRService()
    assert service.service is not None
    
    # 모킹 모드이므로 MockOCRService여야 함
    assert isinstance(service.service, MockOCRService)