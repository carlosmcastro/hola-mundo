import sqlite3 as sq
#actualizar datos con sql.


# /* comentario sql
# de varias
# lineas*/

# --comentario sql de una linea.
conexion = sq.connect("bd.db")

#el punto y coma es opcional en python, pero en otros lugares puede no serlo.
print("Borramos la tabla si existe.")
conexion.execute("drop table if exists usuarios;")

def imprimir(sql_ins):
	cursor = conexion.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)

try:
	print("Creamos la tabla.")
	conexion.execute("""create table usuarios (
					    nombre text,
						clave text
					);""")
except sq.OperationalError:
	print("Ya existe la tabla.")

valores = [("Pablo", "Perejil"),
		   ("José", "Zanahoria"),
		   ("María", "Tomate"),
		   ("Juana", "Pepino")]
conexion.executemany("insert into usuarios (nombre, clave) values (?,?);", valores)
conexion.commit()

todos = "select * from usuarios;"

print("\nPartimos cos estos elementos para la tabla:")
imprimir(todos)

print("\nActualizamos: Cambiamos todas las claves por Brocoli.")
conexion.execute("update usuarios set clave = 'Brocoli'")
conexion.commit()
imprimir(todos)

print("\nActualizamos: Le asignamos Manzana a Juana.")
conexion.execute("""update usuarios set clave = 'Manzana' 
					where nombre = 'Juana'""")
conexion.commit()
imprimir(todos)

print("\nSi no encuentra el registro no modifica valor alguno de la base de datos.")
conexion.execute("update usuarios set clave = 'Peras' where nombre = 'EsferaCeleste'")
conexion.commit()
imprimir(todos)

print("\nSe pueden actualizar varios campos.")
print("\nActualizamos: José por JoséAldo y Brocoli por Piña.")
conexion.execute("""update usuarios set clave = 'Piña', nombre = 'JoséAldo'
					where nombre = 'José';""")
conexion.commit()
imprimir(todos)

conexion.close()