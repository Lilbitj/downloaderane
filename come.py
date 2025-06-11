from flask import Flask, request, render_template, send_from_directory
import os, uuid
import yt_dlp

app = Flask(__name__)
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), 'downloads')
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    filetype = request.form['format']
    unique_id = str(uuid.uuid4())
    template = os.path.join(DOWNLOAD_DIR, f"{unique_id}.%(ext)s")

    ydl_opts = {'outtmpl': template}
    ext = 'mp4'

    if filetype == 'mp3':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
        ext = 'mp3'
    else:
        ydl_opts['format'] = 'best'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        return f"Gagal download: {e}"

    filename = f"{unique_id}.{ext}"
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)