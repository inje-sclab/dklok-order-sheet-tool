import os
import tempfile
from typing import List, Callable, Optional
from ..models.document import ProcessedDocument, DocumentPage
from ..models.order_item import OrderItem
from ..utils.pdf_converter import PDFConverter
from ..utils.file_utils import is_pdf_file
from .ocr_service import OCRService


class DocumentProcessor:
    """문서 처리 메인 클래스"""
    
    def __init__(self):
        self.ocr_service = OCRService()
        self.pdf_converter = PDFConverter()
    
    def process_document(
        self, 
        file_path: str, 
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> ProcessedDocument:
        """문서 처리 메인 메서드"""
        
        if is_pdf_file(file_path):
            return self._process_pdf(file_path, progress_callback)
        else:
            return self._process_image(file_path, progress_callback)
    
    def _process_pdf(
        self, 
        pdf_path: str, 
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> ProcessedDocument:
        """PDF 파일 처리"""
        print(f"PDF 파일 처리 중: {pdf_path}")
        
        temp_dir = tempfile.mkdtemp()
        total_cost = 0.0
        
        try:
            # PDF를 이미지로 변환
            image_paths, num_pages = self.pdf_converter.convert_to_images(pdf_path, temp_dir)
            print(f"PDF를 {num_pages}개 페이지로 변환 완료")
            
            pages = []
            
            # 각 페이지 처리
            for i, img_path in enumerate(image_paths):
                page_num = i + 1
                print(f"페이지 {page_num}/{num_pages} 처리 중...")
                
                if progress_callback:
                    progress_callback(page_num, num_pages)
                
                # OCR 처리
                items, page_cost = self.ocr_service.process_image(img_path)
                total_cost += page_cost
                
                # 페이지 데이터 생성
                page = DocumentPage(
                    page_number=page_num,
                    items=items,
                    raw_content={"processed_items": len(items)}
                )
                pages.append(page)
                
                # 임시 이미지 파일 삭제
                if os.path.exists(img_path):
                    os.remove(img_path)
            
            # 문서 결과 생성
            document = ProcessedDocument(
                filename=os.path.basename(pdf_path),
                document_type="PDF",
                total_pages=num_pages,
                pages=pages,
                processing_cost=total_cost
            )
            
            return document
            
        finally:
            # 임시 디렉토리 정리
            try:
                if os.path.exists(temp_dir):
                    os.rmdir(temp_dir)
            except OSError:
                pass
    
    def _process_image(
        self, 
        image_path: str, 
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> ProcessedDocument:
        """이미지 파일 처리"""
        print(f"이미지 파일 처리 중: {image_path}")
        
        if progress_callback:
            progress_callback(1, 1)
        
        # OCR 처리
        items, cost = self.ocr_service.process_image(image_path)
        
        # 페이지 데이터 생성
        page = DocumentPage(
            page_number=1,
            items=items,
            raw_content={"processed_items": len(items)}
        )
        
        # 문서 결과 생성
        document = ProcessedDocument(
            filename=os.path.basename(image_path),
            document_type="Image",
            total_pages=1,
            pages=[page],
            processing_cost=cost
        )
        
        return document