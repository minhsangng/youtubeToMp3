from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_audio(url):
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'cookiefile': 'cookies.txt',
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")
    return filename

@app.route('/')
def home():
    return "Flask app is running!"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            try:
                filename = download_audio(url)
                return send_file(filename, as_attachment=True)
            except Exception as e:
                return f"Lỗi: {str(e)}"
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>YouTube to MP3 Converter</title>
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: #fff;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
            }
            .container {
                background: rgba(255, 255, 255, 0.1);
                padding: 30px;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
            }
            h2 {
                margin-bottom: 20px;
            }
            input {
                padding: 10px;
                width: 80%;
                border: none;
                border-radius: 8px;
                margin-bottom: 15px;
                font-size: 16px;
                color: #333;
            }
            button {
                padding: 12px 25px;
                border: none;
                border-radius: 8px;
                background: #ff6b6b;
                color: #fff;
                font-size: 16px;
                cursor: pointer;
                transition: background 0.3s;
            }
            button:hover {
                background: #ff4f4f;
            }
            #status {
                margin-top: 20px;
                font-size: 18px;
                color: #f1f1f1;
            }
        </style>
        <script>
            async function convertAudio(event) {
                event.preventDefault();
                const url = document.getElementById('url').value;
                const status = document.getElementById('status');
                if (!url) {
                    status.textContent = 'Vui lòng nhập URL.';
                    return;
                }
                status.textContent = '🔄 Đang tải...';

                try {
                    const response = await fetch('/', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                        body: `url=${encodeURIComponent(url)}`
                    });

                    if (response.ok) {
                        const blob = await response.blob();
                        const downloadUrl = window.URL.createObjectURL(blob);
                        const link = document.createElement('a');
                        link.href = downloadUrl;
                        link.download = 'youtube_audio.mp3';
                        document.body.appendChild(link);
                        link.click();
                        link.remove();
                        status.textContent = '✅ Đã tải xong!';
                    } else {
                        status.textContent = '❌ Chuyển đổi thất bại.';
                    }
                } catch (error) {
                    status.textContent = `❌ Lỗi: ${error.message}`;
                }
            }
        </script>
    </head>
    <body>
        <div class="container">
            <h2>🎵 YouTube to MP3 Converter</h2>
            <form onsubmit="convertAudio(event)">
                <input type="text" id="url" name="url" placeholder="Dán link YouTube vào đây" required>
                <br>
                <button type="submit">🔄 Chuyển đổi</button>
            </form>
            <div id="status"></div>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
