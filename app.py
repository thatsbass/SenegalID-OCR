from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import cv2
import json
from datetime import datetime
from config import Config
from ocr import CarteIdentiteSenegalaiseOCR
from utils import allowed_file

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/api/extract', methods=['POST'])
def extract_info():
    if 'image' not in request.files:
        return jsonify({'error': 'Aucun fichier trouvé dans la requête', 'status': 400}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Aucun fichier sélectionné', 'status': 400}), 400

    if not allowed_file(file.filename, Config.ALLOWED_EXTENSIONS):
        return jsonify({'error': 'Type de fichier non autorisé. Formats acceptés: ' + ', '.join(Config.ALLOWED_EXTENSIONS), 'status': 400}), 400

    try:
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        img = cv2.imread(filepath)
        carte_senegalaise = CarteIdentiteSenegalaiseOCR(img)

        os.remove(filepath)
        return jsonify(json.loads(carte_senegalaise.to_json()))

    except Exception as e:
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'error': str(e), 'status': 500}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
