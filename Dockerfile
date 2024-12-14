# Usar uma imagem oficial do Python
FROM python:3.10-slim

# Configurar o diretório de trabalho no contêiner
WORKDIR /app

# Copiar o arquivo de requisitos para o contêiner
COPY requirements.txt /app/

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt


# Copiar o restante do código para o contêiner
COPY . /app/

# Expor a porta padrão do Django
EXPOSE 8000
