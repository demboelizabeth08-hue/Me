from flask import Flask, render_template_string, jsonify, send_from_directory
import os

app = Flask(__name__)

# Directory where audio files are stored (current directory)
MEDIA_FOLDER = os.path.dirname(os.path.abspath(__file__))

# Updated mood mapping including YouTube embeds and local audio tracks
MOOD_PLAYLISTS = {
    "chill": [
        {"title": "You and I - LexNour", "type": "local", "file": "LexNour_You_and_I.mp3"},
        {"title": "Lofi Hip Hop - Beats to Relax", "type": "youtube", "embed_id": "jfKfPfyJRdk"}
    ],
    "energetic": [
        {"title": "Trap & Bass Gaming Music", "type": "youtube", "embed_id": "7NOSDKb0HlU"}
    ],
    "focus": [
        {"title": "Deep Focus Synthwave", "type": "youtube", "embed_id": "4xDzrJKXOOY"}
    ],
    "romantic": [
        {"title": "You and I - LexNour", "type": "local", "file": "LexNour_You_and_I.mp3"}
    ]
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mood Sync 🎵</title>
    <style>
        * { box-sizing: border-box; font-family: system-ui, -apple-system, sans-serif; }
        body {
            background-color: #0f0f12;
            color: #f3f3f3;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }
        .container { width: 100%; max-width: 500px; text-align: center; }
        h1 { color: #1ed760; font-size: 2rem; margin-bottom: 5px; }
        p { color: #a7a7a7; font-size: 0.95rem; }
        
        .mood-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin: 25px 0;
        }
        .btn {
            background: #1e1e24;
            color: #fff;
            border: 1px solid #2a2a32;
            padding: 14px;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
        }
        .btn:active { background: #1ed760; color: #000; }
        .player-box {
            background: #18181c;
            border-radius: 16px;
            padding: 15px;
            margin-top: 15px;
            display: none;
        }
        iframe { width: 100%; height: 220px; border: none; border-radius: 12px; }
        audio { width: 100%; margin-top: 10px; }
        .track-title { font-size: 1.1rem; font-weight: 600; margin-bottom: 12px; color: #fff; }
    </style>
</head>
<body>

    <div class="container">
        <h1>Mood Sync</h1>
        <p>Select your mood to generate a stream</p>

        <div class="mood-grid">
            <button class="btn" onclick="fetchMoodTrack('chill')">☕ Chill</button>
            <button class="btn" onclick="fetchMoodTrack('energetic')">⚡ Energetic</button>
            <button class="btn" onclick="fetchMoodTrack('focus')">🧠 Focus</button>
            <button class="btn" onclick="fetchMoodTrack('romantic')">❤️ Romantic</button>
        </div>

        <div class="player-box" id="playerBox">
            <div class="track-title" id="trackTitle">Playing...</div>
            <div id="mediaContainer"></div>
        </div>
    </div>

    <script>
        function fetchMoodTrack(mood) {
            fetch('/api/playlist/' + mood)
                .then(res => res.json())
                .then(data => {
                    if (data.length > 0) {
                        const track = data[Math.floor(Math.random() * data.length)];
                        document.getElementById('trackTitle').innerText = track.title;
                        
                        const container = document.getElementById('mediaContainer');
                        if (track.type === 'youtube') {
                            container.innerHTML = `<iframe src="https://www.youtube.com/embed/${track.embed_id}?autoplay=1" allow="autoplay"></iframe>`;
                        } else if (track.type === 'local') {
                            container.innerHTML = `<audio controls autoplay><source src="/audio/${track.file}" type="audio/mpeg">Your browser does not support audio playback.</audio>`;
                        }
                        
                        document.getElementById('playerBox').style.display = 'block';
                    }
                });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/playlist/<mood>')
def get_playlist(mood):
    playlist = MOOD_PLAYLISTS.get(mood.lower(), [])
    return jsonify(playlist)

# Route to safely serve local audio files from your device folder
@app.route('/audio/<path:filename>')
def serve_audio(filename):
    return send_from_directory(MEDIA_FOLDER, filename)

if __name__ == '__main__':
    # debug=False prevents reloading crashes on Pydroid 3
    app.run(host='0.0.0.0', port=5000, debug=False)