"""GUI 스타일 정의"""

MAIN_STYLE_SHEET = """
QMainWindow {
    background-color: #f0f0f0;
}

QGroupBox {
    font-weight: bold;
    border: 1px solid #cccccc;
    border-radius: 6px;
    margin-top: 12px;
    padding-top: 10px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px 0 5px;
}

QPushButton {
    background-color: #4a86e8;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #3a76d8;
}

QPushButton:pressed {
    background-color: #2a66c8;
}

QPushButton:disabled {
    background-color: #cccccc;
    color: #666666;
}

QProgressBar {
    border: 1px solid #cccccc;
    border-radius: 4px;
    text-align: center;
    height: 20px;
}

QProgressBar::chunk {
    background-color: #4a86e8;
    width: 1px;
}

QLabel {
    color: #333333;
}

QTableWidget {
    gridline-color: #d9d9d9;
    selection-background-color: #e6f0ff;
    selection-color: #000000;
    border: 1px solid #cccccc;
    border-radius: 4px;
}

QTableWidget::item {
    padding: 4px;
}

QTableWidget QHeaderView::section {
    background-color: #e6e6e6;
    border: 1px solid #cccccc;
    padding: 4px;
    font-weight: bold;
}

QTabWidget::pane {
    border: 1px solid #cccccc;
    border-radius: 4px;
}

QTabBar::tab {
    background-color: #e6e6e6;
    border: 1px solid #cccccc;
    border-bottom: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    padding: 6px 12px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: #ffffff;
    border-bottom: 1px solid #ffffff;
}

QTextEdit {
    border: 1px solid #cccccc;
    border-radius: 4px;
    background-color: #ffffff;
}

QToolBar {
    background-color: #e6e6e6;
    border: none;
    spacing: 3px;
    padding: 3px;
}

QToolButton {
    border: none;
    border-radius: 4px;
    padding: 5px;
    background-color: transparent;
}

QToolButton:hover {
    background-color: #d9d9d9;
}

QToolButton:pressed {
    background-color: #cccccc;
}
"""