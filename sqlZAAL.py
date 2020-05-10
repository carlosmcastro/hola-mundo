import sqlite3 as sq
#comparaciones de join y suboconsultas.

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

valores = [('Alicia en el pais de las maravillas', 'Lewis Carroll', 'Emece', 20.0),
		    ('Alicia en el pais de las maravillas', 'Lewis Carroll', 'Plaza', 35.0),
		    ('Aprenda PHP', 'Mario Molina', 'Siglo XXI', 40.0),
		    ('El aleph', 'Borges', 'Emece', 10.0),
		    ('Ilusiones', 'Richard Bach', 'Planeta', 15.0),
		    ('Java en 10 minutos', 'Mario Molina', 'Siglo XXI', 50.0),
		    ('Martin Fierro', 'Jose Hernandez', 'Planeta', 20.0),
		    ('Martin Fierro', 'Jose Hernandez', 'Emece', 30.0),
		    ('Uno', 'Richard Bach', 'Planeta', 10.0)]
cur.executemany("insert into libros(titulo, autor, editorial, precio) values (?,?,?,?)", valores)

conexion.commit()

print("\nLibros:")
imprimir("select * from libros")

print("\nLibros publicados por distintas editoriales (con subconsulta):")
imprimir("select distinct l1.titulo from libros as l1 where l1.titulo in (select titulo from libros as l2 where l2.editorial <> l1.editorial)")

print("\nLibros publicados por distintas editoriales (con join):")
imprimir("select distinct l1.titulo from libros as l1 join libros as l2 on l1.titulo=l2.titulo where l1.editorial <> l2.editorial")

print("\nLibros que tienen el mismo precio que 'El aleph' (con subconsulta):")
imprimir("select titulo from libros where titulo<>'El aleph' and precio=(select precio from libros where titulo='El aleph')")

print("\nLibros que tienen el mismo precio que 'El aleph' (con join):")
#nota el orden de l1 y l2 importa.
imprimir("select l1.titulo from libros as l1 join libros as l2 on l1.precio=l2.precio where l2.titulo='El aleph' and l1.titulo<>l2.titulo")

print("\nLibros cuyo precio supera el precio promedio por editorial (con subconsulta):")
imprimir("""select l1.titulo, l1.precio, l1.editorial from libros as l1 
			where l1.precio > (select avg(l2.precio) from libros as l2 where l1.editorial=l2.editorial)""")

print("\nLibros cuyo precio supera el precio promedio por editorial (con join, usando having):")
imprimir("""select l1.titulo, l1.precio, l1.editorial from libros as l1 join 
			libros as l2 on l1.editorial=l2.editorial group by l1.titulo, l1.editorial, l1.precio having l1.precio > avg(l2.precio)""")

conexion.close()