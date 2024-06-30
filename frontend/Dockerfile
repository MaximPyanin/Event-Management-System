# Указание базового образа
FROM nginx:alpine

# Копирование файлов фронтенда в стандартную директорию nginx
COPY ./ /usr/share/nginx/html

# Копирование настроек nginx
#COPY ./nginx.conf /etc/nginx/nginx.conf

# Запуск nginx
CMD ["nginx", "-g", "daemon off;"]
