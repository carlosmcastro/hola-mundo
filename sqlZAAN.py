import sqlite3 as sq

#uso de delete y update con subconsultas

conexion = sq.connect("bd.db")
cur = conexion.cursor()

cur.executescript(""" 
drop table if exists libros;
drop table if exists editoriales;

create table libros(
	codigo integer primary key,
	titulo text,
	autor text,
	precio real,
	codigoeditorial integer
);
create table editoriales(
	codigo integer primary key,
	nombre text
);
""")
conexion.commit()

def imprimir(sql_ins):
	cursor = cur.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)

valores = [('Planeta',),
		    ('Emece',),
		    ('Paidos',),
		    ('Siglo XXI',)]
cur.executemany("insert into editoriales(nombre) values (?)", valores)
valores = [('Uno', 'Richard Bach', 1, 15),
		    ('Ilusiones', 'Richard Bach', 2, 20),
		    ('El aleph', 'Borges', 3, 10),
		    ('Aprenda PHP', 'Mario Molina', 4, 40),
		    ('Poemas', 'Juan Perez', 1, 20),
		    ('Cuentos', 'Juan Perez', 3, 25),
		    ('Java en 10 minutos', 'Marcelo Perez', 2, 30)]
cur.executemany("insert into libros(titulo, autor, codigoeditorial, precio) values (?,?,?,?)", valores)

conexion.commit()

print("\nLibros:")
imprimir("select * from libros")
print("\nEditoriales:")
imprimir("select * from editoriales")

print("\nActualizamos el precio (incrementandolo un 10%) en todos los libros de la editorial Emece:")
cur.execute("update libros set precio = precio + (precio*0.10) where codigoeditorial = (select codigo from editoriales where nombre='Emece')")
imprimir("select * from libros")

print("\nEliminamos todos los libros de las editoriales donde se ha publicado algo de Juan Perez:")
cur.execute("""delete from libros where codigoeditorial in (select e.codigo from editoriales as e 
				join libros on e.codigo=codigoeditorial where autor='Juan Perez')""")
imprimir("select * from libros")

conexion.close()