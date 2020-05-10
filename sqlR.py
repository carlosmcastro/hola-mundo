import sqlite3 as sq
#creación de indice común, e indice unico.
#uso de index para crear indices.
#uso de unico para volver un indice unico.

conexion = sq.connect("bd.db")

conexion.execute("drop table if exists libros")

conexion.execute("""create table libros (
						codigo integer primary key,
						titulo text,
						autor text,
						editorial text,
						precio real
					)""")

def imprimir(sql_ins):
	cursor = conexion.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)
					
print("\nCreamos un indice común sobre el campo editorial:")
conexion.execute("create index I_libros_editorial on libros(editorial)")

print("\nCreamos un indice único:")
conexion.execute("create unique index I_libros_tituloautor on libros(titulo, autor)")

valores = [('El aleph', 'Borges', 'Emece', None), 
		   ('AntologÃ\xada poÃ©tica', 'Borges', 'Planeta', 39.5), 
		   ('Java en 10 minutos', 'Mario Molina', 'Planeta', 50.5), 
		   ('Alicia en el pais de las maravillas', 'Lewis Carroll', 'Emece', 19.9), 
		   ('Martin Fierro', 'Jose Hernandez', 'Emece', 25.9), 
		   ('Aprenda PHP', 'Mario Molina', 'Emece', 19.5), 
		   ('Cervantes y el quijote', 'Borges', 'Paidos', 18.4)]
conexion.executemany("insert into libros (titulo, autor, editorial, precio) values (?,?,?,?)", valores)
conexion.commit()

print("\nInsertamos algunos valores:")
imprimir("select * from libros")

print("\nEliminamos el indice comun si existe (si no verificamos esto da error).")
conexion.execute("drop index if exists I_libros_editorial")
imprimir("select * from libros")

print("\nIntentamos insertar un elemento repetido (mismo autor, mismo titulo, diferente editorial y precio):")
try:
	conexion.execute("insert into libros (titulo, autor, editorial, precio) values ('Martin Fierro', 'Jose Hernandez', 'Paidos', 16.8);")
except sq.IntegrityError:
	print("\tNo se puede insertar el elemento.")
	
print("\nEliminamos el indice único e intentamos insertar el elemento otra vez (con if exists para evitar un error si no existe):")
conexion.execute("drop index if exists I_libros_tituloautor")
conexion.execute("insert into libros (titulo, autor, editorial, precio) values ('Martin Fierro', 'Jose Hernandez', 'Paidos', 16.8);")
imprimir("select * from libros")

conexion.close()