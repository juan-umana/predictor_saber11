FROM python:3.10

# Crear usuario que ejecuta el dash
RUN adduser --disabled-password --gecos '' dash-user

# Definir directorio de trabajo 
WORKDIR /app

# Copiar contenido del directorio actual a la carpeta de trabajo
COPY . /app

# Instala las dependencias del proyecto
RUN pip install -r requirements.txt

# Hacer el directorio de trabajo ejecutable 
RUN chmod +x run.sh

# Cambiar propiedad de la carpeta a dash-user 
RUN chown -R dash-user:dash-user ./

# Cambiar al usuario dash-user
USER dash-user

# Puerto a exponer para el tablero
EXPOSE 80

# Comandos a ejecutar al correr el contenedor 
CMD ["bash", "run.sh"]
