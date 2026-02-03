# 🎬 YouTube Video & Audio Downloader (yt-dlp + FFmpeg)

This project is a Python-based utility for downloading **full YouTube videos**, **audio-only files**, and optionally **trimming** them using time ranges. It leverages **yt-dlp** for downloading and **FFmpeg** for video/audio processing.

> ⚠️ **Disclaimer**: This tool is for educational and personal use only. Always respect YouTube’s Terms of Service and copyright laws.

---

## ✨ Features

* Download full YouTube videos as MP4
* Download audio-only (MP3 or M4A)
* Optional trimming using start/end timestamps
* Automatically creates an `output/` directory
* Supports Shorts, standard videos, and playlists (playlist download disabled by default)

---

## 📦 Requirements

### System Requirements

* **Python 3.9+**
* **FFmpeg** (must be available in your system PATH)

### Python Packages

* `yt-dlp`

---

## 🛠 Environment Setup

### 1️⃣ Clone or Download the Project

```bash
git clone <your-repo-url>
cd <project-folder>
```

Or simply place the Python file in a directory of your choice.

---

### 2️⃣ Create a Virtual Environment (Recommended)

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3️⃣ Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Install FFmpeg

FFmpeg is **required** for trimming and audio conversion.

#### macOS (Homebrew)

```bash
brew install ffmpeg
```

#### Ubuntu / Debian

```bash
sudo apt update
sudo apt install ffmpeg
```

#### Windows

1. Download FFmpeg from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Extract it
3. Add the `bin` folder to your **System PATH**
4. Verify installation:

```bash
ffmpeg -version
```

---

## ▶️ How to Run

Run the script directly:

```bash
python main.py
```

(Replace `main.py` with your file name if different.)

---

## 🧪 Usage Examples

### Download Full Video

```python
download_full_video("https://www.youtube.com/watch?v=VIDEO_ID")
```

### Download & Trim Video

```python
download_full_video(
    video_url="https://www.youtube.com/watch?v=VIDEO_ID",
    start_time="00:01:30",
    end_time="00:02:00"
)
```

---

### Download Audio Only (MP3)

```python
download_audio_only(
    video_url="https://www.youtube.com/watch?v=VIDEO_ID",
    output_format="mp3"
)
```

### Download & Trim Audio

```python
download_audio_only(
    video_url="https://www.youtube.com/watch?v=VIDEO_ID",
    output_format="mp3",
    start_time="00:00:10",
    end_time="00:00:30"
)
```

---

## 📂 Output Structure

```
project-root/
│
├── output/
│   ├── Video Title.mp4
│   ├── Video Title_trimmed.mp4
│   ├── Video Title.mp3
│
├── main.py
├── requirements.txt
└── README.md
```

---

## ❗ Common Issues

### ❌ `ffmpeg: command not found`

➡️ FFmpeg is not installed or not in PATH.

### ❌ YouTube blocked the request

* Try again later
* Change network/IP
* Update yt-dlp:

```bash
pip install -U yt-dlp
```

---

## 🔒 Notes & Best Practices

* Use reasonable `sleep_interval` values (already included)
* Avoid excessive downloads
* Keep yt-dlp updated

---

## 📜 License

MIT License (or update as needed)

---

## 🙌 Credits

* [yt-dlp](https://github.com/yt-dlp/yt-dlp)
* [FFmpeg](https://ffmpeg.org/)

