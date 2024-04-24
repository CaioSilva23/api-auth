FROM python:3.8

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app/

# Definindo permissõe do script
RUN chmod +x /app/scripts/entrypoint.sh

EXPOSE 8000

# Comando para executar o servidor Django
CMD ["/app/scripts/entrypoint.sh"]