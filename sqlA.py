import sqlite3 as sq
#Crear una tabla y borrarla en una base se datos.

conexion = sq.connect("bd.db")

try:
	#creamos la tabla usuarios, con dos datos tipo texto.
	conexion.execute("""
			create table usuarios (
			nombre text,
			clave text
			);
	""")
	print("Se ha creado una table.")
except sq.OperationalError:
	print("La tabla ya existe.")
	

#Insertamos un registro.
conexion.execute("insert into usuarios (nombre, clave) values ('Anabel', 'Muñeca');")
conexion.execute("insert into usuarios (nombre, clave) values ('Toallin', 'Toalla');")
conexion.execute("insert into usuarios (nombre, clave) values ('Pikachu', 'Pokemon');")
conexion.commit()
	
#Visualizamos un registro.
#esto solo es necesario en python, en un visualizador se omite el commit y los detalles.
cursor = conexion.execute("select nombre, clave from usuarios;")
for fila in cursor.fetchall():
	print(fila)
	
	
print("eliminamos la tabla creada")
conexion.execute("drop table usuarios;")
conexion.commit()
conexion.close()