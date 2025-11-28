from flask import Flask, render_template, request, send_file, jsonify
from deep_translator import GoogleTranslator
from werkzeug.utils import secure_filename
import io

app = Flask(__name__)

# Language mapping (same codes as your original)
languages = {
    'Hindi': 'hi',
    'Tamil': 'ta',
    'Telugu': 'te',
    'Malayalam': 'ml',
    'Kannada': 'kn',
    'Gujarati': 'gu',
    'Marathi': 'mr',
    'Punjabi': 'pa',
    'Bengali': 'bn',
    'Odia': 'or',
    'Assamese': 'as',
    'Urdu': 'ur',
    'Sindhi': 'sd',
    'Nepali': 'ne',
    'Sinhala': 'si'
}

@app.route('/')
def index():
    return render_template('lan.html')

@app.route('/translate', methods=['POST'])
def translate():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    language_name = request.form.get('language')
    if not file or file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    if not language_name:
        return jsonify({'error': 'No language selected'}), 400
    if language_name not in languages:
        return jsonify({'error': 'Unsupported language'}), 400

    filename = secure_filename(file.filename)
    input_bytes = file.read()
    try:
        text = input_bytes.decode('utf-8')
    except UnicodeDecodeError:
        # try latin-1 fallback
        text = input_bytes.decode('latin-1')

    target_code = languages[language_name]

    try:
        translator = GoogleTranslator(source='auto', target=target_code)
        translated_text = translator.translate(text)
    except Exception as e:
        return jsonify({'error': f'Translation failed: {e}'}), 500

    out_io = io.BytesIO()
    out_io.write(translated_text.encode('utf-8'))
    out_io.seek(0)

    out_filename = f"translated_{target_code}.txt"
    return send_file(
        out_io,
        as_attachment=True,
        download_name=out_filename,
        mimetype='text/plain'
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)
