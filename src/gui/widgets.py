from PyQt5.QtWidgets import (QTableWidget, QWidget, QHBoxLayout, QLabel, 
                             QToolButton, QDialog, QVBoxLayout, QFormLayout,
                             QLineEdit, QCheckBox, QDialogButtonBox, QGroupBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QKeySequence
import pyperclip

from ..core.document_processor import DocumentProcessor
from ..config.settings import app_settings


class CopyableTableWidget(QTableWidget):
    """복사 기능이 추가된 테이블 위젯"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSelectionMode(QTableWidget.ExtendedSelection)
        self.main_window = None

    def setMainWindow(self, main_window):
        """메인 윈도우 참조 설정"""
        self.main_window = main_window

    def keyPressEvent(self, event):
        """키 이벤트 처리 - Ctrl+C로 선택된 항목 복사"""
        if event.matches(QKeySequence.Copy):
            self.copySelection()
        else:
            super().keyPressEvent(event)

    def copySelection(self):
        """선택된 항목을 클립보드에 복사"""
        selected_items = self.selectedItems()

        if not selected_items:
            return

        # 선택된 행/열 구조 파악
        rows = {}
        for item in selected_items:
            if item.row() not in rows:
                rows[item.row()] = {}
            rows[item.row()][item.column()] = item.text()

        # 클립보드에 복사할 텍스트 생성
        text = ""
        for row in sorted(rows.keys()):
            cells = []
            for col in sorted(rows[row].keys()):
                cells.append(rows[row][col])
            text += "\t".join(cells) + "\n"

        # 클립보드에 복사
        pyperclip.copy(text.strip())

        # 복사 확인 메시지
        if self.main_window and hasattr(self.main_window, 'statusBar'):
            n_rows = len(rows)
            n_cells = len(selected_items)
            if n_rows == 1 and n_cells == 1:
                self.main_window.statusBar().showMessage("1개 셀이 클립보드에 복사되었습니다", 2000)
            elif n_rows == 1:
                self.main_window.statusBar().showMessage(f"{n_cells}개 셀이 클립보드에 복사되었습니다", 2000)
            else:
                self.main_window.statusBar().showMessage(f"{n_rows}행 {n_cells}개 셀이 클립보드에 복사되었습니다", 2000)

    def copySelectedRows(self):
        """선택된 행의 내용을 클립보드에 복사"""
        selected_rows = set()

        # 선택된 셀들로부터 행 번호 수집
        for item in self.selectedItems():
            selected_rows.add(item.row())

        if not selected_rows:
            return

        # 클립보드에 복사할 텍스트 생성
        text = ""
        for row in sorted(selected_rows):
            row_text = []
            for col in range(self.columnCount()):
                item = self.item(row, col)
                if item is not None:
                    row_text.append(item.text())
                else:
                    row_text.append("")
            text += "\t".join(row_text) + "\n"

        # 클립보드에 복사
        pyperclip.copy(text.strip())

        if self.main_window and hasattr(self.main_window, 'statusBar'):
            if len(selected_rows) == 1:
                self.main_window.statusBar().showMessage("1행이 클립보드에 복사되었습니다", 2000)
            else:
                self.main_window.statusBar().showMessage(f"{len(selected_rows)}행이 클립보드에 복사되었습니다", 2000)

    def copyColumn(self, column):
        """테이블의 특정 열 전체를 복사"""
        if column < 0 or column >= self.columnCount():
            return

        # 클립보드에 복사할 텍스트 생성
        column_texts = []
        for row in range(self.rowCount()):
            item = self.item(row, column)
            if item is not None:
                column_texts.append(item.text())
            else:
                column_texts.append("")

        text = "\n".join(column_texts)

        # 클립보드에 복사
        pyperclip.copy(text.strip())

        # 열 이름 가져오기
        column_names = ['품번', '수량']  # 기본 열 이름 목록
        column_name = column_names[column] if column < len(column_names) else f"열 {column+1}"

        # 복사 확인 메시지
        if self.main_window and hasattr(self.main_window, 'statusBar'):
            self.main_window.statusBar().showMessage(f"'{column_name}' 열 전체({len(column_texts)}개 항목)가 클립보드에 복사되었습니다", 2000)

    def copyTableForExcel(self, include_header=True):
        """엑셀 호환 형식으로 테이블 전체를 클립보드에 복사"""
        if self.rowCount() == 0:
            return

        text_parts = []
        
        # 헤더 추가 (선택적)
        if include_header:
            headers = []
            for col in range(self.columnCount()):
                header_item = self.horizontalHeaderItem(col)
                if header_item:
                    headers.append(header_item.text())
                else:
                    headers.append(f"열{col+1}")
            text_parts.append("\t".join(headers))

        # 모든 행 데이터 추가
        for row in range(self.rowCount()):
            row_data = []
            for col in range(self.columnCount()):
                item = self.item(row, col)
                if item is not None:
                    # 엑셀 호환을 위해 특수 문자 처리
                    cell_text = item.text().replace('\n', ' ').replace('\r', ' ')
                    row_data.append(cell_text)
                else:
                    row_data.append("")
            text_parts.append("\t".join(row_data))

        # 최종 텍스트 생성 (탭으로 구분, 줄바꿈으로 행 구분)
        final_text = "\n".join(text_parts)
        
        # 클립보드에 복사
        pyperclip.copy(final_text)

        # 확인 메시지
        if self.main_window and hasattr(self.main_window, 'statusBar'):
            row_count = self.rowCount()
            header_text = "헤더 포함 " if include_header else ""
            self.main_window.statusBar().showMessage(
                f"테이블 전체({header_text}{row_count}행)가 엑셀 호환 형식으로 클립보드에 복사되었습니다", 3000
            )

    def copySelectedAsExcelTable(self):
        """선택된 영역을 엑셀 호환 형식으로 복사"""
        selected_items = self.selectedItems()
        if not selected_items:
            return

        # 선택된 셀들의 좌표 수집
        selected_positions = {}
        for item in selected_items:
            row, col = item.row(), item.column()
            if row not in selected_positions:
                selected_positions[row] = {}
            selected_positions[row][col] = item.text()

        # 연속된 영역인지 확인하고 정렬
        rows = sorted(selected_positions.keys())
        if not rows:
            return

        cols = set()
        for row_data in selected_positions.values():
            cols.update(row_data.keys())
        cols = sorted(cols)

        # 엑셀 호환 텍스트 생성
        text_parts = []
        for row in rows:
            row_data = []
            for col in cols:
                cell_value = selected_positions.get(row, {}).get(col, "")
                # 엑셀 호환을 위해 특수 문자 처리
                cell_value = cell_value.replace('\n', ' ').replace('\r', ' ')
                row_data.append(cell_value)
            text_parts.append("\t".join(row_data))

        final_text = "\n".join(text_parts)
        pyperclip.copy(final_text)

        # 확인 메시지
        if self.main_window and hasattr(self.main_window, 'statusBar'):
            cell_count = len(selected_items)
            self.main_window.statusBar().showMessage(
                f"선택된 영역({cell_count}개 셀)이 엑셀 호환 형식으로 클립보드에 복사되었습니다", 3000
            )


class ColumnHeaderWidget(QWidget):
    """열 헤더와 복사 버튼을 포함하는 위젯"""

    def __init__(self, text, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(2, 0, 2, 0)
        layout.setSpacing(2)

        # 헤더 텍스트
        self.label = QLabel(text)
        self.label.setFont(QFont('Arial', 9, QFont.Bold))
        self.label.setAlignment(Qt.AlignCenter)

        # 복사 버튼
        self.copy_btn = QToolButton()
        self.copy_btn.setText("📋")
        self.copy_btn.setToolTip(f"{text} 열 전체 복사")
        self.copy_btn.setMaximumSize(20, 20)

        layout.addWidget(self.label, 1)  # 1은 stretch factor
        layout.addWidget(self.copy_btn, 0)  # 0은 stretch factor 없음

        self.setLayout(layout)


class SettingsDialog(QDialog):
    """설정 대화상자"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle("설정")
        self.setMinimumWidth(500)

        layout = QVBoxLayout()

        # API 설정 그룹
        api_group = QGroupBox("OpenAI API 설정")
        api_layout = QFormLayout()

        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.Password)
        self.show_key_checkbox = QCheckBox("API 키 표시")
        self.show_key_checkbox.stateChanged.connect(self.toggle_key_visibility)

        key_layout = QHBoxLayout()
        key_layout.addWidget(self.api_key_input)
        key_layout.addWidget(self.show_key_checkbox)

        self.model_input = QLineEdit("gpt-4o-mini")

        api_layout.addRow("OpenAI API 키:", key_layout)
        api_layout.addRow("사용할 모델:", self.model_input)

        # 개발용 설정
        self.mock_mode_checkbox = QCheckBox("개발 모드 (API 호출 없이 모킹)")
        api_layout.addRow("개발 설정:", self.mock_mode_checkbox)

        api_group.setLayout(api_layout)
        layout.addWidget(api_group)

        # 버튼 영역
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def toggle_key_visibility(self, state):
        """API 키 표시/숨김 전환"""
        if state == Qt.Checked:
            self.api_key_input.setEchoMode(QLineEdit.Normal)
        else:
            self.api_key_input.setEchoMode(QLineEdit.Password)

    def load_settings(self):
        """저장된 설정 불러오기"""
        self.api_key_input.setText(app_settings.api_key or "")
        self.model_input.setText(app_settings.model_name)
        self.mock_mode_checkbox.setChecked(app_settings.mock_mode)

    def save_settings(self):
        """설정 저장"""
        app_settings.api_key = self.api_key_input.text()
        app_settings.model_name = self.model_input.text()
        app_settings.mock_mode = self.mock_mode_checkbox.isChecked()
        app_settings.save_settings()


class ProcessingWorker(QThread):
    """백그라운드에서 문서 처리를 수행하는 워커 스레드"""
    progress_updated = pyqtSignal(int, int)  # (현재 페이지, 총 페이지 수)
    result_ready = pyqtSignal(object)  # ProcessedDocument 객체
    error_occurred = pyqtSignal(str)

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        self.processor = DocumentProcessor()

    def run(self):
        try:
            result = self.processor.process_document(self.file_path, self.progress_callback)
            self.result_ready.emit(result)
        except Exception as e:
            self.error_occurred.emit(f"오류 발생: {str(e)}")

    def progress_callback(self, current, total):
        self.progress_updated.emit(current, total)