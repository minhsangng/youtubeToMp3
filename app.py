import os
import imageio_ffmpeg as ffmpeg
from flask import Flask, request, send_file
import yt_dlp

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return '''
    <h2>🎵 YouTube to MP3 Converter</h2>
    <form method="get" action="/convert">
        <input type="text" name="url" placeholder="Nhập link YouTube" required>
        <button type="submit">Chuyển đổi</button>
    </form>
    '''

@app.route('/convert', methods=['GET'])
def convert():
    url = request.args.get('url')
    if not url:
        return "Thiếu URL!", 400

    try:
        options = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': f'downloads/%(title)s.%(ext)s',
            'ffmpeg_location': ffmpeg.get_ffmpeg_exe(),  # Chỉ định ffmpeg
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return f"Lỗi: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
