from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

def get_video_info(url):
    ydl_opts = {'format': 'best', 'quiet': True, 'no_warnings': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return {
                'status': 'success',
                'title': info.get('title', 'Media File'),
                'download_url': info.get('url'),
                'thumbnail': info.get('thumbnail'),
                'duration': info.get('duration')
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/extract', methods=['POST'])
def extract():
    data = request.get_json()
    video_url = data.get('url')
    if not video_url:
        return jsonify({'status': 'error', 'message': 'URL is required'}), 400
    return jsonify(get_video_info(video_url))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
