import os
from flask import Flask, render_template, request, send_file
import fitz
import pytesseract
from PyPDF2 import PdfReader, PdfWriter
import pdfplumber
from PIL import Image
import re
import zipfile

app = Flask(__name__)

UPLOAD_FOLDER = 'PDF_ARCH'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Caminho para o arquivo ZIP de saída
ZIP_PATH = os.path.join(UPLOAD_FOLDER, "comprovantes.zip")

# Funções de manipulação de CPF
def sanitize_filename(cpf):
    return re.sub(r'[<>:"/\\|?*]', '_', cpf)

def formatar_cpf(cpf):
    return cpf.replace('.', '').replace('-', '').strip()

def cpf_na_pagina(cpf, texto):
    cpf_formatado = formatar_cpf(cpf)
    texto_limpo = re.sub(r'\D', '', texto)
    return cpf_formatado in texto_limpo

def ocr_para_texto(imagem_path):
    imagem_pil = Image.open(imagem_path)
    imagem_pil = imagem_pil.convert('L')
    return pytesseract.image_to_string(imagem_pil)

def busca_e_salva_pdfs(pdf_path, cpfs_file):
    with open(cpfs_file, 'r') as f:
        cpfs = [linha.strip() for linha in f.readlines()]

    cpfs_nao_encontrados = cpfs.copy()
    comprovantes_paths = []

    with pdfplumber.open(pdf_path) as pdf_plumber:
        for i, pagina_plumber in enumerate(pdf_plumber.pages):
            texto = pagina_plumber.extract_text()
            if texto:
                for cpf in cpfs:
                    if cpf_na_pagina(cpf, texto):
                        cpf_formatado = formatar_cpf(cpf)
                        nome_arquivo = f"{sanitize_filename(cpf_formatado)}_pagina_{i+1}.pdf"
                        writer = PdfWriter()
                        pagina_pypdf = PdfReader(pdf_path).pages[i]
                        writer.add_page(pagina_pypdf)
                        output_path = os.path.join(UPLOAD_FOLDER, nome_arquivo)
                        comprovantes_paths.append(output_path)
                        with open(output_path, 'wb') as output_pdf:
                            writer.write(output_pdf)
                        if cpf in cpfs_nao_encontrados:
                            cpfs_nao_encontrados.remove(cpf)

    # Criar um arquivo ZIP com todos os comprovantes encontrados
    with zipfile.ZipFile(ZIP_PATH, 'w') as zipf:
        for file_path in comprovantes_paths:
            zipf.write(file_path, os.path.basename(file_path))

    return ZIP_PATH

def extract_text_from_pdf(pdf_path):
    """Extrai o texto de um arquivo PDF."""
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(document.page_count):
        text += document[page_num].get_text()
    document.close()
    return text

def summarize_text(text):
    """Retorna um resumo simplificado do texto."""
    token_limit = 512  # Ajustado para evitar erros de sequência longa
    tokens = text.split()

    if len(tokens) > token_limit:
        text = ' '.join(tokens[:token_limit])
    elif len(tokens) < 100:
        return text

    # Versão simplificada do resumo
    return text[:500] + "..." if len(text) > 500 else text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Verificação mais clara dos arquivos e ações
    if 'pdf' not in request.files:
        return "Nenhum arquivo PDF foi enviado", 400

    pdf_file = request.files['pdf']
    action = request.form.get('action')

    # Verifica se o arquivo PDF foi selecionado corretamente
    if pdf_file.filename == '':
        return "Nome do arquivo PDF vazio", 400

    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
    pdf_file.save(pdf_path)

    # Se a ação for buscar comprovantes, o arquivo de CPFs é necessário
    if action == "comprovantes":
        if 'cpfs_file' not in request.files:
            return "Nenhum arquivo de CPFs foi enviado", 400
        cpfs_file = request.files['cpfs_file']
        if cpfs_file.filename == '':
            return "Nome do arquivo de CPFs vazio", 400

        cpfs_file_path = os.path.join(app.config['UPLOAD_FOLDER'], cpfs_file.filename)
        cpfs_file.save(cpfs_file_path)

        # Buscar e salvar comprovantes no ZIP
        zip_file_path = busca_e_salva_pdfs(pdf_path, cpfs_file_path)
        return render_template('index.html', zip_file=True, upload_success=True)

    elif action == "resumo":
        # Gerar resumo do PDF
        pdf_text = extract_text_from_pdf(pdf_path)
        summary = summarize_text(pdf_text)
        return render_template('index.html', summary=summary, upload_success=True)

    return "Ação inválida. Por favor, tente novamente.", 400

@app.route('/download_zip')
def download_zip():
    return send_file(ZIP_PATH, as_attachment=True)

if __name__ == "__main__":
    # Ajuste para garantir que a aplicação use a porta fornecida pela variável de ambiente
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)




