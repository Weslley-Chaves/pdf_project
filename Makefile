.PHONY: run install clean

# Comando para instalar dependências
install:
	pip install -r requirements.txt

# Comando para executar a aplicação localmente
run:
	FLASK_APP=app.py FLASK_ENV=development flask run

# Comando para iniciar o Gunicorn
start:
	gunicorn app:app --bind 0.0.0.0:10000

# Limpa arquivos e diretórios indesejados
clean:
	rm -rf __pycache__ *.pyc *.pyo
	rm -rf PDF_ARCH/*
