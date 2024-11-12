
FROM python:3.11-slim

# Instalar dependências do sistema necessárias para compilar certas bibliotecas
RUN apt-get update && apt-get install -y \
    build-essential \
    cargo \
    gcc \
    libglib2.0-0 \
    git && \
    apt-get clean

# Definir o diretório de trabalho
WORKDIR /app

# Copiar todos os arquivos do projeto para o contêiner
COPY . /app

# Instalar as dependências do Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Definir o comando padrão para iniciar a aplicação
CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:8080"]
