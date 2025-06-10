import pytest
from PyQt5.QtWidgets import QApplication, QTableWidgetItem
from PyQt5.QtCore import Qt
from src.gui.widgets import CopyableTableWidget
import pyperclip


@pytest.fixture
def app():
    """QApplication 인스턴스 생성"""
    return QApplication([])


@pytest.fixture
def table_widget(app):
    """테스트용 테이블 위젯 생성"""
    widget = CopyableTableWidget()
    widget.setColumnCount(2)
    widget.setHorizontalHeaderLabels(['품번', '수량'])
    
    # 테스트 데이터 추가
    test_data = [
        ("DMCA-4N-SA", "22"),
        ("DMCA-8N-SA", "7"),
        ("DMCA-12N-SA", "15"),
    ]
    
    for i, (code, qty) in enumerate(test_data):
        widget.insertRow(i)
        widget.setItem(i, 0, QTableWidgetItem(code))
        widget.setItem(i, 1, QTableWidgetItem(qty))
    
    return widget


def test_copy_table_for_excel_with_header(table_widget):
    """헤더 포함 엑셀 복사 테스트"""
    table_widget.copyTableForExcel(include_header=True)
    
    clipboard_content = pyperclip.paste()
    lines = clipboard_content.split('\n')
    
    # 헤더 확인
    assert lines[0] == "품번\t수량"
    
    # 데이터 행 확인
    assert lines[1] == "DMCA-4N-SA\t22"
    assert lines[2] == "DMCA-8N-SA\t7"
    assert lines[3] == "DMCA-12N-SA\t15"
    
    # 총 4줄 (헤더 + 3개 데이터)
    assert len(lines) == 4


def test_copy_table_for_excel_without_header(table_widget):
    """헤더 없이 엑셀 복사 테스트"""
    table_widget.copyTableForExcel(include_header=False)
    
    clipboard_content = pyperclip.paste()
    lines = clipboard_content.split('\n')
    
    # 헤더 없이 데이터만
    assert lines[0] == "DMCA-4N-SA\t22"
    assert lines[1] == "DMCA-8N-SA\t7"
    assert lines[2] == "DMCA-12N-SA\t15"
    
    # 총 3줄 (데이터만)
    assert len(lines) == 3


def test_copy_selected_as_excel_table(table_widget):
    """선택된 영역 엑셀 복사 테스트"""
    # 첫 번째와 두 번째 행 선택
    table_widget.selectRow(0)
    table_widget.selectRow(1)
    
    table_widget.copySelectedAsExcelTable()
    
    clipboard_content = pyperclip.paste()
    lines = clipboard_content.split('\n')
    
    # 선택된 2행이 복사되어야 함
    assert len(lines) == 2
    assert lines[0] == "DMCA-4N-SA\t22"
    assert lines[1] == "DMCA-8N-SA\t7"


def test_excel_format_special_characters(app):
    """특수 문자 처리 테스트"""
    widget = CopyableTableWidget()
    widget.setColumnCount(2)
    widget.setHorizontalHeaderLabels(['품번', '수량'])
    
    # 특수 문자가 포함된 데이터
    widget.insertRow(0)
    widget.setItem(0, 0, QTableWidgetItem("TEST\nPART"))  # 줄바꿈 포함
    widget.setItem(0, 1, QTableWidgetItem("10\r"))        # 캐리지 리턴 포함
    
    widget.copyTableForExcel(include_header=False)
    
    clipboard_content = pyperclip.paste()
    
    # 특수 문자가 공백으로 변환되어야 함
    assert clipboard_content == "TEST PART\t10 "


if __name__ == "__main__":
    pytest.main([__file__])