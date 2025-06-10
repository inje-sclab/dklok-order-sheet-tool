import os
import tempfile
from typing import Tuple, List

# PDF 처리를 위한 대안 라이브러리들
try:
    from pdf2image import convert_from_path
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False


class PDFConverter:
    """PDF를 이미지로 변환하는 클래스"""
    
    def __init__(self):
        self.available_backend = self._check_available_backend()
        if not self.available_backend:
            raise RuntimeError(
                "PDF 처리를 위한 라이브러리가 설치되지 않았습니다.\n"
                "다음 중 하나를 설치해주세요:\n"
                "1. PyMuPDF (권장): pip install PyMuPDF\n"
                "2. pdf2image + Poppler: pip install pdf2image + Poppler 설치"
            )
    
    def _check_available_backend(self) -> str:
        """사용 가능한 PDF 처리 백엔드 확인"""
        if PYMUPDF_AVAILABLE:
            return "pymupdf"
        elif PDF2IMAGE_AVAILABLE:
            return "pdf2image"
        else:
            return ""
    
    def convert_to_images(self, pdf_path: str, output_folder: str = None) -> Tuple[List[str], int]:
        """PDF를 이미지로 변환"""
        if output_folder is None:
            output_folder = tempfile.mkdtemp()
        
        if self.available_backend == "pymupdf":
            return self._convert_with_pymupdf(pdf_path, output_folder)
        elif self.available_backend == "pdf2image":
            return self._convert_with_pdf2image(pdf_path, output_folder)
        else:
            raise RuntimeError("사용 가능한 PDF 처리 백엔드가 없습니다.")
    
    def _convert_with_pymupdf(self, pdf_path: str, output_folder: str) -> Tuple[List[str], int]:
        """PyMuPDF를 사용하여 PDF를 이미지로 변환"""
        doc = fitz.open(pdf_path)
        image_paths = []
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            # 높은 해상도로 렌더링 (300 DPI)
            mat = fitz.Matrix(300/72, 300/72)
            pix = page.get_pixmap(matrix=mat)
            
            image_path = os.path.join(output_folder, f'page_{page_num+1}.png')
            pix.save(image_path)
            image_paths.append(image_path)
        
        num_pages = len(doc)
        doc.close()
        return image_paths, num_pages
    
    def _convert_with_pdf2image(self, pdf_path: str, output_folder: str) -> Tuple[List[str], int]:
        """pdf2image를 사용하여 PDF를 이미지로 변환"""
        try:
            # PDF 페이지 수 확인
            if PYPDF2_AVAILABLE:
                with open(pdf_path, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    num_pages = len(pdf_reader.pages)
            else:
                num_pages = 1  # 기본값
            
            # PDF를 이미지로 변환
            images = convert_from_path(pdf_path, dpi=300)
            image_paths = []
            
            for i, image in enumerate(images):
                image_path = os.path.join(output_folder, f'page_{i+1}.jpg')
                image.save(image_path, 'JPEG')
                image_paths.append(image_path)
            
            return image_paths, len(images)
            
        except Exception as e:
            if "poppler" in str(e).lower():
                raise RuntimeError(
                    "Poppler가 설치되지 않았거나 PATH에 등록되지 않았습니다.\n"
                    "해결 방법:\n"
                    "1. Windows: conda install -c conda-forge poppler\n"
                    "2. macOS: brew install poppler\n"
                    "3. Linux: sudo apt-get install poppler-utils\n"
                    "또는 PyMuPDF 사용을 권장합니다: pip install PyMuPDF"
                )
            else:
                raise e