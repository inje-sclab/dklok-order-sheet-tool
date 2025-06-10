import os
from PyQt5.QtCore import QSettings
from typing import Optional


class AppSettings:
    """애플리케이션 설정 관리"""
    
    def __init__(self):
        self.settings = QSettings("OCR App", "GPT OCR Converter")
        self._api_key: Optional[str] = None
        self._model_name: str = "gpt-4o-mini"
        self._input_cost: float = 0.10
        self._output_cost: float = 0.40
        self._exchange_rate: float = 1399.0
        self._mock_mode: bool = True
        
        self.load_settings()
    
    def load_settings(self):
        """설정 파일에서 설정 불러오기"""
        self._api_key = self.settings.value("api_key", "")
        self._model_name = self.settings.value("model", "gpt-4o-mini")
        self._input_cost = float(self.settings.value("input_cost", "0.10"))
        self._output_cost = float(self.settings.value("output_cost", "0.40"))
        self._exchange_rate = float(self.settings.value("exchange_rate", "1399"))
        self._mock_mode = self.settings.value("mock_mode", "true").lower() == "true"
    
    def save_settings(self):
        """설정을 파일에 저장"""
        self.settings.setValue("api_key", self._api_key or "")
        self.settings.setValue("model", self._model_name)
        self.settings.setValue("input_cost", self._input_cost)
        self.settings.setValue("output_cost", self._output_cost)
        self.settings.setValue("exchange_rate", self._exchange_rate)
        self.settings.setValue("mock_mode", str(self._mock_mode).lower())
        self.settings.sync()
    
    @property
    def api_key(self) -> Optional[str]:
        return self._api_key
    
    @api_key.setter
    def api_key(self, value: str):
        self._api_key = value
    
    @property
    def model_name(self) -> str:
        return self._model_name
    
    @model_name.setter
    def model_name(self, value: str):
        self._model_name = value
    
    @property
    def input_cost_per_million(self) -> float:
        return self._input_cost
    
    @input_cost_per_million.setter
    def input_cost_per_million(self, value: float):
        self._input_cost = value
    
    @property
    def output_cost_per_million(self) -> float:
        return self._output_cost
    
    @output_cost_per_million.setter
    def output_cost_per_million(self, value: float):
        self._output_cost = value
    
    @property
    def exchange_rate(self) -> float:
        return self._exchange_rate
    
    @exchange_rate.setter
    def exchange_rate(self, value: float):
        self._exchange_rate = value
    
    @property
    def mock_mode(self) -> bool:
        """개발용 모킹 모드 여부"""
        return self._mock_mode
    
    @mock_mode.setter
    def mock_mode(self, value: bool):
        self._mock_mode = value
    
    def calculate_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        """토큰 사용량에 따른 API 비용 계산"""
        input_cost = (prompt_tokens / 1000000.0) * self._input_cost
        output_cost = (completion_tokens / 1000000.0) * self._output_cost
        return input_cost + output_cost
    
    def format_cost(self, cost_usd: float) -> str:
        """비용을 USD와 KRW로 형식화"""
        cost_krw = cost_usd * self._exchange_rate
        return f"${cost_usd:.4f} (₩{int(cost_krw):,})"


# 전역 설정 인스턴스
app_settings = AppSettings()