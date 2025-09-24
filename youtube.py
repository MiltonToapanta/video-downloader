from flask import Flask, render_template, request, send_file
import yt_dlp
import tempfile
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    mensaje = None
    if request.method == 'POST':
        url = request.form['url'].strip()
        formato = request.form['formato']

        try:
            temp_dir = tempfile.gettempdir()
            output_template = os.path.join(temp_dir, '%(title)s.%(ext)s')

            # Descargar solo streams progresivos (video+audio juntos)
            ydl_opts = {
                'outtmpl': output_template,
                'format': 'best[ext=mp4]/best',  # Solo progresivo MP4
            }

            if formato == '720p':
                ydl_opts['format'] = 'best[height<=720][ext=mp4]/best[ext=mp4]/best'
            elif formato == '360p':
                ydl_opts['format'] = 'best[height<=360][ext=mp4]/best[ext=mp4]/best'

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            return send_file(filename, as_attachment=True)

        except Exception as e:
            mensaje = f"❌ Error: {e}"

    return render_template('index.html', mensaje=mensaje)

if __name__ == '__main__':
    app.run(debug=True)
