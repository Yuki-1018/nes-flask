from flask import Flask, request, jsonify
from pytube import YouTube
from linebot import LineBotApi
from linebot.models import TextSendMessage

app = Flask(__name__)
line_bot_api = LineBotApi('2WGisi8Zt2+KwcsZwRRjh/X+uO/VKMmKl5jrm9PhFaBTi7RzgdeMRRoxEFUZP1XlAPFfGvMDcsEdW6p6PAiXuw/1foqApC8Jan3xndgAU7wP3Y3Eyu8EHf33KmvP7Dxf3H1V5ZmSx9sHWiSzvExtqQdB04t89/1O/w1cDnyilFU=')  # Lineのチャンネルアクセストークンを入力

@app.route('/yt', methods=['POST'])
def get_youtube_links():
    data = request.json
    youtube_link = data.get('youtube_link')
    if not youtube_link:
        return jsonify({'error': 'No YouTube link provided'}), 400
    
    try:
        mp4_link, mp3_link = get_download_links(youtube_link)
        user_id = data.get('user_id')  # ユーザーIDの取得（Lineの場合）
        send_links_to_user(user_id, mp4_link, mp3_link)
        return jsonify({'mp4_link': mp4_link, 'mp3_link': mp3_link}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_download_links(youtube_link):
    yt = YouTube(youtube_link)
    mp4_link = yt.streams.filter(file_extension='mp4').first().url
    mp3_link = yt.streams.filter(only_audio=True).first().url
    return mp4_link, mp3_link

def send_links_to_user(user_id, mp4_link, mp3_link):
    message = f"MP4 Link: {mp4_link}\nMP3 Link: {mp3_link}"
    line_bot_api.push_message(user_id, TextSendMessage(text=message))

if __name__ == "__main__":
    app.run(debug=True)
