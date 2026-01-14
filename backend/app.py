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
                # Try pypdf first (faster)
                import io
                file_bytes = file.read()
                file_stream = io.BytesIO(file_bytes)
                
                pdf_reader = pypdf.PdfReader(file_stream)
                pages_extracted = 0
                pages_failed = 0
                
                for i, page in enumerate(pdf_reader.pages):
                    try:
                        text = page.extract_text()
                        if text and text.strip():
                            text_content += text + "\n"
                            pages_extracted += 1
                    except Exception as extraction_error:
                        pages_failed += 1
                        print(f"Warning: PyPDF failed on page {i+1}: {extraction_error}")
                        continue
                
                # If PyPDF failed completely, try pdfplumber as fallback
                if pages_extracted == 0 and pages_failed > 0:
                    try:
                        import pdfplumber
                        file_stream.seek(0)  # Reset stream
                        with pdfplumber.open(file_stream) as pdf:
                            print(f"Trying pdfplumber fallback ({len(pdf.pages)} pages)...")
                            for i, page in enumerate(pdf.pages):
                                try:
                                    text = page.extract_text()
                                    if text and text.strip():
                                        text_content += text + "\n"
                                        pages_extracted += 1
                                except Exception as e:
                                    print(f"pdfplumber also failed on page {i+1}: {e}")
                                    continue
                    except ImportError:
                        print("pdfplumber not available for fallback")
                
                # Log extraction statistics
                print(f"PDF extraction: {pages_extracted} pages OK, {pages_failed} pages failed")
                
            except Exception as e:
                return jsonify({"error": f"Erro ao abrir PDF: {str(e)}"}), 400
        elif file.filename.endswith('.txt'):
            text_content = file.read().decode('utf-8')
        elif file.filename.endswith('.msg'):
            try:
                import extract_msg
                import io
                file_bytes = file.read()
                file_stream = io.BytesIO(file_bytes)
                
                msg = extract_msg.Message(file_stream)
                
                # Extract with null checks
                subject = msg.subject or "(Sem assunto)"
                sender = msg.sender or "(Remetente desconhecido)"
                
                # Try different body properties
                body = msg.body or msg.htmlBody or msg.rtfBody or ""
                
                # Build text content
                text_content += f"Assunto: {subject}\n\n"
                text_content += f"De: {sender}\n\n"
                if body:
                    text_content += f"{body}\n"
                else:
                    text_content += "(Email sem corpo de texto)\n"
                    
                print(f"MSG extraction successful: {len(text_content)} chars")
            except Exception as e:
                print(f"MSG extraction error: {e}")
                return jsonify({"error": f"Erro ao ler arquivo MSG: {str(e)}"}), 400
        else:
            return jsonify({"error": "Formato não suportado. Use .txt, .pdf ou .msg"}), 400
    
    # Handle Text Input
    elif 'text' in request.form:
        text_content = request.form['text']
    
    elif request.json and 'text' in request.json:
        text_content = request.json['text']

    if not text_content.strip():
        if 'file' in request.files and request.files['file'].filename.endswith('.pdf'):
            return jsonify({
                "error": "Não foi possível extrair texto do PDF.",
                "suggestion": "Este PDF pode ser:\n• Imagem escaneada (sem texto)\n• Protegido/criptografado\n• Com formatação problemática\n\n💡 Solução: Abra o PDF, copie o texto e use a aba 'Texto Direto'."
            }), 400
        return jsonify({"error": "Nenhum conteúdo encontrado para análise."}), 400

    # Process
    result = nlp.classify_and_respond(text_content)
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
