import sys

import Package_Page as PP
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

"""  
  主程序---创建App
"""


# 主窗口
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("CardGame")
        self.setGeometry(400, 500, 600, 600)

        self.stacked_widget = QStackedWidget()

        self.page_a = PP.PageA()
        self.page_b = PP.PageB()

        self.stacked_widget.addWidget(self.page_a)
        self.stacked_widget.addWidget(self.page_b)

        self.combo_box = QComboBox()
        self.combo_box.addItem("PAGE1 -- 随机模拟")
        self.combo_box.addItem("PAGE2 -- 自由选择")
        self.combo_box.currentIndexChanged.connect(self.display_page)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.combo_box)
        layout.addWidget(self.stacked_widget)

        self.setLayout(layout)

    # 用于显示不同界面
    def display_page(self, index):
        self.stacked_widget.setCurrentIndex(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Arial", 12)
    app.setFont(font)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
