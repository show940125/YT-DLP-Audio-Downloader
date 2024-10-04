<a id="top"></a>

# YT-DLP Audio Downloader / YT-DLP 音频下载器

<div align="center">
<img src="image/YT-DLP.png" alt="App Icon" width="400"/>
</div>

YT-DLP Audio Downloader is a GUI application that allows users to download audio from YouTube videos. 
It is built using PyQt5 for the graphical user interface and yt-dlp for the downloading process, making it easy to extract audio from YouTube and save it in various formats.
Unlike other tools, YT-DLP Audio Downloader offers an intuitive interface, detailed status updates, and the ability to select specific time segments, making it a versatile and user-friendly choice for all types of users.

## 版本 / Versions

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
- [Creating an Installer](#creating-an-installer)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## English

### Features
- Download audio from YouTube videos in various formats (MP3, AAC, WAV, etc.).
- Supports downloading entire videos or selecting specific time segments.
- Customizable audio quality (128k, 192k, 256k, 320k).
- Displays download progress with detailed status updates (e.g., "Downloading", "Clipping", "Transcoding").
- User-friendly graphical interface built with PyQt5.

### Requirements
- Python 3.7 or later
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/download.html) (for audio extraction)
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
FFmpeg is required for audio extraction. You need to download and install it if it is not already available on your system.

1. Visit the [FFmpeg download page](https://ffmpeg.org/download.html).
2. Download the appropriate version for your operating system.
3. Extract the downloaded file and add the `bin` folder to your system's PATH.
   - **Windows**: Add the `ffmpeg\bin` directory to your system's environment variables.
   - **Linux/macOS**: Make sure the `ffmpeg` command is accessible from your terminal (e.g., by adding it to your `.bashrc` or `.zshrc` file).

   **Common Issues**: If you encounter issues with FFmpeg not being recognized, ensure that the `bin` folder is correctly added to your system's PATH. Restart your terminal or computer after making changes to environment variables. On Windows, double-check that you have edited the correct environment variable (`Path`) and that there are no typos.

To verify FFmpeg is correctly installed, run:
```sh
ffmpeg -version
```

#### Step 5: Run the Application
You can now run the application using the following command:
```sh
python main.py
```

### Usage
- **Load URLs**: Paste one or more YouTube URLs in the text box, with each URL on a new line.
- **Select Output Format**: Choose the desired audio format (e.g., MP3, AAC, WAV).
- **Select Quality**: Set the desired audio quality (e.g., 128k, 192k).
- **Specify Time Segments** (Optional): If you want to download specific parts of the video, select the URL, specify start and end times, and click "Add Segment".
- **Set Output Directory**: Select where the audio files will be saved.
- **Download**: Click the "Download" button to start downloading the audio.

### Packaging the Application
If you want to package this application into an executable file, you can use `PyInstaller`:

1. Install PyInstaller:
   ```sh
   pip install pyinstaller
   ```

2. Run the following command to create a standalone `.exe` file:
   ```sh
   pyinstaller --onefile --windowed --icon=app_icon.ico main.py
   ```
   The executable file will be located in the `dist` directory.

   **Note**: Packaging might require additional testing on different versions of Windows to ensure compatibility.

### Creating an Installer
*(Content for creating an installer can be added here if available.)*

### Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request. Contributions, issues, and feature requests are welcome!

### License
This project is licensed under the Apache-2.0 License. See the `LICENSE` file for details.

### Acknowledgments
- Thanks to [yt-dlp](https://github.com/yt-dlp/yt-dlp) for providing a powerful YouTube download utility.
- Thanks to the [FFmpeg](https://ffmpeg.org/) project for enabling audio extraction.

[Back to Top](#top)

---

### 中文
- [功能特性](#功能特性)
- [需求](#需求)
- [安裝](#安裝)
  - [步驟 1：克隆倉庫](#步驟-1克隆倉庫)
  - [步驟 2：建立虛擬環境（可選但推薦）](#步驟-2建立虛擬環境可選但推薦)
  - [步驟 3：安裝相依性](#步驟-3安裝相依性)
  - [步驟 4：安裝 FFmpeg](#步驟-4安裝-ffmpeg)
  - [步驟 5：運行應用程式](#步驟-5運行應用程式)
- [使用方法](#使用方法)
- [打包應用程式](#打包應用程式)
- [貢獻](#貢獻)
- [許可證](#許可證)
- [致謝](#致謝)

## 中文

### 功能特性
- 支援以多種格式（MP3、AAC、WAV 等）下載 YouTube 影片的音訊。
- 支援下載整個影片或選擇特定時間段。
- 可自訂音訊品質（128k、192k、256k、320k）。
- 顯示下載進度並提供詳細的狀態更新（例如「下載中」、「剪輯中」、「轉碼中」）。
- 使用 PyQt5 建構的使用者友好圖形介面。

### 需求
- Python 3.7 或更高版本
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/download.html)（用於音訊提取）
- PyQt5

### 安裝

#### 步驟 1：克隆倉庫
```sh
git clone https://github.com/show941025/YT-DLP-Audio-Downloader.git
cd YT-DLP-Audio-Downloader
```

#### 步驟 2：建立虛擬環境（可選但推薦）
建議建立虛擬環境來管理此專案的相依性。
```sh
python -m venv venv
source venv/bin/activate  # 在 Windows 上使用：venv\Scripts\activate
```

#### 步驟 3：安裝相依性
使用 `pip` 安裝所需的 Python 套件：
```sh
pip install -r requirements.txt
```
確保您的 `requirements.txt` 包含：
```
yt-dlp
PyQt5
```

#### 步驟 4：安裝 FFmpeg
FFmpeg 是進行音訊提取所必需的。如果系統中尚未安裝，需要下載並安裝它。

1. 前往 [FFmpeg 下載頁面](https://ffmpeg.org/download.html)。
2. 下載適用於您的作業系統的版本。
3. 解壓下載的檔案並將 `bin` 資料夾加入系統的 PATH。
   - **Windows**：將 `ffmpeg\bin` 目錄添加到系統環境變數中。
   - **Linux/macOS**：確保終端機可以存取 `ffmpeg` 指令（例如，通過將其添加到 `.bashrc` 或 `.zshrc` 檔案中）。

   **常見問題**：如果遇到 FFmpeg 無法識別的問題，請確保已正確將 `bin` 資料夾添加到系統的 PATH 中。在更改環境變數後，請重新啟動終端機或電腦。在 Windows 上，請仔細檢查是否編輯了正確的環境變數 (`Path`)，並確保沒有拼寫錯誤。

驗證 FFmpeg 是否正確安裝，請執行：
```sh
ffmpeg -version
```

#### 步驟 5：運行應用程式
您現在可以使用以下指令運行應用程式：
```sh
python main.py
```

### 使用方法
- **加載 URL**：在文字框中貼上一个或多個 YouTube URL，每個 URL 單獨一行。
- **選擇輸出格式**：選擇所需的音訊格式（例如，MP3、AAC、WAV）。
- **選擇品質**：設定所需的音訊品質（例如，128k、192k）。
- **指定時間段**（可選）：如果您只想下載影片的特定部分，選擇 URL，指定開始和結束時間，然後點擊「添加段落」。
- **設定輸出目錄**：選擇音訊檔案的保存位置。
- **下載**：點擊「下載」按鈕開始下載音訊。

### 打包應用程式
如果您想將此應用程式打包成可執行檔，可以使用 `PyInstaller`：

1. 安裝 PyInstaller：
   ```sh
   pip install pyinstaller
   ```

2. 執行以下指令以建立獨立的 `.exe` 檔：
   ```sh
   pyinstaller --onefile --windowed --icon=app_icon.ico main.py
   ```
   可執行檔將位於 `dist` 目錄中。

   **注意**：打包可能需要在不同版本的 Windows 上進行額外測試以確保相容性。

### 貢獻
如果您想為本專案做出貢獻，請先 Fork 倉庫，然後提交 Pull Request。歡迎貢獻程式碼、報告問題和提出功能請求！

### 許可證
本專案採用 Apache-2.0 許可證。詳情請參閱 `LICENSE` 檔案。

### 致謝
- 感謝 [yt-dlp](https://github.com/yt-dlp/yt-dlp) 提供了強大的 YouTube 下載工具。
- 感謝 [FFmpeg](https://ffmpeg.org/) 專案，使音訊提取成為可能。

[返回頂部](#top)
