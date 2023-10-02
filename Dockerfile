# Usa una imagen base de Node.js
FROM node:20.8.0

# Crea un directorio de trabajo en la imagen
WORKDIR /app

# Copia los archivos de tu aplicación al directorio de trabajo
COPY . .

# Instala las dependencias
RUN npm install

# Expone el puerto en el que la aplicación escucha
EXPOSE 80

# Comando para ejecutar la aplicación cuando se inicie el contenedor
CMD ["node", "src/app.js"]
