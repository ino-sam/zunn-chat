import json
import requests
import simpleaudio as sa
import io
import wave
import os

HOST = os.environ.get('VOICEVOX_HOST', 'localhost')
PORT = int(os.environ.get('VOICEVOX_PORT', 50021))

def generate_audio_query(text, speaker=1):
    """
    音声合成のためのクエリを生成する。

    Args:
        text (str): 合成するテキスト。
        speaker (int): 話者ID。

    Returns:
        dict: 音声合成クエリ。
    """
    params = (
        ('text', text),
        ('speaker', speaker),
    )
    try:
        response = requests.post(
            f'http://{HOST}:{PORT}/audio_query',
            params=params
        )
        response.raise_for_status()  # HTTPエラーをチェック
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"エラー: 音声クエリの生成に失敗しました: {e}")
        return None

def synthesize_audio(query):
    """
    音声データを合成する。

    Args:
        query (dict): 音声合成クエリ。

    Returns:
        bytes: 合成された音声データ。
    """
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(
            f'http://{HOST}:{PORT}/synthesis',
            headers=headers,
            params={'speaker': query.get('speaker', 1)},
            data=json.dumps(query)
        )
        response.raise_for_status()  # HTTPエラーをチェック
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"エラー: 音声合成に失敗しました: {e}")
        return None

def play_wav_data(wav_data):
    """
    WAVデータを再生する。

    Args:
        wav_data (bytes): WAVデータ。
    """
    try:
        # バイナリデータをwaveオブジェクトとして読み込む
        with io.BytesIO(wav_data) as audio_io:
            with wave.open(audio_io, 'rb') as wave_read:
                # simpleaudioで再生可能なオーディオオブジェクトを生成
                audio_data = wave_read.readframes(wave_read.getnframes())
                wave_obj = sa.WaveObject(audio_data, wave_read.getnchannels(), wave_read.getsampwidth(), wave_read.getframerate())

        # WAVファイル再生部分
        play_obj = wave_obj.play()
        play_obj.wait_done()  # 再生が完了するまで待つ
    except Exception as e:
        print(f"エラー: WAVデータの再生に失敗しました: {e}")

def generate_and_play_wav(text, speaker=1):
    """
    テキストから音声を生成して再生する。

    Args:
        text (str): 合成するテキスト。
        speaker (int): 話者ID。
    """
    query = generate_audio_query(text, speaker)
    if query:
        wav_data = synthesize_audio(query)
        if wav_data:
            play_wav_data(wav_data)

if __name__ == '__main__':
    text = '明日の天気は晴れと雪だよ'
    generate_and_play_wav(text)
