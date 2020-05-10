import sqlite3 as sq
#primer uso de subconsultas.
#consultas anidas.
#pueden ser reemplazadas por lo general por combinaciones.
#que son más eficientes. Pero que suelen ser más engorrosas.
#En este caso solo devuelve un valor.

conexion = sq.connect("bd.db")
cur = conexion.cursor()

cur.executescript(""" 
drop table if exists libros;

create table libros(
		codigo integer primary key,
		titulo text,
		autor text,
		editorial text,
		precio real
);
""")
conexion.commit()

def imprimir(sql_ins):
	cursor = cur.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)

valores = [('Uno', 'Richard Bach', 'Planeta', 10.0),
		    ('El aleph', 'Borges', 'Emece', None),
		    ('Antología poética', 'Borges', 'Planeta', 39.5),
		    ('Java en 10 minutos', 'Mario Molina', 'Planeta', 50.5),
		    ('Alicia en el pais de las maravillas', 'Lewis Carroll', 'Emece', 19.9),
		    ('Martin Fierro', 'Jose Hernandez', 'Emece', 25.9),
		    ('Martin Fierro', 'Jose Hernandez', 'Paidos', 16.8),
		    ('Aprenda PHP', 'Mario Molina', 'Emece', 19.5),
		    ('Cervantes y el quijote', 'Borges', 'Paidos', 18.4)]
cur.executemany("insert into libros(titulo, autor, editorial, precio) values (?,?,?,?)", valores)

conexion.commit()

print("\nLibros:")
imprimir("select * from libros")

print("\nMostramos el titulo, precio, y diferencia (precio, respecto del maximo) del libro llamado 'Uno':")
imprimir("select titulo, precio, -precio + (select max(precio) from libros) as diferencia from libros where titulo='Uno'")

print("\nMostramos el titulo, autor, precio del libro más costoso:")
imprimir("select titulo, autor, precio from libros where precio = (select max(precio) from libros)")

print("\nActualizamos el precio del libro más costoso a 45:")
cur.execute("update libros set precio = 45 where precio = (select max(precio) from libros)")
imprimir("select * from libros")

print("\nEliminamos los libros con el menor precio:")
cur.execute("delete from libros where precio = (select min(precio) from libros)")
imprimir("select * from libros")

conexion.close()