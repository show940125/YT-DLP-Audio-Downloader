# ui_main.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QTextEdit,
    QProgressBar, QTreeWidget, QTreeWidgetItem
)
from PyQt5.QtCore import Qt

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("YouTube 音頻下載器")
        MainWindow.setFixedSize(700, 800)  # 設置固定窗口大小
        central_widget = QWidget()
        MainWindow.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        
        # 設置樣式表
        style = """
        QWidget {
            font-family: 微軟正黑體;
            font-size: 14px;
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            font-size: 14px;
            margin: 4px 2px;
            border-radius: 8px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QLineEdit, QTextEdit, QComboBox, QTreeWidget {
            border: 1px solid #ccc;
            border-radius: 4px;
            padding: 6px;
        }
        QLabel {
            font-weight: bold;
        }
        QProgressBar {
            height: 20px;
        }
        """
        central_widget.setStyleSheet(style)
        
        # 視頻 URLs 輸入
        urls_label = QLabel("視頻 URLs (每行一個):")
        self.urlsTextEdit = QTextEdit()
        main_layout.addWidget(urls_label)
        main_layout.addWidget(self.urlsTextEdit)
        
        # 加載 URLs 按鈕
        self.loadUrlsButton = QPushButton("加載 URLs")
        main_layout.addWidget(self.loadUrlsButton)
        
        # 音頻格式
        format_layout = QHBoxLayout()
        format_label = QLabel("音頻格式:")
        self.formatComboBox = QComboBox()
        self.formatComboBox.addItems(["mp3", "aac", "wav", "m4a"])
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.formatComboBox)
        main_layout.addLayout(format_layout)
        
        # 音質選項
        quality_layout = QHBoxLayout()
        quality_label = QLabel("音質:")
        self.qualityComboBox = QComboBox()
        self.qualityComboBox.addItems(["128k", "192k", "256k", "320k"])
        quality_layout.addWidget(quality_label)
        quality_layout.addWidget(self.qualityComboBox)
        main_layout.addLayout(quality_layout)
        
        # 輸出目錄
        output_layout = QHBoxLayout()
        output_label = QLabel("輸出目錄:")
        self.outputLineEdit = QLineEdit()
        self.browseButton = QPushButton("瀏覽")
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.outputLineEdit)
        output_layout.addWidget(self.browseButton)
        main_layout.addLayout(output_layout)
        
        # 提示標籤
        no_segment_hint_label = QLabel("提示: 如果不選擇時間段，將會下載整部影片的音頻")
        main_layout.addWidget(no_segment_hint_label)
        
        # 時間段選擇（按視頻管理）
        segments_label = QLabel("為每個視頻添加下載時間段 (格式: HH:MM:SS):")
        main_layout.addWidget(segments_label)
        
        self.treeWidget = QTreeWidget()
        self.treeWidget.setHeaderLabels(["視頻 URL", "時間段"])
        self.treeWidget.setColumnWidth(0, 400)
        self.treeWidget.setColumnWidth(1, 250)
        main_layout.addWidget(self.treeWidget)
        
        # 添加時間段按鈕
        segment_buttons_layout = QHBoxLayout()
        self.addSegmentButton = QPushButton("添加時間段")
        self.removeSegmentButton = QPushButton("移除選中")
        segment_buttons_layout.addWidget(self.addSegmentButton)
        segment_buttons_layout.addWidget(self.removeSegmentButton)
        main_layout.addLayout(segment_buttons_layout)
        
        # 添加開始和結束時間輸入
        time_input_layout = QHBoxLayout()
        self.startTimeEdit = QLineEdit()
        self.startTimeEdit.setPlaceholderText("開始時間 (HH:MM:SS)")
        self.endTimeEdit = QLineEdit()
        self.endTimeEdit.setPlaceholderText("結束時間 (HH:MM:SS)")
        time_input_layout.addWidget(self.startTimeEdit)
        time_input_layout.addWidget(self.endTimeEdit)
        main_layout.addLayout(time_input_layout)

        # 日誌輸出框
        self.logTextEdit = QTextEdit()
        self.logTextEdit.setReadOnly(True)
        main_layout.addWidget(QLabel("下載日誌:"))
        main_layout.addWidget(self.logTextEdit)
        
        # 進度條
        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)
        main_layout.addWidget(self.progressBar)
        
        # 下載按鈕
        self.downloadButton = QPushButton("下載")
        main_layout.addWidget(self.downloadButton)
        
        central_widget.setLayout(main_layout)
