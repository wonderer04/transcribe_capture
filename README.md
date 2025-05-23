# transcribe_capture
#主な機能はmacで再生している音声をmacのスピーカーで自分でも聞きながら文字起こしを行えるというアプリです。

#事前にblackholeをインストールの上、下記設定が必要です。

Audio MIDI設定で「複数出力装置」を作る
Finder > アプリケーション > ユーティリティ > Audio MIDI設定 を開く。

左下の「＋」ボタン > 「複数出力装置」を作成。

使用する出力を選択（例: MacBookのスピーカー + BlackHole 2ch　blackhole_2chインストールの場合）

これを「主出力」に設定する（右クリックで設定可能）。

こうすることで、自分にも音が聞こえながら、BlackHoleにも音が流れます。

システム環境設定 ＞ サウンド ＞ 入力 を BlackHole に設定
「入力」タブを開く

BlackHole 2ch　を選択

これで、Macの再生音が仮想的に「マイク入力」として扱われます。

ターミナルから下記コード使用

cd ~/Desktop

mkdir transcribe

cd transcribe
#デスクトップに作成したtranscribeフォルダ内に移動。ソースコードファイルはこのフォルダ内に配置

python3 -m venv venv
#仮想環境を作成（仮想環境名venv)

source venv/bin/activate
#仮想環境の起動


pip install --upgrade pip
pip install numpy scipy sounddevice git+https://github.com/openai/whisper.git
#必要なライブラリをインストール

python capture_and_transcribe.py

#ソースコードファイルcapture_and_transcribe.pyを実行。ブラウザなどで会話のある動画または音声ファイル再生

#ソースコードのあるフォルダ内にフォルダを作成、文字起こしされたテキストファイルが作成されます。
