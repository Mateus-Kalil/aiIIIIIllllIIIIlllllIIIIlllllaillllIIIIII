# Usa uma imagem bem leve do NGINX
FROM nginx:alpine

# Copia todos os arquivos da pasta local para a pasta padrão do NGINX
COPY . /usr/share/nginx/html

# Expõe a porta 80 (padrão do NGINX)
EXPOSE 80
