from flask import Flask, render_template, request, jsonify
import yt_dlp
from datetime import datetime
import random

app = Flask(__name__)

# محاكاة ذكاء اصطناعي لتلخيص محتوى الفيديو مجاناً وبسرعة فائقة
def ai_summarize_video(title):
    summaries = [
        f"This media focuses on the core concepts of '{title}'. It provides a high-level overview, practical examples, and clear insights suitable for research and global archiving.",
        f"An analytical breakdown of '{title}'. The content explores structural methodologies, key trend definitions, and offers a comprehensive summary tailored for quick digital consumption.",
        f"Quick Summary: '{title}' delivers essential learning tokens, strategic advice, and an optimized conclusion designed to save time while maximizing value."
    ]
    return random.choice(summaries)

def get_video_info(url):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            media_data = {
                'status': 'success',
                'title': info.get('title', 'Media File'),
                'download_url': info.get('url'),
                'thumbnail': info.get('thumbnail'),
                'duration': info.get('duration')
            }
            
            # حفظ الردود تلقائياً في ملف التوثيق
            with open('downloads_log.txt', 'a', encoding='utf-8') as log_file:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                log_file.write(f"[{timestamp}] TITLE: {media_data['title']} | TARGET_URL: {url}\n")
                
            return media_data
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
    
    result = get_video_info(video_url)
    return jsonify(result)

# رابط برمي ذكي خاص بالذكاء الاصطناعي للتلخيص
@app.route('/api/ai-summarize', methods=['POST'])
def ai_summarize():
    data = request.get_json()
    title = data.get('title', 'Media File')
    summary = ai_summarize_video(title)
    return jsonify({'status': 'success', 'summary': summary})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
