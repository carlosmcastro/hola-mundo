import sqlite3 as sq
#Restricción "foreign key"
#coherencia entre el datos de tablas.
#impide eliminar datos dependientes entre tablas.

#no funciona tan bien en python, pero si en sql puro.

conexion = sq.connect("bd.db")
#permite que funcione foreign keys, dado a que estan desactivadas por defecto:
conexion.execute("PRAGMA foreign_keys=1") #tambien funciona on en lugar de 1, y off en lugar de 0
cur = conexion.cursor()

cur.executescript(" ".join(["drop table if exists "+i+";" for i in ("libros", 'editoriales')]))

cur.execute("""create table editoriales(
						codigo integer primary key,
						nombre text
					)""")

cur.execute("""create table libros(
						codigo integer primary key,
						titulo text,
						autor text,
						precio real,
						codigoeditorial integer,
						FOREIGN KEY(codigoeditorial) references editoriales(codigo)
					)""")					
conexion.commit()

#codigoeditorial integer references editoriales(codigo)
#es equivalente a foreign key

def imprimir(sql_ins):
	cursor = cur.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)			
					
valores = [('Planeta',),
		    ('Emece',),
		    ('Siglo XXI',)]
cur.executemany("insert into editoriales(nombre) values (?)", valores)			
print("\nMostramos las editoriales a usar:")
imprimir("select * from editoriales")

valores = [('El aleph', 'Borges', 2, 34),
		    ('Antología poética', 'Borges', 1, 39.5),
		    ('Java en 10 minutos', 'Mario Molina', 1, 50.5),
		    ('Alicia en el pais de las maravillas', 'Lewis Carroll', 2, 19.9),
		    ('Martin Fierro', 'Jose Hernandez', 2, 25.9),
		    ('Martin Fierro', 'Jose Hernandez', 3, 16.8)]
cur.executemany("insert into libros(titulo, autor, codigoeditorial, precio) values (?,?,?,?)", valores)
conexion.commit()

print("\nMostramos los libros a usar:")
imprimir("select * from libros")

print("""\nLas filas en libros se han podido ingresar, porque codigoeditorial esta entre 1-3
		 \nSi ingresamos un valor como 7 nos da error porque no existe tal elemento en editoriales.""")
		 
cur.execute("insert into libros(titulo, autor, codigoeditorial) values('JSP basico','Tornado Luis',7);")
conexion.commit()
imprimir("select * from libros")

print("\n")
cur.execute("delete from editoriales where codigo=1")
imprimir("select * from editoriales")

#ya se arreglo el problema, y funciona como debe funcionar.
"""
print("Por alguna razon el foreign key, es ignorado, no sé exacamente porque.")
print("Pero lo que debe hacer es: no permitir borrar tablas con dependecias(editoriales), ni sus valores, tampoco actualizarlos.")
print("Por la dependencia con libros.")"""


conexion.close()























