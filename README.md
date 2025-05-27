# Transcribe Capture for macOS  
**再生中の音声をそのまま聞きながら、リアルタイムで文字起こしを行うPythonアプリ**

---

## ✅ 概要

このアプリは、macOS上で再生されている音声（例：YouTube動画）を、自分で聞きながら文字起こしできるCLIツールです。  
仮想オーディオデバイス「BlackHole」と、OpenAIの音声認識モデル「Whisper」を使用します。

---

## 🛠 必要な環境

- macOS（Apple Silicon M1/M2 対応）
- Python 3.10 以上
- [BlackHole 2ch](https://github.com/ExistentialAudio/BlackHole)（仮想オーディオドライバ）

---

## ⚙️ BlackHoleの設定手順

### 1. 複数出力装置の作成（Audio MIDI設定）

1. Finder > アプリケーション > ユーティリティ > **Audio MIDI設定** を開く  
2. 左下の「＋」から「複数出力装置」を作成  
3. 「MacBookのスピーカー」＋「BlackHole 2ch」をチェック  
4. 右クリックで「主出力」に設定

### 2. 入力デバイスの設定

- システム設定 > サウンド > 入力  
- 入力デバイスを **BlackHole 2ch** に変更

> これにより、自分で音声を聞きながら、同時に録音・文字起こしが可能になります。

---

## 🐍 仮想環境の作成とライブラリのインストール

```bash
cd ~/Desktop
mkdir transcribe
cd transcribe

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install numpy scipy sounddevice git+https://github.com/openai/whisper.git
```

▶️ アプリの実行
```bash
python capture_and_transcribe.py
```
上記スクリプトを実行した状態で、YouTubeなどで音声を再生すると、自動的に文字起こしが始まります。

---

📁 出力仕様

実行フォルダ内に自動で出力フォルダが作成され、.txt 形式で文字起こしファイルが保存されます。

ファイル名は実行日時ベースです（例：2025-05-21_141500.txt）

---

📌 注意点

音声ソースは「スピーカー出力」として再生される必要があります。

Whisperは初回実行時にモデルファイルをダウンロードします（数百MB程度）。

---

🤝 ライセンス・著作権

Whisper: MIT License

本スクリプトは個人の学習・研究目的で作成されたものです。

---

# Transcribe Capture for macOS
**A Python app that transcribes audio in real time while listening to it**

---

## ✅ Overview

This app is a CLI tool that allows you to transcribe audio (e.g. YouTube videos) being played on macOS while listening to it yourself.
It uses the virtual audio device "BlackHole" and OpenAI's speech recognition model "Whisper".

---

## 🛠 Required environment

- macOS (Apple Silicon M1/M2 compatible)

- Python 3.10 or later

- [BlackHole 2ch](https://github.com/ExistentialAudio/BlackHole) (Virtual audio driver)

---

## ⚙️ BlackHole setup procedure

### 1. Create a multiple output device (Audio MIDI Setup)

1. Open Finder > Applications > Utilities > **Audio MIDI Setup**
2. Create a "Multiple Output Device" from the "+" in the lower left
3. Check "MacBook Speakers" + "BlackHole 2ch"
4. Right-click to set as "Main Output"

### 2. Input device settings

- System Preferences > Sound > Input
- Change the input device to **BlackHole 2ch**

> This allows you to record and transcribe audio while listening to it yourself.

---

## 🐍 Create a virtual environment and install libraries

```bash
cd ~/Desktop
mkdir transcribe
cd transcribe

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install numpy scipy sounddevice git+https://github.com/openai/whisper.git
```

▶️ Run the app
```bash
python capture_and_transcribe.py
```
When the above script is executed, play audio on YouTube etc. and transcription will start automatically.

---

📁 Output specifications

An output folder is automatically created in the execution folder and the transcription file is saved in .txt format.

The file name is based on the execution date and time (e.g. 2025-05-21_141500.txt)

---

📌 Notes

The audio source must be played as "speaker output".

Whisper downloads a model file the first time it is run (about several hundred MB).

---

🤝 License and Copyright

Whisper: MIT License

This script was created for personal study and research purposes.
