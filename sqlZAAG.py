import sqlite3 as sq
#Uso de subconsultas con multiples tablas.
#Cuando devuelve varios valores.


conexion = sq.connect("bd.db")
cur = conexion.cursor()

cur.executescript(""" 
drop table if exists libros;
drop table if exists editoriales;

create table editoriales(
	codigo integer primary key,
	nombre text
);
create table libros(
	codigo integer primary key,
	titulo text,
	autor text,
	precio real,
	codigoeditorial integer
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
valores = [('Uno', 'Richard Bach', 1),
		    ('Ilusiones', 'Richard Bach', 1),
		    ('Aprenda PHP', 'Mario Molina', 4),
		    ('El aleph', 'Borges', 2),
		    ('Puente al infinito', 'Richard Bach', 2)]
cur.executemany("insert into libros(titulo, autor, codigoeditorial) values (?,?,?)", valores)

conexion.commit()

print("\nEditoriales:")
imprimir("select * from editoriales")
print("\nLibros:")
imprimir("select * from libros")

print("\nMostramos las editoriales de los libros con el autor Richard Bach:")
imprimir("select nombre from editoriales where codigo in (select codigoeditorial from libros where autor = 'Richard Bach')")

print("\nVemos los codigoeditoriales de Richard Bach:")
imprimir("select codigoeditorial from libros where autor = 'Richard Bach'")

print("\nHacemos lo mismo con un join (combinaciones, más eficiente):")
#RECORDAR: distinct permite ver valores sin duplicados:
imprimir("select distinct nombre from editoriales as e join libros as l on codigoeditorial=e.codigo where autor = 'Richard Bach'")

print("\nEditoriales que no han publicado a Richard:")
imprimir("select nombre from editoriales where codigo not in (select codigoeditorial from libros where autor = 'Richard Bach')")

conexion.close()