# transcribe_capture
cd ~/Desktop
mkdir transcribe
cd transcribe
#デスクトップに作成したtranscribeフォルダにソースコードファイルを配置

python3 -m venv venv
#仮想環境を作成（仮想環境名venv)

source venv/bin/activate
#仮想環境の起動


pip install --upgrade pip
pip install numpy scipy sounddevice git+https://github.com/openai/whisper.git
#必要なライブラリを下記コードでインストール
