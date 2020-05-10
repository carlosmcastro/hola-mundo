import sqlite3 as sq
#tipo de datos en sql.
#blob es para archivos binarios, como imagenes. (averiguar como se usa)
#insertar, executemany, eliminar valores, ver valores con uso de where filtro.


conexion = sq.connect("bd.db")

def imprimir(sql_ins):
	cursor = conexion.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)

print("Eliminamos la tabla libros si existe.")
conexion.execute("drop table if exists libros;")

#real es flotante, text es string, integer es int (entero)
try:
	print("Creando tabla.")
	conexion.execute(""" 
			create table libros (
				titulo text,
				autor text,
				editorial text,
				precio real,
				cantidad integer
			);
	""")
except sq.OperationalError:
	print("La tabla ya existe...")
	
print("Insertamos algunos valores.")
#esto es equivalente a lo de abajo.
valores = [('El magazo', 'Un sujeto', 'Norma', 78.45, 23),
		   ('Rayuela', 'Cortázar', 'Pepito', 2.5, 223),
		   ('Milagros', 'El milagrero', 'Vacacio', 8.2, 198),
		   ('Un mundo feliz', 'Aldoux Huxley', 'Laralanda', 7, 2334)]
conexion.executemany("""insert into libros (titulo, autor, editorial, precio, cantidad) 
						values (?,?,?,?,?);""", valores)
'''
conexion.execute("""insert into libros (titulo, autor, editorial, precio, cantidad) 
					values ('El magazo', 'Un sujeto', 'Norma', 78.45, 23);
					""")
conexion.execute("""					insert into libros (titulo, autor, editorial, precio, cantidad) 
					values ('Rayuela', 'Cortázar', 'Pepito', 2.5, 223);
					""")
conexion.execute("""					insert into libros (titulo, autor, editorial, precio, cantidad) 
					values ('Milagros', 'El milagrero', 'Vacacio', 8.2, 198);
					""")
conexion.execute("""					insert into libros (titulo, autor, editorial, precio, cantidad) 
					values ('Un mundo feliz', 'Aldoux Huxley', 'Laralanda', 7, 2334);
					""")
'''
conexion.commit()

# * permite recuperar todas la columnas definidas en la tabla.
print("Mostramos el dato almacenado:")
imprimir("select * from libros;")

print("\nMostramos las filas que tengan de autor a Cortázar:")
imprimir("select * from libros where autor = 'Cortázar';")

print("\nMostramos los titulos de la editorial Norma:")
imprimir("select titulo from libros where editorial = 'Norma'")

print("\nMostrasmos la editorial de Un mundo feliz:")
imprimir("select editorial from libros where titulo = 'Un mundo feliz'")

print("\nMostramos los registros con titulo distinto a Rayuela:")
imprimir("select * from libros where titulo <> 'Rayuela'")

print("\nMostramos los titulos y precios de aquellos valores que cuesten menos de 8 en precio:")
imprimir("select titulo, precio from libros where precio<8")

print("\nMostramos los titulos y precios de aquellos valores que cuesten menos(o iguales) a 8.2 en precio:")
imprimir("select titulo, precio from libros where precio<=8.2")

print("\n\nProbamos ahora eliminando elementos.")
print("\nEliminamos el elemento del registro que valga 8.2 o más:")
conexion.execute("delete from libros where precio >= 8.2;")
conexion.commit()
imprimir("select * from libros;")

print("\nEliminamos todos los elementos:")
conexion.execute("delete from libros;")
conexion.commit()
imprimir("select * from libros;")

conexion.close()












