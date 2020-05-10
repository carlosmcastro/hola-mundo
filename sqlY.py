import sqlite3 as sq

#uso de grop by, para hacer operaciones entre varias columnas.
#funciones de agrupamiento.

conexion = sq.connect("bd.db")

conexion.execute("drop table if exists libros")
conexion.execute("drop table if exists editoriales")

def imprimir(sql_ins):
	cursor = conexion.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)

conexion.executescript("""
	create table libros (
		codigo integer primary key,
		titulo text,
		autor text,
		codigoeditorial integer,
		precio real
	);
	create table editoriales(
		codigo integer primary key,
		nombre text
	);
""")

valores = [*zip(['Planeta', 'Emece', 'Siglo XXI'])]
conexion.executemany("insert into editoriales(nombre) values (?)", valores)
valores = [('El aleph', 'Borges', 2, 34),
		   ('AntologÃ\xada poÃ©tica', 'Borges', 1, 39.5),
		   ('Java en 10 minutos', 'Mario Molina', 1, 50.5),
		   ('Alicia en el pais de las maravillas', 'Lewis Carroll', 2, 19.9),
		   ('Martin Fierro', 'Jose Hernandez', 2, 25.9),
		   ('Martin Fierro', 'Jose Hernandez', 3, 16.8)]
conexion.executemany("insert into libros(titulo, autor,codigoeditorial, precio) values (?,?,?,?)", valores)
conexion.commit()

print("\nMostramos la tabla de libros:")
imprimir("select * from libros")

print("\nMostramos la tabla de editoriales:")
imprimir("select * from editoriales")

print("\nContamos la cantidad de libros de cada editorial.")
print("Consultando en las dos tablas:")
imprimir("select nombre as editorial, count(*) as cantidad from editoriales as e join libros as l on codigoeditorial=e.codigo group by e.nombre")

print("\nBuscamos el libros más costoso por editorial, haciendo uso de join y left join.")
print("\nJoin:")
imprimir("select titulo as libro, nombre as editorial, max(precio) from editoriales as e join libros as l on codigoeditorial=e.codigo group by nombre")
print("\nLeft Join:")
imprimir("select titulo as libro, nombre as editorial, max(precio) from editoriales as e left join libros as l on codigoeditorial=e.codigo group by nombre")

print("\nLeft join podría ser más util en estos casos si se quiere abarcar más datos para cierta columna.")

conexion.close()