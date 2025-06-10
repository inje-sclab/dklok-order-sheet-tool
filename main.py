#!/usr/bin/env python3
"""
주문서 OCR 처리 도구
리팩토링된 메인 진입점
"""
import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.gui.main_window import MainWindow
from src.core.document_processor import DocumentProcessor
from src.utils.file_utils import save_json_result
from src.config.settings import app_settings


def main_cli(file_path: str = None):
    """CLI 모드 실행"""
    if not file_path:
        file_path = "./data/주문서 (미국).pdf"
    
    print(f"문서 처리 시작: {file_path}")
    
    # API 키 확인 (모킹 모드가 아닌 경우)
    if not app_settings.mock_mode and not app_settings.api_key:
        print("오류: OpenAI API 키가 설정되지 않았습니다.")
        print("설정에서 API 키를 입력하거나 모킹 모드를 활성화해주세요.")
        return
    
    try:
        # 문서 처리
        processor = DocumentProcessor()
        document = processor.process_document(file_path)
        
        # 결과 저장
        output_file = save_json_result(document.to_dict(), file_path)
        
        print(f"\n결과가 다음 파일에 저장되었습니다: {output_file}")
        print(f"추출된 항목 수: {document.total_items}")
        print(f"추정 API 비용: {app_settings.format_cost(document.processing_cost)}")
        
        # 추출된 항목 출력
        if document.total_items > 0:
            print("\n추출된 항목:")
            for i, item in enumerate(document.all_items, 1):
                print(f"{i:2d}. {item.product_code}: {item.quantity}개")
        
    except Exception as e:
        print(f"오류 발생: {e}")


def main_gui():
    """GUI 모드 실행"""
    # QApplication 생성 전에 High DPI 설정
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    
    # PDF 처리 라이브러리 상태 확인
    try:
        from src.utils.pdf_converter import PDFConverter
        converter = PDFConverter()
        print(f"PDF 처리 라이브러리: {converter.available_backend}")
    except Exception as e:
        print(f"경고: PDF 처리 라이브러리 확인 실패: {e}")
        print("PyMuPDF 설치 권장: pip install PyMuPDF")

    # 메인 윈도우 생성 및 표시
    window = MainWindow()
    window.show()
    
    # 애플리케이션 실행
    sys.exit(app.exec_())


def main():
    """메인 함수"""
    # 명령줄 인자 확인
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        # CLI 모드
        file_path = sys.argv[2] if len(sys.argv) > 2 else None
        main_cli(file_path)
    else:
        # GUI 모드
        main_gui()


if __name__ == "__main__":
    main()