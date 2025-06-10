from dataclasses import dataclass
from typing import Union


@dataclass
class OrderItem:
    """주문 항목 데이터 모델"""
    product_code: str  # 품번
    quantity: int      # 수량
    
    def __post_init__(self):
        if isinstance(self.quantity, str):
            try:
                self.quantity = int(self.quantity)
            except ValueError:
                self.quantity = 0
    
    def to_dict(self) -> dict:
        """딕셔너리로 변환"""
        return {
            "품번": self.product_code,
            "수량": self.quantity
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "OrderItem":
        """딕셔너리에서 생성"""
        return cls(
            product_code=data.get("품번", ""),
            quantity=data.get("수량", 0)
        )