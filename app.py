from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/convert', methods=['GET'])
def convert():
    url = request.args.get('url')
    if not url:
        return "Thiếu URL", 400

    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        file_name = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')

    return send_file(file_name, as_attachment=True)

if __name__ == '__main__':
    os.makedirs('downloads', exist_ok=True)
    app.run(host='0.0.0.0', port=5000)
