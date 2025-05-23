import os
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import whisper
import threading
from datetime import datetime

# サンプルレートと録音時間（秒）
SAMPLE_RATE = 44100  # 標準的なサンプルレート
SEGMENT_DURATION = 60  # 1分ごとにファイルを保存
SILENCE_THRESHOLD = 0.01  # 無音と見なす閾値（振幅の絶対値）
SILENCE_DURATION = 30  # 無音が30秒続いたら終了

# 使用するデバイスのIDとチャンネル数（BlackHole 64ch）
DEVICE_ID = 0  # BlackHole 64ch
device_info = sd.query_devices(DEVICE_ID, 'input')
CHANNELS = min(2, device_info['max_input_channels'])  # 2ch録音（なければ1ch）

# Whisperモデルのロード
model = whisper.load_model("base")

# 録音完了を知らせるフラグ
recording_finished = threading.Event()
audio_data = []
silent_duration = 0  # 無音状態が続いている時間

# 録音終了時間でフォルダを作成する関数
def create_directory_with_timestamp():
    now = datetime.now()
    folder_name = now.strftime("%Y-%m-%d_%H-%M-%S")  # タイムスタンプでフォルダを作成
    os.makedirs(folder_name, exist_ok=True)  # フォルダ作成
    return folder_name

# 録音のコールバック関数
def callback(indata, frames, time, status):
    global silent_duration
    if status:
        print(status)
    audio_data.append(indata.copy())
    
    # 入力データの振幅をチェックして無音を検知
    if np.abs(indata).mean() < SILENCE_THRESHOLD:
        silent_duration += frames / SAMPLE_RATE  # 無音時間を加算
    else:
        silent_duration = 0  # 音があれば無音カウンタをリセット

    # 無音が規定時間続いたら録音終了
    if silent_duration > SILENCE_DURATION:
        print(f"無音が{SILENCE_DURATION}秒続いたため、録音を停止します。")
        recording_finished.set()

# 話者名を手動で挿入しやすくする空白を挿入する関数
def insert_speaker_placeholder(transcription_text):
    lines = transcription_text.split('\n')  # テキストを行ごとに分割
    result = []

    for line in lines:
        # 各段落の前に空の話者名を挿入
        result.append(line)
        result.append("\n(Speaker Name)\n")  # 話者名のための空白を挿入

    return '\n'.join(result)

# テキストファイルを1つにまとめる関数
def combine_text_files(folder_name, output_filename):
    with open(output_filename, 'w') as outfile:
        for i in range(1, len(os.listdir(folder_name)) // 2 + 1):  # ファイル数に基づくループ
            transcription_filename = os.path.join(folder_name, f'transcription_{i}.txt')
            if os.path.exists(transcription_filename):
                with open(transcription_filename, 'r') as infile:
                    outfile.write(infile.read() + "\n")
    print(f"テキストファイルが {output_filename} にまとめられました。")

# 録音開始
print(f"録音を開始します... デバイス: {DEVICE_ID}, チャンネル: {CHANNELS}")
stream = sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, device=DEVICE_ID, callback=callback)
   
with stream:
    folder_name = create_directory_with_timestamp()  # フォルダを作成
    print(f"フォルダ '{folder_name}' にファイルを保存します。")
    
    segment_count = 0  # セグメント数のカウンタ
    while not recording_finished.is_set():
        recording_finished.wait(timeout=SEGMENT_DURATION)  # 1分ごとに待機
        segment_count += 1

        # 音声データを結合して保存
        audio_array = np.concatenate(audio_data)
        wav_filename = os.path.join(folder_name, f'captured_audio_{segment_count}.wav')
        wav.write(wav_filename, SAMPLE_RATE, audio_array)
        print(f"{wav_filename}に保存しました。")

        # Whisperで文字起こし（進捗表示を有効化）
        print(f"Whisperで文字起こし中... {wav_filename}")
        result = model.transcribe(wav_filename, verbose=True)  # 文字起こし結果を取得
        transcription_text = result['text']  # テキストを取得

        # 手動で話者名を挿入しやすくするための空白を挿入
        final_transcription = insert_speaker_placeholder(transcription_text)

        print(f"文字起こし結果 ({wav_filename}):")
        print(final_transcription)

        # 文字起こし結果をファイルに保存
        transcription_filename = os.path.join(folder_name, f'transcription_{segment_count}.txt')
        with open(transcription_filename, 'w') as f:
            f.write(final_transcription)

        # 1分間の録音が終わったのでデータをクリア
        audio_data.clear()

# すべての文字起こしテキストファイルを1つにまとめる
final_output_filename = os.path.join(folder_name, 'combined_transcription.txt')
combine_text_files(folder_name, final_output_filename)

print("録音と文字起こしが完了しました。")
