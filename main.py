# main.py
import sys
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QTreeWidgetItem
from PyQt5.QtCore import QThread, pyqtSignal
from ui_main import Ui_MainWindow
from downloader import Downloader

class DownloadThread(QThread):
    # 定義自訂信號，用於通知下載完成
    download_finished = pyqtSignal(str)  # 傳送下載的視頻 URL
    
    def __init__(self, url, audio_format, quality, segments, output_dir):
        super().__init__()
        self.url = url
        self.audio_format = audio_format
        self.quality = quality
        self.segments = segments
        self.output_dir = output_dir
        self.downloader = Downloader()
        # 連接 Downloader 的信號
        self.downloader.progress.connect(self.emit_progress)
        self.downloader.status.connect(self.emit_status)
    
    def run(self):
        self.downloader.download_audio(self.url, self.audio_format, self.quality, self.segments, self.output_dir)
        self.download_finished.emit(self.url)
    
    def emit_progress(self, value):
        # 可選：這裡可以發射進度到主窗口
        pass
    
    def emit_status(self, message):
        # 可選：這裡可以發射狀態到主窗口
        pass

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.threads = []  # 用於追蹤線程
        self.completed_downloads = 0
        self.total_downloads = 0
        
        # 連接按鈕
        self.browseButton.clicked.connect(self.browse_output)
        self.loadUrlsButton.clicked.connect(self.load_urls)
        self.addSegmentButton.clicked.connect(self.add_segment)
        self.removeSegmentButton.clicked.connect(self.remove_segment)
        self.downloadButton.clicked.connect(self.start_download)
    
    def browse_output(self):
        folder = QFileDialog.getExistingDirectory(self, "選擇下載目錄")
        if folder:
            self.outputLineEdit.setText(folder)
    
    def load_urls(self):
        urls_text = self.urlsTextEdit.toPlainText().strip()
        if not urls_text:
            QMessageBox.warning(self, "輸入錯誤", "請輸入至少一個 YouTube 視頻的 URL。")
            return
        urls = [url.strip() for url in urls_text.splitlines() if url.strip()]
        
        # 清空 treeWidget
        self.treeWidget.clear()
        
        # 添加 URLs 為頂層項
        for url in urls:
            url_item = QTreeWidgetItem([url])
            self.treeWidget.addTopLevelItem(url_item)
    
    def add_segment(self):
        selected_items = self.treeWidget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "選擇錯誤", "請先選擇一個視頻 URL。")
            return
        
        current_item = selected_items[0]
        if current_item.parent() is not None:
            QMessageBox.warning(self, "選擇錯誤", "請選擇一個頂層視頻 URL。")
            return
        
        start = self.startTimeEdit.text().strip()
        end = self.endTimeEdit.text().strip()
        if not self.validate_time_format(start) or not self.validate_time_format(end):
            QMessageBox.warning(self, "輸入錯誤", "開始時間和結束時間必須為格式: HH:MM:SS。")
            return
        if self.time_to_seconds(start) >= self.time_to_seconds(end):
            QMessageBox.warning(self, "輸入錯誤", "開始時間必須小於結束時間。")
            return
        
        # 添加時間段作為子項
        segment_item = QTreeWidgetItem([f"{start} - {end}"])
        current_item.addChild(segment_item)
        current_item.setExpanded(True)
        self.startTimeEdit.clear()
        self.endTimeEdit.clear()
    
    def remove_segment(self):
        selected_items = self.treeWidget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "選擇錯誤", "請先選擇一個時間段。")
            return
        
        current_item = selected_items[0]
        if current_item.parent() is None:
            QMessageBox.warning(self, "選擇錯誤", "請選擇一個時間段，而不是視頻 URL。")
            return
        
        parent = current_item.parent()
        parent.removeChild(current_item)
    
    def start_download(self):
        output_dir = self.outputLineEdit.text().strip()
        if not output_dir:
            QMessageBox.warning(self, "輸入錯誤", "請選擇下載目錄。")
            return
        
        # 解析下載任務
        top_level_count = self.treeWidget.topLevelItemCount()
        if top_level_count == 0:
            QMessageBox.warning(self, "錯誤", "請先加載視頻 URLs 並添加時間段。")
            return
        
        download_tasks = []  # 將 download_tasks 定義在這裡
        
        for i in range(top_level_count):
            url_item = self.treeWidget.topLevelItem(i)
            url = url_item.text(0)
            segments = []
            for j in range(url_item.childCount()):
                segment_text = url_item.child(j).text(0)
                start, end = segment_text.split(' - ')
                segments.append((start, end))
            
            # 如果沒有選擇時間段，segments 為空列表
            download_tasks.append((url, segments if segments else None))
        
        if not download_tasks:
            QMessageBox.warning(self, "錯誤", "沒有下載任務。")
            return
        
        self.progressBar.setValue(0)
        self.downloadButton.setEnabled(False)
        
        self.completed_downloads = 0
        self.total_downloads = len(download_tasks)
        
        # 啟動下載線程
        for url, segments in download_tasks:
            thread = DownloadThread(url, self.formatComboBox.currentText(), self.qualityComboBox.currentText(), segments, output_dir)
            thread.download_finished.connect(self.on_download_finished)
            thread.downloader.status.connect(self.update_log)  # 連接狀態信號
            thread.downloader.progress.connect(self.progressBar.setValue)  # 連接進度條
            self.threads.append(thread)
            thread.start()
    
    def on_download_finished(self, url):
        self.completed_downloads += 1
        # 更新進度條
        progress = int((self.completed_downloads / self.total_downloads) * 100)
        self.progressBar.setValue(progress)
        if self.completed_downloads == self.total_downloads:
            QMessageBox.information(self, "完成", "所有下載任務已完成。")
            self.downloadButton.setEnabled(True)
    
    def update_log(self, message):
        self.logTextEdit.append(message)

    def validate_time_format(self, time_str):
        """
        驗證時間格式是否為 HH:MM:SS
        """
        pattern = re.compile(r'^([0-1]\d|2[0-3]):([0-5]\d):([0-5]\d)$')
        return bool(pattern.match(time_str))
    
    def time_to_seconds(self, time_str):
        """
        將 HH:MM:SS 格式的時間轉換為秒數
        """
        h, m, s = map(int, time_str.split(':'))
        return h * 3600 + m * 60 + s

    # Override closeEvent to ensure all threads are properly terminated
    def closeEvent(self, event):
        for thread in self.threads:
            thread.wait()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
