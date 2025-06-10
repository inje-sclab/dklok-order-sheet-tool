import pytest
from src.models.order_item import OrderItem
from src.models.document import ProcessedDocument, DocumentPage


def test_order_item_creation():
    """OrderItem 생성 테스트"""
    item = OrderItem("ABC-123", 10)
    assert item.product_code == "ABC-123"
    assert item.quantity == 10


def test_order_item_string_quantity():
    """문자열 수량 자동 변환 테스트"""
    item = OrderItem("ABC-123", "15")
    assert item.quantity == 15


def test_order_item_from_dict():
    """딕셔너리에서 OrderItem 생성 테스트"""
    data = {"품번": "TEST-001", "수량": 5}
    item = OrderItem.from_dict(data)
    assert item.product_code == "TEST-001"
    assert item.quantity == 5


def test_order_item_to_dict():
    """OrderItem을 딕셔너리로 변환 테스트"""
    item = OrderItem("TEST-002", 20)
    result = item.to_dict()
    expected = {"품번": "TEST-002", "수량": 20}
    assert result == expected


def test_processed_document():
    """ProcessedDocument 테스트"""
    items = [OrderItem("PART-A", 10), OrderItem("PART-B", 5)]
    page = DocumentPage(1, items, {})
    
    doc = ProcessedDocument(
        filename="test.pdf",
        document_type="PDF",
        total_pages=1,
        pages=[page],
        processing_cost=0.01
    )
    
    assert doc.total_items == 2
    assert len(doc.all_items) == 2
    assert doc.all_items[0].product_code == "PART-A"