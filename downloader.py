# downloader.py
import yt_dlp
import os
from PyQt5.QtCore import QObject, pyqtSignal
import uuid  # 引入uuid用于生成唯一标识符

class Downloader(QObject):
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
    
    def download_audio(self, url, audio_format, quality, segments, output_dir):
        try:
            if segments:
                for idx, (start, end) in enumerate(segments):
                    self.status.emit(f"下載中: 分段 {idx + 1}")
                    unique_id = uuid.uuid4().hex
                    start_clean = start.replace(':', '-')
                    end_clean = end.replace(':', '-')
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': os.path.join(output_dir, f"%(title)s_segment{idx + 1}_{start_clean}_to_{end_clean}_{unique_id}.%(ext)s"),
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': audio_format,
                            'preferredquality': quality.rstrip('k'),
                        }],
                        'quiet': True,
                        'no_warnings': True,
                        'progress_hooks': [self.hook],
                        'postprocessor_args': [
                            '-ss', start,
                            '-to', end
                        ],
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
            else:
                self.status.emit("下載中: 完整音檔")
                unique_id = uuid.uuid4().hex
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': os.path.join(output_dir, f"%(title)s_{unique_id}.%(ext)s"),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': audio_format,
                        'preferredquality': quality.rstrip('k'),
                    }],
                    'quiet': True,
                    'no_warnings': True,
                    'progress_hooks': [self.hook],
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
        except Exception as e:
            self.status.emit(f"下載失敗: {str(e)}")
    
    def hook(self, d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes', 1)
            downloaded_bytes = d.get('downloaded_bytes', 0)
            percentage = int(downloaded_bytes / total_bytes * 100)
            self.status.emit(f"下載中: {percentage}%")
            self.progress.emit(percentage)
        elif d['status'] == 'finished':
            self.status.emit("轉檔中: 完成下載，轉檔完成")
