from flask import Flask, render_template, request, jsonify
from url_analyzer import URLAnalyzer

app = Flask(__name__)
analyzer = URLAnalyzer()


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/check', methods=['POST'])
def check_url():
    """Analyze a URL and return results"""
    data = request.get_json()
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({
            'error': 'No URL provided'
        }), 400
    
    # Add scheme if missing
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    
    # Analyze the URL
    result = analyzer.analyze(url)
    
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
