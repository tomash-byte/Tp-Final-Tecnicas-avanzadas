import mysql.connector 
from mysql.connector import Error



                 # Configuración de la conexión a MySQL (ajusta host, user, password si es necesario)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Cambia si tienes contraseña
    'database': 'centro_deportivo'
}

                # Función para conectar a la base de datos
def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

                # Inicializar la base de datos (ejecutar el SQL si no está hecho)
def init_db():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            with open('../dbf/database.sql', 'r') as f:
                sql_script = f.read()
                                    # Ejecutar el script (dividido por ; para múltiples statements)
                for statement in sql_script.split(';'):
                    if statement.strip():
                        cursor.execute(statement)
            conn.commit()
            print("Base de datos iniciada.")
        except Exception as e:
            print(f"Error inicializando DB: {e}")
        finally:
            cursor.close()
            conn.close()

                   # CREATE: Agregar un nuevo miembro
def create_member():
    name = input("Nombre: ")
    email = input("Email: ")
    join_date = input("Fecha de nacimiento (YYYY-MM-DD): ")
    nationality_type = input("Nacionalidad: ")

    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO members (name, email, nationality_type, join_date) VALUES (%s, %s, %s, %s)',
                           (name, email, nationality_type, join_date))
            conn.commit()
            print("Socio agregado exitosamente.")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

                       # READ: Listar todos los miembros
def read_members():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM members')
        members = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if members:
            print("\nLista de socios:")
            for member in members:
                print(f"ID: {member[0]}, Nombre: {member[1]}, Email: {member[2]}, Nacionalidad: {member[3]}, Fecha: {member[4]}")
        else:
            print("No existen socios registrados.")

                  # READ: Buscar un miembro por ID
def read_member_by_id():
    member_id = int(input("ID del socio: "))
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM members WHERE id = %s', (member_id,))
        member = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if member:
            print(f"ID: {member[0]}, Nombre: {member[1]}, Email: {member[2]}, Nacionalidad: {member[3]}, Fecha: {member[4]}")
        else:
            print("No se pudo encontrar el socio.")

                 # UPDATE: Modificar un miembro
def update_member():
    member_id = int(input("ID del socio a actualizar: "))
    name = input("Nuevo nombre (deja vacío para no cambiar): ")
    email = input("Nuevo email (deja vacío para no cambiar): ")
    membership_type = input("Nuevo tipo de membresía (deja vacío para no cambiar): ")
    join_date = input("Nueva fecha de ingreso (YYYY-MM-DD, deja vacío para no cambiar): ")
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM members WHERE id = %s', (member_id,))
        if not cursor.fetchone():
            print("Socio no encontrado.")
            cursor.close()
            conn.close()
            return
        
        updates = []
        params = []
        if name:
            updates.append("name = %s")
            params.append(name)
        if email:
            updates.append("email = %s")
            params.append(email)
        if membership_type:
            updates.append("membership_type = %s")
            params.append(membership_type)
        if join_date:
            updates.append("join_date = %s")
            params.append(join_date)
        
        if updates:
            query = f"UPDATE members SET {', '.join(updates)} WHERE id = %s"
            params.append(member_id)
            try:
                cursor.execute(query, params)
                conn.commit()
                print("Socio actualizado exitosamente.")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("No se realizaron cambios.")
        cursor.close()
        conn.close()

                 # DELETE: Eliminar un miembro
def delete_member():
    member_id = int(input("ID del socio a eliminar: "))
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM members WHERE id = %s', (member_id,))
        if not cursor.fetchone():
            print("Socio no encontrado.")
            cursor.close()
            conn.close()
            return
        
        confirm = input("¿Estás seguro de eliminar este socio? (s/n): ").lower()
        if confirm == 's':
            cursor.execute('DELETE FROM members WHERE id = %s', (member_id,))
            conn.commit()
            print("El socio ha sido eliminado exitosamente.")
        else:
            print("Eliminación de carnet cancelada.")
        cursor.close()
        conn.close()

                # Menú principal
def main():
    init_db()
    while True:
        print("\n--- CRUD Centro Deportivo ---")
        print("1. Agregar socio (Create)")
        print("2. Listar socios (Read)")
        print("3. Buscar socios por ID (Read)")
        print("4. Actualizar socio (Update)")
        print("5. Eliminar socio (Delete)")
        print("6. Salir")
        choice = input("Elige una opción: ")
        
        if choice == '1':
            create_member()
        elif choice == '2':
            read_members()
        elif choice == '3':
            read_member_by_id()
        elif choice == '4':
            update_member()
        elif choice == '5':
            delete_member()
        elif choice == '6':
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida.")

if __name__ == '__main__':
    main()

