import os
import json
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QLabel, QVBoxLayout, 
                             QHBoxLayout, QFileDialog, QTextEdit, QWidget, 
                             QProgressBar, QMessageBox, QTableWidgetItem, 
                             QHeaderView, QTabWidget, QGroupBox, QAction, 
                             QMenu, QToolBar)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont

from .widgets import CopyableTableWidget, SettingsDialog, ProcessingWorker
from .styles import MAIN_STYLE_SHEET
from ..models.document import ProcessedDocument
from ..config.settings import app_settings
from ..utils.file_utils import save_json_result


class MainWindow(QMainWindow):
    """OCR 응용 프로그램의 메인 윈도우"""

    def __init__(self):
        super().__init__()
        self.selected_file = None
        self.worker = None
        self.current_document = None
        
        self.init_ui()

    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle('GPT OCR 변환기')
        self.setGeometry(100, 100, 1000, 800)
        self.setStyleSheet(MAIN_STYLE_SHEET)

        # 툴바 설정
        self._setup_toolbar()

        # 상태바 설정
        self.statusBar().showMessage('준비')

        # 중앙 위젯 설정
        self._setup_central_widget()

    def _setup_toolbar(self):
        """툴바 설정"""
        toolbar = QToolBar("메인 툴바")
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)

        # 파일 선택 액션
        file_action = QAction("파일 선택", self)
        file_action.setStatusTip("OCR 처리할 파일 선택")
        file_action.triggered.connect(self.select_file)
        toolbar.addAction(file_action)

        # 처리 액션
        process_action = QAction("처리 시작", self)
        process_action.setStatusTip("OCR 처리 시작")
        process_action.triggered.connect(self.start_processing)
        process_action.setEnabled(False)
        self.process_action = process_action
        toolbar.addAction(process_action)

        # 설정 액션
        settings_action = QAction("설정", self)
        settings_action.setStatusTip("앱 설정")
        settings_action.triggered.connect(self.show_settings)
        toolbar.addAction(settings_action)

    def _setup_central_widget(self):
        """중앙 위젯 설정"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 파일 선택 그룹
        self._setup_file_selection_group(main_layout)

        # 작업 상태 그룹
        self._setup_status_group(main_layout)

        # 비용 정보 그룹
        self._setup_cost_group(main_layout)

        # 결과 그룹
        self._setup_result_group(main_layout)

        # 상태 표시줄
        self.status_label = QLabel('준비')
        self.status_label.setFont(QFont('Arial', 9))
        main_layout.addWidget(self.status_label)

    def _setup_file_selection_group(self, main_layout):
        """파일 선택 그룹 설정"""
        file_group = QGroupBox("파일 선택")
        file_layout = QHBoxLayout()
        
        self.file_label = QLabel('선택된 파일: 없음')
        self.file_button = QPushButton('찾아보기')
        self.file_button.setFixedWidth(100)
        self.file_button.clicked.connect(self.select_file)
        
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_button)
        file_group.setLayout(file_layout)
        main_layout.addWidget(file_group)

    def _setup_status_group(self, main_layout):
        """작업 상태 그룹 설정"""
        status_group = QGroupBox("작업 상태")
        status_layout = QVBoxLayout()

        # 진행 상태 표시줄
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        status_layout.addWidget(self.progress_bar)

        # 처리 버튼
        button_layout = QHBoxLayout()
        self.process_button = QPushButton('OCR 처리 시작')
        self.process_button.setFixedHeight(40)
        self.process_button.setEnabled(False)
        self.process_button.clicked.connect(self.start_processing)
        button_layout.addStretch()
        button_layout.addWidget(self.process_button)
        button_layout.addStretch()
        status_layout.addLayout(button_layout)

        status_group.setLayout(status_layout)
        main_layout.addWidget(status_group)

    def _setup_cost_group(self, main_layout):
        """비용 정보 그룹 설정"""
        cost_group = QGroupBox("API 비용 정보")
        cost_layout = QVBoxLayout()

        cost_info_layout = QHBoxLayout()
        self.cost_label = QLabel('추정 API 비용: $0.00 (₩0)')
        self.cost_label.setFont(QFont('Arial', 10, QFont.Bold))
        cost_info_layout.addWidget(self.cost_label)
        cost_info_layout.addStretch()

        cost_layout.addLayout(cost_info_layout)
        cost_group.setLayout(cost_layout)
        main_layout.addWidget(cost_group)

    def _setup_result_group(self, main_layout):
        """결과 그룹 설정"""
        result_group = QGroupBox("OCR 결과")
        result_layout = QVBoxLayout()

        # 탭 위젯 생성
        self.tab_widget = QTabWidget()

        # 테이블 탭
        self.table_widget = CopyableTableWidget()
        self.table_widget.setMainWindow(self)
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(['품번', '수량'])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setAlternatingRowColors(True)
        self.tab_widget.addTab(self.table_widget, "테이블 보기")

        # 테이블 우클릭 컨텍스트 메뉴 추가
        self.table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self.show_table_context_menu)

        # JSON 탭
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setFont(QFont('Courier New', 10))
        self.tab_widget.addTab(self.result_text, "JSON 보기")

        result_layout.addWidget(self.tab_widget)
        result_group.setLayout(result_layout)
        main_layout.addWidget(result_group, 1)

    def select_file(self):
        """파일 선택 다이얼로그 열기"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "OCR 처리할 파일 선택", "", "이미지/PDF 파일 (*.jpg *.jpeg *.png *.pdf)"
        )

        if file_path:
            self.selected_file = file_path
            file_name = os.path.basename(file_path)
            self.file_label.setText(f'선택된 파일: {file_name}')
            self.file_label.setToolTip(file_path)
            self.process_button.setEnabled(True)
            self.process_action.setEnabled(True)
            self.statusBar().showMessage(f'파일 선택됨: {file_name}')

    def start_processing(self):
        """OCR 처리 시작"""
        if not self.selected_file:
            QMessageBox.warning(self, "경고", "파일을 먼저 선택해주세요.")
            return

        # API 키 확인 (모킹 모드가 아닌 경우)
        if not app_settings.mock_mode and not app_settings.api_key:
            reply = QMessageBox.question(
                self, "API 키 없음",
                "OpenAI API 키가 설정되지 않았습니다.\n설정 화면을 열까요?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.show_settings()
            return

        # UI 업데이트
        self._set_processing_state(True)

        # 워커 스레드에서 처리 시작
        self.worker = ProcessingWorker(self.selected_file)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.result_ready.connect(self.handle_result)
        self.worker.error_occurred.connect(self.handle_error)
        self.worker.start()

    def _set_processing_state(self, processing: bool):
        """처리 중 상태 UI 업데이트"""
        self.process_button.setEnabled(not processing)
        self.process_action.setEnabled(not processing)
        self.file_button.setEnabled(not processing)
        self.progress_bar.setVisible(processing)
        
        if processing:
            self.progress_bar.setValue(0)
            self.result_text.clear()
            self.table_widget.setRowCount(0)
            self.cost_label.setText('추정 API 비용: $0.00 (₩0)')
            self.status_label.setText("처리 중...")
            self.statusBar().showMessage("처리 중...")
        else:
            self.progress_bar.setVisible(False)

    def update_progress(self, current, total):
        """진행 상황 업데이트"""
        progress = int(current / total * 100)
        self.progress_bar.setValue(progress)
        self.status_label.setText(f"처리 중... ({current}/{total} 페이지)")
        self.statusBar().showMessage(f"처리 중... {progress}% 완료")

    def handle_result(self, document: ProcessedDocument):
        """OCR 결과 처리"""
        self.current_document = document
        
        # 비용 정보 업데이트
        self.cost_label.setText(f'추정 API 비용: {app_settings.format_cost(document.processing_cost)}')

        # JSON 파일로 저장
        output_file = save_json_result(document.to_dict(), self.selected_file)

        # JSON 표시
        formatted_json = json.dumps(document.to_dict(), ensure_ascii=False, indent=2)
        self.result_text.setText(formatted_json)

        # 테이블에 데이터 표시
        self._populate_table(document)

        # UI 상태 업데이트
        self._set_processing_state(False)
        
        item_count = document.total_items
        status_msg = f"완료! {item_count}개 항목 추출됨. 결과가 {output_file}에 저장되었습니다."
        self.status_label.setText(status_msg)
        self.statusBar().showMessage(status_msg)

        # 완료 메시지
        if item_count == 0:
            QMessageBox.warning(
                self,
                "처리 완료",
                f"OCR 처리가 완료되었지만 품목이 검출되지 않았습니다.\n"
                f"- 결과 파일: {output_file}\n"
                f"- 추정 API 비용: {app_settings.format_cost(document.processing_cost)}\n\n"
                f"JSON 탭에서 원본 응답을 확인해보세요."
            )
        else:
            QMessageBox.information(
                self,
                "처리 완료",
                f"OCR 처리가 완료되었습니다.\n"
                f"- 추출 항목: {item_count}개\n"
                f"- 결과 파일: {output_file}\n"
                f"- 추정 API 비용: {app_settings.format_cost(document.processing_cost)}"
            )

    def _populate_table(self, document: ProcessedDocument):
        """테이블에 데이터 채우기"""
        self.table_widget.setRowCount(0)
        
        for item in document.all_items:
            row = self.table_widget.rowCount()
            self.table_widget.insertRow(row)
            
            name_item = QTableWidgetItem(str(item.product_code))
            qty_item = QTableWidgetItem(str(item.quantity))
            qty_item.setTextAlignment(Qt.AlignCenter)
            
            self.table_widget.setItem(row, 0, name_item)
            self.table_widget.setItem(row, 1, qty_item)

    def handle_error(self, error_msg):
        """오류 처리"""
        self.result_text.setText(f"오류 발생:\n{error_msg}")
        self.status_label.setText("오류 발생")
        self.statusBar().showMessage("오류 발생")
        self._set_processing_state(False)

        QMessageBox.critical(self, "오류", f"처리 중 오류가 발생했습니다:\n{error_msg}")

    def show_table_context_menu(self, pos):
        """테이블 우클릭 컨텍스트 메뉴 표시"""
        context_menu = QMenu(self)

        # 기본 선택 항목 복사
        copy_selection_action = QAction("선택 항목 복사", self)
        copy_selection_action.triggered.connect(self.table_widget.copySelection)

        # 행 복사
        copy_rows_action = QAction("선택 행 복사", self)
        copy_rows_action.triggered.connect(self.table_widget.copySelectedRows)

        # 열 복사
        copy_column_actions = []
        selected_columns = set()
        for item in self.table_widget.selectedItems():
            selected_columns.add(item.column())

        column_names = ['품번', '수량']

        for col in sorted(selected_columns):
            if col < len(column_names):
                col_name = column_names[col]
                action = QAction(f"'{col_name}' 열 복사", self)
                action.triggered.connect(lambda checked, col=col: self.copy_column(col))
                copy_column_actions.append(action)

        # 모든 항목 복사
        copy_all_action = QAction("모두 복사", self)
        copy_all_action.triggered.connect(self.copy_all_rows)

        if self.table_widget.rowCount() > 0:
            context_menu.addAction(copy_selection_action)
            context_menu.addAction(copy_rows_action)

            if copy_column_actions:
                context_menu.addSeparator()
                for action in copy_column_actions:
                    context_menu.addAction(action)

            context_menu.addSeparator()
            context_menu.addAction(copy_all_action)

            context_menu.exec_(self.table_widget.mapToGlobal(pos))

    def copy_all_rows(self):
        """모든 행을 클립보드에 복사"""
        if self.table_widget.rowCount() == 0:
            return

        # 모든 행 선택
        self.table_widget.selectAll()
        self.table_widget.copySelectedRows()

    def copy_column(self, column):
        """테이블의 특정 열 전체를 복사"""
        self.table_widget.copyColumn(column)

    def show_settings(self):
        """설정 대화상자 표시"""
        dialog = SettingsDialog(self)
        if dialog.exec_():
            dialog.save_settings()
            QMessageBox.information(
                self,
                "설정 저장 완료",
                "설정이 저장되었습니다. 변경된 설정은 다음 OCR 처리부터 적용됩니다."
            )