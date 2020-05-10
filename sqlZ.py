import sqlite3 as sq
#combinar más de dos tablas.

conexion = sq.connect("bd.db")

conexion.executescript("""drop table if exists libros;
						  drop table if exists editoriales;
						  drop table if exists autores;""")

conexion.execute("""create table libros(
						codigo integer primary key,
						titulo text,
						codigoautor integer,
						codigoeditorial integer,
						precio real
					)""")
conexion.execute("""create table editoriales(
						codigo integer primary key,
						nombre text
					)""")
conexion.execute("""create table autores(
						codigo integer primary key,
						nombre text
					)""")

def imprimir(sql_ins):
	cursor=conexion.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)
		
ver_todos = "select * from "
print("\nInsertamos las editoriales a usar:")
valores = [('Planeta',),
		    ('Emece',),
		    ('Siglo XXI',),
		    ('Plaza',)]
conexion.executemany("insert into editoriales(nombre) values(?)", valores)
imprimir(ver_todos+"editoriales")

print("\nInsertamos los autores a usar:")
valores = [('Richard Bach',),
		    ('Borges',),
		    ('Jose Hernandez',),
		    ('Mario Molina',),
		    ('Paenza',)]
conexion.executemany("insert into autores(nombre) values(?)", valores)
imprimir(ver_todos+"autores")


print("\nInsertamos los libros a usar:")
valores = [('El aleph', 2, 2, 20),
		    ('Martin Fierro', 3, 1, 30),
		    ('Aprenda PHP', 4, 3, 50),
		    ('Uno', 1, 1, 15),
		    ('Java en 10 minutos', 0, 3, 45),
		    ('Matematica estas ahi', 0, 0, 15),
		    ('Java de la A a la Z', 4, 0, 50)]
conexion.executemany("insert into libros(titulo, codigoautor, codigoeditorial, precio) values (?,?,?,?)", valores)
imprimir(ver_todos+"libros")

print("\nCombinamos las tres tablas en una, con dos join 'comunes' (inner join):")
imprimir("""select titulo, a.nombre, e.nombre, precio 
				from libros as l join editoriales as e 
					on codigoeditorial=e.codigo
				join autores as a
					on codigoautor=a.codigo""")
					
print("\nCombinamos las tres tablas en una, usando dos tipos distintos de join, inner y left:")
imprimir("""select titulo, a.nombre, e.nombre, precio
				from libros as l join autores as a
					on codigoautor=a.codigo
				left join editoriales as e
					on codigoeditorial=e.codigo""")
					
print("\nRECORDATORIO: Left join completa los datos faltantes con Null (None en python), en la tabla izquierda.")
print("join ignora los valores no coincidentes.")
conexion.close()