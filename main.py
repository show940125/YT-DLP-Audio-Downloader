# -*- coding: utf-8 -*-
"""
影音批量下載工具 – 最終直排版UI版
------------------------------------------------------------
本程式整合 yt-dlp 與 FFmpeg 後製，支援從 YouTube 等影音網站下載影片或音檔，
並允許使用者針對單筆或批量任務進行獨立設定。除了原有功能外，
在影片/音檔種類中均新增「效率(webm)」選項，直接下載原始webm串流以追求快速下載。
本程式UI採直排設計，各功能模組依下列順序排列：

第一排：FFMPEG路徑：【框框】 【選擇資料夾按鈕】
第二排：影片網址：【框框】 【取得影片資訊按鈕】
第三排：下載模式：【下載影片(選項)】【下載音訊(選項)】
       （下方緊接著顯示下載任務列表框框）
第四排：【清除任務列表按鈕】
第五排：若點選下載影片，顯示「影片畫質：」及畫質選項軸、「檔案格式：」及格式選項軸；
       若點選下載音訊，顯示「音訊品質：」及品質選項軸、「檔案格式：」及格式選項軸。
第六排：下載位置：【框框】 【選擇資料夾按鈕】
第七排：起始時間： 【時間框框】（可微調） 【時間選擇軸】 【顯示時間標籤】
第八排：結束時間： 【時間框框】（可微調） 【時間選擇軸】 【顯示時間標籤】
第九排：【加入任務按鈕】
排間：【日誌框框】（與下載狀態整合）
第十排：【開始批量下載按鈕】 【進度條】
------------------------------------------------------------
使用前請確認：
  1. 系統中已安裝 FFmpeg，並於第一排中指定 FFmpeg.exe 所在資料夾之絕對路徑（例如 C:\ffmpeg\bin）。
  2. 已安裝 yt-dlp 與 PyQt5 套件（pip install yt-dlp PyQt5）。
------------------------------------------------------------
未來預計優化:
1.按鈕顏色彩新綠對比色
2.GT既有項目+中英read.me
"""

import sys, os, subprocess, traceback
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QFileDialog, QRadioButton, QSlider,
    QTimeEdit, QListWidget, QGroupBox, QStackedWidget, QTextEdit, QProgressBar
)
from PyQt5.QtCore import Qt, QTime, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QFont
import yt_dlp

# -------------------------------------------------
# 定義單筆下載任務資料類別
class DownloadTask:
    def __init__(self, url, mode, video_quality, video_format, audio_quality, audio_format,
                 download_dir, start_time, end_time):
        self.url = url.strip()
        self.mode = mode  # "video" 或 "audio"
        self.video_quality = video_quality  # 如 "最高", "720p", "480p", "360p"
        self.video_format = video_format      # 如 "mp4", "mkv", "效率(webm)"
        self.audio_quality = audio_quality    # 如 "128K", "256K"
        self.audio_format = audio_format      # 如 "mp3", "wav", "效率(webm)"
        self.download_dir = download_dir.strip()
        self.start_time = start_time  # QTime 物件
        self.end_time = end_time      # QTime 物件
        self.duration = None          # 影片總秒數
        self.filename = None          # 下載完成後的檔案名稱

# -------------------------------------------------
# Worker 線程：逐筆處理下載任務
class DownloadWorker(QThread):
    progress_signal = pyqtSignal(int, str)  # 傳送百分比與狀態文字
    task_finished = pyqtSignal(str)         # 任務完成後傳回訊息

    def __init__(self, task: DownloadTask, ffmpeg_path, parent=None):
        super().__init__(parent)
        self.task = task
        self.ffmpeg_path = ffmpeg_path  # 使用者指定的 FFmpeg.exe 所在資料夾（絕對路徑）
        self.error = None

    def run(self):
        try:
            # 取得影片資訊，用以獲取影片長度與標題
            ydl_opts_info = {'quiet': True, 'skip_download': True}
            with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
                info = ydl.extract_info(self.task.url, download=False)
            total_sec = info.get('duration', 0)
            self.task.duration = total_sec

            # 設定 yt-dlp 選項
            outtmpl = os.path.join(self.task.download_dir, '%(title)s.%(ext)s')
            ydl_opts = {
                'outtmpl': outtmpl,
                'ffmpeg_location': self.ffmpeg_path,
                'progress_hooks': [self.ydl_hook],
                'noplaylist': True,
                'quiet': True,
            }
            # 根據下載模式及種類分別設定
            if self.task.mode == "audio":
                if self.task.audio_format == "效率(webm)":
                    ydl_opts['format'] = 'bestaudio/best'
                else:
                    ydl_opts['format'] = 'bestaudio/best'
                    if self.task.audio_format.lower() == 'mp3':
                        ydl_opts['postprocessors'] = [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3'
                        }]
                        ydl_opts['postprocessor_args'] = ['-b:a', '128k'] if self.task.audio_quality == '128K' else ['-b:a', '256k']
                    elif self.task.audio_format.lower() == 'wav':
                        ydl_opts['postprocessors'] = [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'wav'
                        }]
            else:  # video 模式
                if self.task.video_format == "效率(webm)":
                    ydl_opts['format'] = 'bestvideo+bestaudio/best'
                else:
                    if self.task.video_quality == "最高":
                        ydl_opts['format'] = 'bestvideo+bestaudio/best'
                    else:
                        quality_value = self.task.video_quality.replace("p", "")
                        ydl_opts['format'] = f'bestvideo[height<={quality_value}]+bestaudio/best'
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': self.task.video_format
                    }]
                    ydl_opts['merge_output_format'] = self.task.video_format

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.task.url])

            # 取得預期檔名，利用 prepare_filename 並根據目標格式更換副檔名（若非效率(webm)）
            downloaded_file = ydl.prepare_filename(info)
            if self.task.mode == "video":
                if self.task.video_format != "效率(webm)":
                    base, _ = os.path.splitext(downloaded_file)
                    downloaded_file = base + "." + self.task.video_format
            else:
                if self.task.audio_format != "效率(webm)":
                    base, _ = os.path.splitext(downloaded_file)
                    downloaded_file = base + "." + self.task.audio_format
            self.task.filename = downloaded_file

            # 若使用者設定剪輯區段（非全長下載），則利用 FFmpeg 裁切
            start_sec = self.qtime_to_seconds(self.task.start_time)
            end_sec = self.qtime_to_seconds(self.task.end_time)
            need_trim = (start_sec > 0) or (end_sec < total_sec)
            if need_trim:
                if not os.path.exists(downloaded_file):
                    raise Exception(f"下載檔案不存在：{downloaded_file}")
                base, ext = os.path.splitext(downloaded_file)
                trimmed_file = f"{base}_clip{ext}"
                self.progress_signal.emit(0, f"開始剪輯：{info.get('title', 'video')}")
                cmd = [
                    os.path.join(self.ffmpeg_path, "ffmpeg.exe"),
                    "-y",
                    "-i", downloaded_file,
                    "-ss", self.format_time(start_sec),
                    "-to", self.format_time(end_sec),
                    "-c", "copy",
                    trimmed_file
                ]
                subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if os.path.exists(trimmed_file):
                    try:
                        if os.path.exists(downloaded_file):
                            os.remove(downloaded_file)
                    except Exception:
                        pass
                    self.task.filename = trimmed_file
                    self.progress_signal.emit(100, f"剪輯完成：{trimmed_file}")
                else:
                    raise Exception("剪輯後檔案不存在，請檢查 FFmpeg 設定。")
            self.task_finished.emit(f"下載完成：{self.task.filename}")
        except Exception as e:
            self.error = traceback.format_exc()
            self.task_finished.emit(f"錯誤：{str(e)}")

    def ydl_hook(self, d):
        if d.get('status') == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded = d.get('downloaded_bytes', 0)
            percent = int(downloaded / total * 100) if total else 0
            self.progress_signal.emit(percent, f"下載中：{percent}%")
        elif d.get('status') == 'finished':
            self.progress_signal.emit(100, "下載完成，等待後製處理...")

    @staticmethod
    def qtime_to_seconds(qtime: QTime):
        return qtime.hour() * 3600 + qtime.minute() * 60 + qtime.second()

    @staticmethod
    def format_time(seconds: int):
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

# -------------------------------------------------
# 主介面
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("影音批量下載器")
        self.resize(1100, 750)
        self.setMinimumSize(QSize(1000, 700))
        font = QFont()
        font.setPointSize(14)
        self.setFont(font)
        self.tasks = []     # 儲存 DownloadTask 任務列表
        self.worker = None  # 當前執行的 worker
        # 先定義 status_label 以避免在 load_video_info 中引用錯誤
        self.status_label = QLabel("狀態：待命")
        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # 第一排: FFMPEG路徑
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("FFMPEG路徑:"))
        self.ffmpeg_path_input = QLineEdit("C:\\ffmpeg\\bin")
        row1.addWidget(self.ffmpeg_path_input)
        self.ffmpeg_browse_btn = QPushButton("選擇資料夾")
        self.ffmpeg_browse_btn.clicked.connect(self.choose_ffmpeg_folder)
        row1.addWidget(self.ffmpeg_browse_btn)
        main_layout.addLayout(row1)

        # 第二排: 影片網址與取得影片資訊
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("影片網址:"))
        self.url_input = QLineEdit()
        row2.addWidget(self.url_input)
        self.info_btn = QPushButton("取得影片資訊")
        self.info_btn.clicked.connect(self.load_video_info)
        row2.addWidget(self.info_btn)
        main_layout.addLayout(row2)

        # 第三排: 下載模式
        row3 = QHBoxLayout()
        row3.addWidget(QLabel("下載模式:"))
        self.radio_video = QRadioButton("下載影片")
        self.radio_audio = QRadioButton("下載音訊")
        self.radio_video.setChecked(True)
        self.radio_video.toggled.connect(self.switch_mode)
        row3.addWidget(self.radio_video)
        row3.addWidget(self.radio_audio)
        main_layout.addLayout(row3)

        # 下載任務列表框框
        task_list_group = QGroupBox("下載任務列表")
        task_list_layout = QVBoxLayout()
        self.task_list = QListWidget()
        task_list_layout.addWidget(self.task_list)
        task_list_group.setLayout(task_list_layout)
        main_layout.addWidget(task_list_group)

        # 第四排: 清除任務列表按鈕
        row4 = QHBoxLayout()
        self.clear_task_btn = QPushButton("清除任務列表")
        self.clear_task_btn.clicked.connect(lambda: self.task_list.clear())
        row4.addWidget(self.clear_task_btn)
        main_layout.addLayout(row4)

        # 第五排: 下載參數（依模式切換）
        self.stacked = QStackedWidget()
        # 影片參數版面
        video_widget = QWidget()
        video_layout = QHBoxLayout()
        video_layout.addWidget(QLabel("影片畫質:"))
        self.cb_video_quality = QComboBox()
        self.cb_video_quality.addItems(["最高", "1080p", "720p", "480p", "360p"])
        video_layout.addWidget(self.cb_video_quality)
        video_layout.addWidget(QLabel("檔案格式:"))
        self.cb_video_format = QComboBox()
        self.cb_video_format.addItems(["mp4", "mkv", "效率(webm)"])
        video_layout.addWidget(self.cb_video_format)
        video_widget.setLayout(video_layout)
        self.stacked.addWidget(video_widget)
        # 音訊參數版面
        audio_widget = QWidget()
        audio_layout = QHBoxLayout()
        audio_layout.addWidget(QLabel("音訊品質:"))
        self.cb_audio_quality = QComboBox()
        self.cb_audio_quality.addItems(["128K", "256K"])
        audio_layout.addWidget(self.cb_audio_quality)
        audio_layout.addWidget(QLabel("檔案格式:"))
        self.cb_audio_format = QComboBox()
        self.cb_audio_format.addItems(["mp3", "wav", "效率(webm)"])
        audio_layout.addWidget(self.cb_audio_format)
        audio_widget.setLayout(audio_layout)
        self.stacked.addWidget(audio_widget)
        main_layout.addWidget(self.stacked)

        # 第六排: 下載位置
        row6 = QHBoxLayout()
        row6.addWidget(QLabel("下載位置:"))
        self.loc_input = QLineEdit(os.path.join(os.getcwd(), "downloads"))
        row6.addWidget(self.loc_input)
        self.browse_btn = QPushButton("選擇資料夾")
        self.browse_btn.clicked.connect(self.choose_folder)
        row6.addWidget(self.browse_btn)
        main_layout.addLayout(row6)

        # 第七排: 起始時間 (時間框+滑桿+顯示標籤)
        row7 = QHBoxLayout()
        row7.addWidget(QLabel("起始時間:"))
        self.start_time_edit = QTimeEdit()
        self.start_time_edit.setDisplayFormat("HH:mm:ss")
        self.start_time_edit.setTime(QTime(0, 0, 0))
        row7.addWidget(self.start_time_edit)
        self.start_slider = QSlider(Qt.Horizontal)
        self.start_slider.setMinimum(0)
        self.start_slider.setMaximum(100)
        self.start_slider.setEnabled(False)
        row7.addWidget(self.start_slider)
        self.start_slider_label = QLabel("00:00:00")
        row7.addWidget(self.start_slider_label)
        self.start_slider.valueChanged.connect(self.start_slider_changed)
        main_layout.addLayout(row7)

        # 第八排: 結束時間 (時間框+滑桿+顯示標籤)
        row8 = QHBoxLayout()
        row8.addWidget(QLabel("結束時間:"))
        self.end_time_edit = QTimeEdit()
        self.end_time_edit.setDisplayFormat("HH:mm:ss")
        self.end_time_edit.setTime(QTime(0, 0, 0))
        row8.addWidget(self.end_time_edit)
        self.end_slider = QSlider(Qt.Horizontal)
        self.end_slider.setMinimum(0)
        self.end_slider.setMaximum(100)
        self.end_slider.setEnabled(False)
        row8.addWidget(self.end_slider)
        self.end_slider_label = QLabel("00:00:00")
        row8.addWidget(self.end_slider_label)
        self.end_slider.valueChanged.connect(self.end_slider_changed)
        main_layout.addLayout(row8)

        # 第九排: 加入任務按鈕
        row9 = QHBoxLayout()
        self.add_task_btn = QPushButton("加入任務")
        self.add_task_btn.clicked.connect(self.add_task)
        row9.addWidget(self.add_task_btn)
        main_layout.addLayout(row9)

        # 排間: 日誌框框 (與下載狀態整合)
        log_group = QGroupBox("日誌與下載狀態")
        log_layout = QVBoxLayout()
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        log_layout.addWidget(self.log_area)
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group)

        # 第十排: 開始批量下載按鈕與進度條 (使用先前定義的 self.status_label)
        row10 = QHBoxLayout()
        self.start_batch_btn = QPushButton("開始批量下載")
        self.start_batch_btn.clicked.connect(self.start_batch_download)
        row10.addWidget(self.start_batch_btn)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        row10.addWidget(self.progress_bar)
        row10.addWidget(self.status_label)
        main_layout.addLayout(row10)

        self.switch_mode()

    def choose_ffmpeg_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "選擇 FFmpeg 資料夾", self.ffmpeg_path_input.text())
        if folder:
            self.ffmpeg_path_input.setText(folder)

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "選擇下載資料夾", self.loc_input.text())
        if folder:
            self.loc_input.setText(folder)

    def load_video_info(self):
        url = self.url_input.text().strip()
        if not url:
            self.add_log("請先輸入影片網址！")
            return
        try:
            self.status_label.setText("狀態：讀取影片資訊...")
            ydl_opts = {'quiet': True, 'skip_download': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
            duration = info.get('duration', 0)
            self.add_log(f"影片長度：{duration} 秒")
            hours = duration // 3600
            minutes = (duration % 3600) // 60
            seconds = duration % 60
            self.end_time_edit.setTime(QTime(hours, minutes, seconds))
            self.start_slider.setMaximum(duration)
            self.end_slider.setMaximum(duration)
            self.start_slider.setEnabled(True)
            self.end_slider.setEnabled(True)
            self.start_slider.setValue(0)
            self.end_slider.setValue(duration)
            self.start_slider_changed(0)
            self.end_slider_changed(duration)
            self.status_label.setText("狀態：影片資訊取得成功！")
        except Exception as e:
            self.add_log(f"取得影片資訊失敗：{str(e)}")
            self.status_label.setText("狀態：取得影片資訊失敗！")

    def start_slider_changed(self, value):
        if value > self.end_slider.value():
            self.end_slider.setValue(value)
        h = value // 3600
        m = (value % 3600) // 60
        s = value % 60
        time_str = f"{h:02d}:{m:02d}:{s:02d}"
        self.start_slider_label.setText(time_str)
        self.start_time_edit.setTime(QTime(h, m, s))

    def end_slider_changed(self, value):
        if value < self.start_slider.value():
            self.start_slider.setValue(value)
        h = value // 3600
        m = (value % 3600) // 60
        s = value % 60
        time_str = f"{h:02d}:{m:02d}:{s:02d}"
        self.end_slider_label.setText(time_str)
        self.end_time_edit.setTime(QTime(h, m, s))

    def switch_mode(self):
        if self.radio_video.isChecked():
            self.stacked.setCurrentIndex(0)
        else:
            self.stacked.setCurrentIndex(1)

    def add_task(self):
        url = self.url_input.text().strip()
        if not url:
            self.add_log("請輸入影片網址！")
            return
        download_dir = self.loc_input.text().strip()
        if not os.path.exists(download_dir):
            os.makedirs(download_dir, exist_ok=True)
        mode = "video" if self.radio_video.isChecked() else "audio"
        task = DownloadTask(
            url=url,
            mode=mode,
            video_quality=self.cb_video_quality.currentText(),
            video_format=self.cb_video_format.currentText(),
            audio_quality=self.cb_audio_quality.currentText(),
            audio_format=self.cb_audio_format.currentText(),
            download_dir=download_dir,
            start_time=self.start_time_edit.time(),
            end_time=self.end_time_edit.time()
        )
        self.tasks.append(task)
        item_text = f"[{mode.upper()}] {url}"
        self.task_list.addItem(item_text)
        self.add_log(f"已加入任務：{item_text}")
        self.url_input.clear()

    def start_batch_download(self):
        if not self.tasks:
            self.add_log("沒有任務可下載！")
            return
        self.start_batch_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        self.add_log("開始批量下載...")
        self.total_tasks = len(self.tasks)
        self.completed_tasks = 0
        self.process_next_task()

    def process_next_task(self):
        if not self.tasks:
            self.add_log("所有任務已完成！")
            self.start_batch_btn.setEnabled(True)
            self.status_label.setText("狀態：全部任務完成")
            return
        self.current_task = self.tasks.pop(0)
        self.status_label.setText(f"狀態：下載 {self.current_task.url} ...")
        ffmpeg_abs = self.ffmpeg_path_input.text().strip()
        self.worker = DownloadWorker(self.current_task, ffmpeg_abs)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.task_finished.connect(self.task_finished)
        self.worker.start()

    def update_progress(self, percent, message):
        self.progress_bar.setValue(percent)
        self.status_label.setText(message)

    def task_finished(self, message):
        self.add_log(message)
        self.completed_tasks += 1
        overall = int(self.completed_tasks / (self.completed_tasks + len(self.tasks)) * 100)
        self.progress_bar.setValue(overall)
        self.task_list.addItem(f"完成：{self.current_task.url}")
        self.worker = None
        self.process_next_task()

    def add_log(self, text):
        self.log_area.append(text)
        print(text)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
