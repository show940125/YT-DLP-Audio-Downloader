<a id="top"></a>

# YT-DLP Downloader / YT-DLP 下載器

<div align="center">
<img src="image/YT-DLP.png" alt="App Icon" width="400"/>
</div>

YT-DLP Downloader is a GUI application that allows users to download both video and audio from YouTube and other supported platforms.  
Built with PyQt5 for a modern, vertically‐arranged interface and powered by yt-dlp for the download process, this application provides flexible options to download content in various formats.  
It also offers an “Efficiency (webm)” mode for both video and audio downloads, which directly downloads the original webm streams for a faster process without post‐processing.

<div align="center">
<img src="image/YT-DLP UI.png" alt="App Icon" width="800"/>
  
  Sample UI – a clean, vertically arranged interface
</div>

## Versions

- [English](#english)
- [中文](#中文)

## Table of Contents / 目录

### English
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
  - [Step 1: Clone the Repository](#step-1-clone-the-repository)
  - [Step 2: Create a Virtual Environment (Optional but Recommended)](#step-2-create-a-virtual-environment-optional-but-recommended)
  - [Step 3: Install Dependencies](#step-3-install-dependencies)
  - [Step 4: Install FFmpeg](#step-4-install-ffmpeg)
  - [Step 5: Run the Application](#step-5-run-the-application)
- [Usage](#usage)
- [Packaging the Application](#packaging-the-application)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## English

### Features
- **Download Video and Audio:** Choose to download either full videos or extract audio from YouTube and supported sites.
- **Efficiency (webm) Mode:** For both video and audio downloads, select the “Efficiency (webm)” option to directly download the original webm streams for faster downloads without conversion.
- **Customizable Quality:** 
  - For videos: Select “最高” (best quality) or set a maximum resolution (720p, 480p, 360p).
  - For audio: Choose between 128K and 256K quality when converting to MP3; WAV outputs remain lossless.
- **Time Segment Selection:** Easily specify start and end times using an intuitive vertical layout that includes both QTimeEdit fields with up/down adjustments and horizontal sliders.
- **Clean Vertical UI Layout:** The user interface is arranged in a clear, vertical order.
- **Detailed Status Updates:** The application shows real-time download progress and status messages (e.g., “Downloading…”, “Clipping…”, “Transcoding…”).

### Requirements
- Python 3.7 or later
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/download.html) (FFmpeg must be installed on your system; you will need to specify its absolute path in the application)
- PyQt5

### Installation

#### Step 1: Clone the Repository
```sh
git clone https://github.com/show941025/YT-DLP-Audio-Downloader.git
cd YT-DLP-Audio-Downloader
```

#### Step 2: Create a Virtual Environment (Optional but Recommended)
It is recommended to create a virtual environment to manage the dependencies for this project.
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Step 3: Install Dependencies
Install the required Python packages using `pip`:
```sh
pip install -r requirements.txt
```
Make sure your `requirements.txt` includes:
```
yt-dlp
PyQt5
```

#### Step 4: Install FFmpeg
FFmpeg is required for post-processing (video conversion and audio extraction). Follow these steps:
1. Visit the [FFmpeg download page](https://ffmpeg.org/download.html) and download the appropriate version for your operating system.
2. Extract the downloaded file.
3. **Important:** Add the `bin` folder (e.g., `C:\ffmpeg\bin`) to your system's PATH, or note its absolute path. You will need to enter this absolute path in the application.

To verify FFmpeg is correctly installed, run:
```sh
ffmpeg -version
```

#### Step 5: Run the Application
Run the application with:
```sh
python main.py
```

### Usage
1. **FFmpeg Path:** In the first row, enter the absolute path to the FFmpeg folder (e.g., `C:\ffmpeg\bin`) and click "Choose Folder" if needed.
2. **Video URL:** In the second row, enter the video URL and click “Get Video Info” to load video details.
3. **Download Mode:** In the third row, select either “Download Video” or “Download Audio.”
4. **Task List:** The current download tasks are displayed in a dedicated list. You can clear the list with the "Clear Task List" button.
5. **Quality and Format Settings:** 
   - For video downloads, the settings row shows “Video Quality” (options: “最高”, “720p”, “480p”, “360p”, “效率(webm)”) and “File Format” (options: “mp4”, “mkv”, “效率(webm)”).
   - For audio downloads, it shows “Audio Quality” (options: “128K”, “256K”, “效率(webm)”) and “File Format” (options: “mp3”, “wav”, “效率(webm)”).
6. **Download Location:** In the sixth row, set the download location and choose a folder.
7. **Time Segment Selection:** 
   - **Start Time:** In the seventh row, specify the start time using a time field (with up/down adjustments) and a horizontal slider.
   - **End Time:** In the eighth row, specify the end time in a similar fashion.
8. **Add Task:** Click the “Add Task” button (ninth row) to add the current settings as a new download task.
9. **Logs:** The log area displays integrated download status and messages. You can clear the logs with the "Clear Log" button.
10. **Batch Download:** In the tenth row, click “Start Batch Download” to process all tasks. A progress bar shows overall progress.

### Packaging the Application
To package the application into an executable using PyInstaller:

1. Install PyInstaller:
   ```sh
   pip install pyinstaller
   ```

2. Package the application:
   ```sh
   pyinstaller --onefile --windowed --icon=app_icon.ico main.py
   ```
   The executable will be located in the `dist` directory.

   **Note:** Ensure FFmpeg is installed or that you correctly specify its absolute path on the target system.

### Contributing
Contributions, bug reports, and feature requests are welcome! Please fork the repository and submit a pull request.

### License
This project is licensed under the Apache-2.0 License. See the `LICENSE` file for details.

### Acknowledgments
- Thanks to [yt-dlp](https://github.com/yt-dlp/yt-dlp) for the powerful download engine.
- Thanks to the [FFmpeg](https://ffmpeg.org/) project for providing essential media processing capabilities.

[Back to Top](#top)

---

### 中文

### 功能特性
- **影片與音訊下載：** 使用者可以選擇下載完整影片或從 YouTube 等平台提取音訊。
- **效率(webm)模式：** 在影片與音訊下載中，提供「效率(webm)」選項，直接下載原始 webm 串流以達到快速下載的目的，不進行後製轉檔。
- **自訂品質：**  
  - **影片：** 可選擇「最高」或指定最大解析度（720p、480p、360p）。
  - **音訊：** 選擇 128K 或 256K 品質（MP3轉換時），WAV 為無損格式；另有「效率(webm)」選項。
- **時間段選擇：** 直排式介面中，使用者可分別設定起始與結束時間（透過時間框及滑桿），輕鬆選擇下載區段。
- **直排式 UI：**  如附圖。
- **詳細狀態更新：** 顯示實時下載進度與狀態訊息（如「下載中」、「剪輯中」、「轉碼中」）。

### 需求
- Python 3.7 或更高版本
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/download.html)（用於影片轉檔與音訊提取）
- PyQt5

### 安裝

#### 步驟 1：克隆倉庫
```sh
git clone https://github.com/show941025/YT-DLP-Audio-Downloader.git
cd YT-DLP-Audio-Downloader
```

#### 步驟 2：建立虛擬環境（可選但推薦）
```sh
python -m venv venv
source venv/bin/activate  # Windows 上使用：venv\Scripts\activate
```

#### 步驟 3：安裝相依性
```sh
pip install -r requirements.txt
```
確保 `requirements.txt` 包含：
```
yt-dlp
PyQt5
```

#### 步驟 4：安裝 FFmpeg
1. 前往 [FFmpeg 下載頁面](https://ffmpeg.org/download.html) 下載適合的版本。
2. 解壓後，將 `bin` 資料夾的路徑（如 `C:\ffmpeg\bin`）記下，並在應用程式中指定該絕對路徑。

#### 步驟 5：運行應用程式
```sh
python main.py
```

### 使用方法
1. **FFmpeg 路徑：** 在第一排輸入 FFmpeg 所在資料夾的絕對路徑，或使用「選擇資料夾」按鈕選擇。
2. **影片網址：** 輸入影片網址並點選「取得影片資訊」以獲取影片長度資訊。
3. **下載模式：** 選擇「下載影片」或「下載音訊」。
4. **任務列表：** 系統會顯示所有加入的任務，並可透過「清除任務列表」按鈕清空列表。
5. **畫質/音質設定：** 根據所選模式，自動顯示：
   - 下載影片時，可選擇「影片畫質」（包括「效率(webm)」選項）及「檔案格式」。
   - 下載音訊時，可選擇「音訊品質」（包括「效率(webm)」選項）及「檔案格式」。
6. **下載位置：** 設定存放檔案的下載位置。
7. **時間段設定：** 分別設定起始與結束時間（可使用時間框及滑桿調整）。
8. **加入任務：** 點選「加入任務」以將當前設定加入任務列表。
9. **日誌與狀態：** 日誌框會顯示下載進度與狀態訊息，可使用「清除日誌」按鈕清空。
10. **開始批量下載：** 點選「開始批量下載」以依序處理所有任務，進度條將顯示整體進度。

### 打包應用程式
使用 PyInstaller 將應用程式打包成獨立執行檔：
1. 安裝 PyInstaller：
   ```sh
   pip install pyinstaller
   ```
2. 執行以下指令：
   ```sh
   pyinstaller --onefile --windowed --icon=app_icon.ico main.py
   ```
生成的可執行檔會位於 `dist` 目錄中。

### 貢獻
歡迎提交 issue、報告錯誤或提交 pull request。請先 Fork 倉庫，再提交修改。

### 許可證
本專案採用 Apache-2.0 許可證。詳情請參閱 `LICENSE` 檔案。

### 致謝
- 感謝 [yt-dlp](https://github.com/yt-dlp/yt-dlp) 為本專案提供強大的下載引擎。
- 感謝 [FFmpeg](https://ffmpeg.org/) 使音訊與影片處理成為可能。

[返回頂部](#top)
