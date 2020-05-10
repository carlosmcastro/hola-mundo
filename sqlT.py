import sqlite3 as sq

conexion = sq.connect("bd.db")

conexion.execute("drop table if exists libros")
conexion.execute("drop table if exists editoriales")

conexion.execute("""create table libros (
						codigo integer primary key,
						titulo text,
						autor text,
						codigoeditorial integer,
						precio real
					)""")
					
conexion.execute("""create table editoriales (
						codigo integer primary key,
						nombre text
					)""")

def imprimir(sql_ins):
	cursor = conexion.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)

valores = [('Planeta',),
		   ('Emece',),
		   ('Siglo XXI',)]
conexion.executemany("insert into editoriales(nombre) values (?)", valores)

valores = [('El aleph', 'Borges', 2, 34), 
			('AntologÃ\xada poÃ©tica', 'Borges', 1, 39.5), 
			('Java en 10 minutos', 'Mario Molina', 1, 50.5), 
			('Alicia en el pais de las maravillas', 'Lewis Carroll', 2, 19.9), 
			('Martin Fierro', 'Jose Hernandez', 2, 25.9), 
			('Martin Fierro', 'Jose Hernandez', 3, 16.8)]
conexion.executemany("insert into libros(titulo, autor, codigoeditorial, precio) values (?,?,?,?)", valores)
conexion.commit()

print("\nMostramos la tabla 'libros':")
imprimir("select * from libros")

print("\nMostramos la tabla 'editoriales':")
imprimir("select * from editoriales")

print("\nCombinamos las tablas, relacionando codigoeditorial con editoriales.codigo:")
imprimir("select * from libros, editoriales on libros.codigoeditorial = editoriales.codigo")

print("\n[La diferencia con el codigo anterior es que al parecer, el join antes era implicito] Combinamos las tablas, relacionando codigoeditorial con editoriales.codigo:")
print("Probar con precaucion.")
imprimir("select * from libros join editoriales on libros.codigoeditorial = editoriales.codigo")

conexion.close()