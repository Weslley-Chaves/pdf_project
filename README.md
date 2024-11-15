# PDF Reader

Este projeto é uma aplicação para leitura, extração de texto e manipulação de arquivos PDF com funcionalidades específicas para busca de CPFs e geração de resumos.

## Funcionalidades

- **Extração de Texto**: Extrai texto de arquivos PDF usando a biblioteca `pdfplumber` e `PyMuPDF`.
- **Busca e Geração de Comprovantes**: Busca CPFs específicos em um PDF e gera arquivos PDF individuais para cada CPF encontrado.
- **Reconhecimento Óptico de Caracteres (OCR)**: Utiliza `pytesseract` para extrair texto de imagens dentro de arquivos PDF.
- **Resumo de Texto**: Gera um resumo do conteúdo textual extraído usando um modelo de NLP (Natural Language Processing) com `transformers`.
- **Geração de Arquivo ZIP**: Cria um arquivo ZIP com todos os comprovantes PDF gerados a partir da busca de CPFs.

## Tecnologias Utilizadas

- **Python Flask**: Framework para criação da aplicação web.
- **Bibliotecas PDF**: `pdfplumber`, `PyPDF2` e `fitz` para manipulação e extração de conteúdo em PDF.
- **Reconhecimento Óptico de Caracteres**: `pytesseract` e `PIL` para reconhecimento de texto em imagens.
- **NLP com Transformers**: Biblioteca `transformers` da Hugging Face para resumir textos extraídos.

## Pré-requisitos

1. Instale o Tesseract OCR no sistema para uso do `pytesseract`.
2. Instale as dependências do Python.

## Como Executar o Projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/AlunosAdsAnhanguera/PDF_reader.git
   ```
2. Navegue até o diretório do projeto:
   ```bash
   cd PDF_reader
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute a aplicação:
   ```bash
   python app.py
   ```
   A aplicação estará disponível em `http://127.0.0.1:5000`.

## Estrutura do Projeto

- **app.py**: Script principal que contém a lógica da aplicação.
- **PDF_ARCH/**: Diretório onde os PDFs carregados e processados são armazenados.
- **templates/** e **static/**: Arquivos de interface e estilos da aplicação.

## Uso da Aplicação

### Upload de Arquivos

- **PDF**: Envie um arquivo PDF para leitura.
- **Arquivo de CPFs (.txt)**: Envie um arquivo de texto contendo os CPFs a serem buscados no PDF.

### Ações Disponíveis

- **Gerar Resumo**: Extrai o texto do PDF e gera um resumo usando um modelo de NLP.
- **Buscar Comprovantes de CPF**: Busca os CPFs no PDF e gera arquivos PDF individuais para cada CPF encontrado, compactando todos os arquivos gerados em um ZIP para download.

## Endpoints

- **Rota Principal (`/`)**: Página inicial com o formulário de upload.
- **Upload (`/upload`)**: Processa o upload do PDF e do arquivo de CPFs, executando a ação selecionada.
- **Download do ZIP (`/download_zip`)**: Permite o download do arquivo ZIP gerado.

## Exemplo de Estrutura do Arquivo de CPFs

O arquivo `cpfs.txt` deve ter o seguinte formato, com um CPF por linha:

```plaintext
123.456.789-00
987.654.321-00
```

## Contribuição

Contribuições são bem-vindas. Sinta-se à vontade para fazer um fork do repositório, criar uma nova branch com suas alterações e abrir um pull request.

## Arquivo de Dependências - `requirements.txt`

Para executar o projeto, é necessário instalar as seguintes bibliotecas:

```plaintext
Flask==2.0.1
PyMuPDF==1.19.0
pytesseract==0.3.8
pdfplumber==0.5.28
Pillow==8.3.1
transformers==4.9.1
torch==1.9.0
PyPDF2==2.1.0
```

### Instruções para Instalação

1. **Instale as Dependências**: Execute o comando abaixo no diretório do projeto para instalar todas as bibliotecas listadas:
   ```bash
   pip install -r requirements.txt
   ```

2. **Instalação do Tesseract OCR**:
   - **Linux (Debian/Ubuntu)**:
     ```bash
     sudo apt-get install tesseract-ocr
     ```
   - **Windows**:
     - Baixe o instalador do Tesseract OCR no [repositório oficial do GitHub](https://github.com/tesseract-ocr/tesseract).
     - Adicione o caminho do executável do Tesseract ao PATH do sistema para que `pytesseract` possa acessá-lo.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
```

Esse conteúdo formata o `README.md` com seções detalhadas e organizadas, incluindo o arquivo `requirements.txt` e as instruções de instalação.


