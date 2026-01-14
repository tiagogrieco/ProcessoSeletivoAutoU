import os
from flask import Flask, request, jsonify, send_from_directory
from .nlp_engine import NLPEngine
import pypdf

app = Flask(__name__, static_folder="../frontend", static_url_path="")
nlp = NLPEngine()

@app.route('/')
def home():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)

@app.route('/api/classify', methods=['POST'])
def classify():
    data = None
    text_content = ""

    # Handle File Upload
    if 'file' in request.files:
        file = request.files['file']
        if file.filename.endswith('.pdf'):
            try:
                # Read PDF
                pdf_reader = pypdf.PdfReader(file)
                for page in pdf_reader.pages:
                    try:
                        text = page.extract_text()
                        if text:
                            text_content += text + "\n"
                    except Exception as extraction_error:
                        print(f"Warning: Could not extract text from a page: {extraction_error}")
                        continue
            except Exception as e:
                return jsonify({"error": f"Failed to read PDF file: {str(e)}"}), 400
        elif file.filename.endswith('.txt'):
            text_content = file.read().decode('utf-8')
        else:
            return jsonify({"error": "Unsupported file format"}), 400
    
    # Handle Text Input
    elif 'text' in request.form:
        text_content = request.form['text']
    
    elif request.json and 'text' in request.json:
        text_content = request.json['text']

    if not text_content.strip():
        if 'file' in request.files and request.files['file'].filename.endswith('.pdf'):
            return jsonify({"error": "Não foi possível extrair texto do PDF. O arquivo pode ser uma imagem escaneada. Tente copiar e colar o texto na aba 'Texto Direto'."}), 400
        return jsonify({"error": "Nenhum conteúdo de texto encontrado para análise."}), 400

    # Process
    result = nlp.classify_and_respond(text_content)
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
