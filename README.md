# Tp-Final-Tecnicas-avanzadas
Proyecto final para la promoción de la materia


  CRUD ---- Centro Deportivo de Futbol

Aplicación de consola sobre Python, para gestionar socios de un centro deportivo utilizando MySQL como base de datos.

------------------------------------------------------------
  REQUISITOS MÍNIMOS

- Python 3.8 o superior
- MySQL Server 8.0 o superior
- pip (gestor de paquetes de Python)
- Visual Studio Code (VS Code) o cualquier editor de texto.

------------------------------------------------------------
  INSTALACIÓN DE DEPENDENCIAS

1. Cloná el repositorio o descargá los archivos del proyecto.
2. Abrí una terminal y ejecutá:

   pip install mysql-connector-python

------------------------------------------------------------
 CONFIGURACIÓN DE MYSQL

1. Abrí CMD y conectate como root:

   cd "C:\Program Files\MySQL\MySQL Server 8.0\bin"
   mysql -u root -p

2. Dentro del cliente MySQL, ejecutá:

   CREATE DATABASE centro_deportivo;

   DROP USER IF EXISTS 'appuser'@'localhost';
   CREATE USER 'appuser'@'localhost' IDENTIFIED BY 'app_pass';
   GRANT ALL PRIVILEGES ON centro_deportivo.* TO 'appuser'@'localhost';
   FLUSH PRIVILEGES;

3. Seleccioná la base de datos y verificá que esté vacía o tenga la tabla members:

   USE centro_deportivo;
   SHOW TABLES;

------------------------------------------------------------
  CREAR LA TABLA MEMBERS

Si no existe la tabla, tenes que crearla manualmente o usar el archivo database.sql.

Opción a: Crearla manualmente

   CREATE TABLE IF NOT EXISTS members (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(100) NOT NULL,
       email VARCHAR(100) NOT NULL UNIQUE,
       nationality_type VARCHAR(50),
       membership_type VARCHAR(50),
       join_date DATE NOT NULL
   );

Opción b: Usar el script

   ·source ruta/a/dbf/database.sql

------------------------------------------------------------
  VERIFICAR CONEXIÓN DESDE PYTHON

1. Abrí VS Code.
2. Abrí el archivo main.py.
3. Asegurate de que la configuración de conexión sea:

   DB_CONFIG = {
       'host': 'localhost',
       'user': 'appuser',
       'password': 'app_pass',
       'database': 'centro_deportivo'
   }

------------------------------------------------------------
 EJECUTAR EL CRUD

1. Desde la terminal de VS Code o CMD, navegá a la carpeta del proyecto:

   ·cd ruta/a/crud_centro_deportivo

2. Ejecutá el script:

   ·python main.py

3. Verás el menú interactivo:

   --- CRUD Centro Deportivo ---
   1. Agregar socio (Create)
   2. Listar socios (Read)
   3. Buscar socios por ID (Read)
   4. Actualizar socio (Update)
   5. Eliminar socio (Delete)
   6. Salir

------------------------------------------------------------
  PRUEBA RÁPIDA

1. Elegí la opción 1 y agregá un socio.
2. Luego elegí la opción 2 para ver la lista de socios.
3. Tambien, podes probar las demás funciones para editar, buscar o eliminar.

------------------------------------------------------------

Desarrollado por Tomás gatica

·tomashgatica03@gmail.com
