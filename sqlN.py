import sqlite3 as sq
import re
#Uso de expresiones regulares para filtrar contenido.
#en sql puro solo se necesita de regexp, sin importar re, pero en python.
#se debe usar re module.


conexion = sq.connect("bd.db")

conexion.execute("drop table if exists libros")

conexion.execute("""create table libros (
						codigo integer primary key,
						titulo text,
						autor text,
						editorial text,
						precio real
					)""")
					
#Es necesario definir esta funcion en python.
def regexp(expresion, item):
	reg = re.compile(expresion)
	#reg es un objeto re (regular expresion) para filtrar.
	#item es el elemento a observar. (Por ejemplo titulo es pasado, pasa a la funcion cada titulo)
	#es necesario convertir a string en python para procesar la expresion regular, en sql puro no es necesario.
	return reg.search(str(item)) is not None #aquí busca la expresion regular, y la retorna si es distinta de None.
	#No retorna directamente al cadena sino un dato re, con la posicion de la 'expresion' dentro del item.
					
def imprimir(sql_ins):
	cursor = conexion.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)
					
conexion.create_function("regexp", 2, regexp) #Nombre, número de parametros que acepta la funcion. La funcion a usar.
valores = [('El aleph', 'Borges', 'Planeta', 15.5), 
		   ('Martin Fierro', 'Jose Hernandez', 'Emece', 22.9), 
		   ('Antologia poetica', 'J.L. Borges', 'Planeta', 39), 
		   ('Aprenda PHP', 'Mario Molina', 'Emece', 19.5), 
		   ('Cervantes y el quijote', 'Bioy Casare- J.L. Borges', 'Paidos', 35.4), 
		   ('El Manual de PHP', 'J.C. Paez', 'Paidos', 19), 
		   ('Harry Potter y la piedra filosofal', 'J.K. Rowling', 'Paidos', 45.0), 
		   ('Harry Potter y la camara secreta', 'J.K. Rowling', 'Paidos', 46.0), 
		   ('Alicia en el pais de las maravillas', 'Lewis Carroll', 'Paidos', 36.0)]
conexion.executemany("insert into libros (titulo, autor, editorial, precio) values (?,?,?,?)", valores)
conexion.commit()

print("\nMostramos la tabla de libros:")
imprimir("select * from libros")

print("\nMostramos los valores que contienen la cadena 'Ma':")
imprimir("select * from libros where titulo regexp 'Ma'")

print("\nMostramos autor y titulo para aquellos valores que tienen en el autor un H ó k ó w:")
#en sql no importan las mayusculas para las funciones. No es casesensitive.
imprimir("select autor, titulo from libros where autor REGEXP '[Hkw]'")

print("\nMostramos los autores que contienen al menos una letra entre la a y la d:")
imprimir("select autor from libros where autor regexp '[a-d]'")

print("\nVemos los libros que comienzan con A:")
imprimir("select titulo from libros where titulo regexp '^A'")

print("\nVemos los libros que terminan con HP:")
imprimir("select titulo from libros where titulo regexp 'HP$'")

print("\nBuscamos titulos que contengan una a, luego un caracter cualquiera, y luego una e:")
imprimir("select titulo from libros where titulo regexp 'a.e'")

print("\nBuscamos titulos que contengan una a, luego dos caracter cualquiera, y luego una e:")
imprimir("select titulo from libros where titulo regexp 'a..e'")

print("\nBuscamos autores que contengan exactamente 13 caracteres:")
imprimir("select autor from libros where autor regexp '^"+"."*13+"$'")

print("\nBuscamos autores que contengan al menos 7 caracteres:")
imprimir("select autor from libros where autor regexp '.......'")

print("\nAñadimos un libro a la lista:")
conexion.execute("insert into libros (titulo,autor,editorial,precio) values('Como ganar $ en esta vida','Rodriguez Pablo','Paidos',25.00)")
imprimir("select * from libros")

print("\nBuscamos un caracter especial de expresiones regulares $, con el uso de \:")
imprimir("select * from libros where titulo regexp '\$'")

print("\nAñadimos dos libros a la lista:")
conexion.execute("insert into libros (titulo,autor,editorial,precio) values('Python','Charles Dierbach','Wiley',100.24)")
conexion.execute("insert into libros (titulo,autor,editorial,precio) values('Jacaro','Chru choh','wooe',1040.24)")
conexion.commit()
imprimir("select * from libros")

print("\nBuscamos los precios que tengan los digitos entre el 0 y el 9, y que sean continuos entre 3 a 6 ocasiones, por ejemplo:")
print("221.23 es valido, pero 22.21 no, porque posee a el caracter '.' que no esta entre 0 y 9.")
#nota sobre regexp, {3, 6} marca error porque toma en cuenta al espacio, debe ser {3,6}
imprimir("select titulo, precio from libros where precio regexp '[0-9]{3,6}'")


conexion.close()