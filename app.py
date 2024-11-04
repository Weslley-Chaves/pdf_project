from flask import Flask, render_template, request, redirect, url_for 
import os
import fitz  
from transformers import pipeline

app = Flask(__name__)


UPLOAD_FOLDER = 'PDF_ARCH'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


summarizer = pipeline("summarization")

def extract_text_from_pdf(pdf_path):
    """Extrai o texto de um arquivo PDF."""
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(document.page_count):
        text += document[page_num].get_text()
    document.close()
    return text

def summarize_text(text):
    """Gera um resumo do texto usando um modelo de NLP."""
    
    # Verifica o comprimento em tokens
    token_limit = 1024
    tokens = text.split()  # Divide o texto em palavras (tokens)

    if len(tokens) > token_limit:
        # Trunca o texto se exceder o limite
        text = ' '.join(tokens[:token_limit])

    elif len(tokens) < 100:
        return text  # Retorna o texto se for muito curto

    print("Comprimento do texto:", len(tokens))
    print("Texto para resumo:", text[:500])  # Mostre os primeiros 500 caracteres

    try:
        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
        
        if summary:
            return summary[0]['summary_text']
        else:
            return "Resumo não pôde ser gerado."
    except Exception as e:
        return f"Erro ao gerar resumo: {str(e)}"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf' not in request.files:
        return "Nenhum arquivo foi enviado", 400
    
    file = request.files['pdf']
    if file.filename == '':
        return "Nome do arquivo vazio", 400
    
    if file and file.filename.endswith('.pdf'):
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(pdf_path)

        # Extrai texto e gera resumo
        pdf_text = extract_text_from_pdf(pdf_path)
        summary = summarize_text(pdf_text)

        # Renderiza a página com o resumo
        return render_template('index.html', summary=summary)

    return "Arquivo inválido. Por favor, envie um PDF.", 400

if __name__ == "__main__":
    app.run(debug=True)
