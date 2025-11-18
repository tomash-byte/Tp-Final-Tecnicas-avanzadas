import mysql.connector
from mysql.connector import Error
import re
from datetime import datetime


###Configuración de conexión
DB_CONFIG = {
    'host': 'localhost',
    'user': 'appuser',
    'password': 'app_pass',
    'database': 'centro_deportivo'
}

#Conexión a la base de datos
def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

###inicializar base de datos
def init_db():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            with open('../dbf/database.sql', 'r') as f:
                sql_script = f.read()
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

##Validaciones
def validar_email(email):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, email)

def validar_fecha(fecha):
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def continuar():
    opcion = input("\n¿Deseás realizar otra operación? (s/n): ").strip().lower()
    return opcion == 's'

#CREATE
def create_member():
    name = input("Nombre: ")

    while True:
        email = input("Email: ")
        if validar_email(email):
            break
        else:
            print(" Mail inválido.")

    while True:
        join_date = input("Fecha de nacimiento (YYYY-MM-DD): ")
        if validar_fecha(join_date):
            break
        else:
            print(" Fecha inválida. Usá el formato YYYY-MM-DD.")

    nationality_type = input("Nacionalidad: ")

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO members (name, email, nationality_type, join_date) VALUES (%s, %s, %s, %s)',
                           (name, email, nationality_type, join_date))
            conn.commit()
            print(" Socio agregado exitosamente.")
        except Exception as e:
            print(f" Error: {e}")
        finally:
            cursor.close()
            conn.close()


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

# ID
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

#UPDATE
def update_member():
    member_id = int(input("ID del socio a actualizar: "))
    name = input("Nuevo nombre : ")

    while True:
        email = input("Nuevo email : ")
        if not email or validar_email(email):
            break
        else:
            print(" Email inválido. Intentá nuevamente.")

    membership_type = input("Nuevo tipo de cuota (deja vacío para no cambiar): ")

    while True:
        join_date = input("Nueva fecha de nacimiento (YYYY-MM-DD): ")
        if not join_date or validar_fecha(join_date):
            break
        else:
            print(" Fecha de nacimiento inválida. Usá el formato YYYY-MM-DD.")

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
                print(" Socio actualizado exitosamente.")
            except Exception as e:
                print(f" Error: {e}")
        else:
            print("No se realizaron cambios.")
        cursor.close()
        conn.close()

#DELETE
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
            print(" El socio ha sido eliminado exitosamente.")
        else:
            print("Eliminación de socio cancelada.")
        cursor.close()
        conn.close()

#MAIN MENU
def main():
    init_db()
    while True:
        print("\n---Centro Deportivo TFC ---")
        print("1. Agregar socio ")  #create
        print("2. Lista de socios ") #read
        print("3. Buscar socios por Id. ") #read id
        print("4. Actualizar socio existente ") #update
        print("5. Eliminar socio ") #delete
        print("6. Salir") #exit
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
            print(" Hasta luego!")
            break
        else:
            print(" Opción inválida.")

        if choice != '6' and not continuar():
            print(" Gracias por usar el sistema de TFC ")
            break

if __name__ == '__main__':
    main()
