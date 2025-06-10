from dataclasses import dataclass
from typing import List, Dict, Any
from .order_item import OrderItem


@dataclass
class DocumentPage:
    """문서 페이지 데이터 모델"""
    page_number: int
    items: List[OrderItem]
    raw_content: Dict[str, Any]
    
    def to_dict(self) -> dict:
        """딕셔너리로 변환"""
        return {
            "page": self.page_number,
            "content": [item.to_dict() for item in self.items],
            "raw_content": self.raw_content
        }


@dataclass
class ProcessedDocument:
    """처리된 문서 데이터 모델"""
    filename: str
    document_type: str  # "PDF" or "Image"
    total_pages: int
    pages: List[DocumentPage]
    processing_cost: float = 0.0
    
    @property
    def total_items(self) -> int:
        """전체 아이템 수"""
        return sum(len(page.items) for page in self.pages)
    
    @property
    def all_items(self) -> List[OrderItem]:
        """모든 페이지의 아이템들을 하나의 리스트로"""
        items = []
        for page in self.pages:
            items.extend(page.items)
        return items
    
    def to_dict(self) -> dict:
        """딕셔너리로 변환"""
        return {
            "document_type": self.document_type,
            "total_pages": self.total_pages,
            "filename": self.filename,
            "pages": [page.to_dict() for page in self.pages],
            "processing_cost": self.processing_cost
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ProcessedDocument":
        """딕셔너리에서 생성"""
        pages = []
        for page_data in data.get("pages", []):
            items = []
            content = page_data.get("content", [])
            
            if isinstance(content, list):
                for item_data in content:
                    if isinstance(item_data, dict) and "품번" in item_data:
                        items.append(OrderItem.from_dict(item_data))
            
            pages.append(DocumentPage(
                page_number=page_data.get("page", 1),
                items=items,
                raw_content=page_data.get("raw_content", {})
            ))
        
        return cls(
            filename=data.get("filename", ""),
            document_type=data.get("document_type", "Image"),
            total_pages=data.get("total_pages", 1),
            pages=pages,
            processing_cost=data.get("processing_cost", 0.0)
        )