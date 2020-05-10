import sqlite3 as sq
#foreign key acciones
#por defecto es no action.
#no action: si se elimina o actualiza una tabla.
#	la accion no se realiza y lanza error.
#cascade: si se altera la clave primaria, las referenciadas.
#	tambien lo hacen.
#set null: estable con valor null en el campo de clave foránea.
#set default: establece valor por defecto. Idem.
#restrict: restringe eliminar, una o más claves principales.
#	si hay valores asociados a ellas.

#SE HA ARREGLADO EL USO DE CLAVE FORANEA EN PYTHON.


conexion = sq.connect("bd.db")
conexion.execute("PRAGMA foreign_keys = 1") #usamos este comando para activar la clave foranea.
cur = conexion.cursor()

cur.executescript(""" 
drop table if exists editoriales;
drop table if exists libros;

create table editoriales(
		codigo integer primary key,
		nombre text
);
create table libros(
		codigo integer primary key,
		titulo text,
		autor text,
		codigoeditorial integer references editoriales(codigo) on delete cascade on update cascade
);
""")
conexion.commit()

def imprimir(sql_ins):
	cursor = cur.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)

valores = [('Emece',),
		    ('Planeta',),
		    ('Siglo XXI',)]
cur.executemany("insert into editoriales(nombre) values (?)", valores)

valores = [('El aleph', 'Borges', 1),
		    ('Martin Fierro', 'Jose Hernandez', 2),
		    ('Aprenda PHP', 'Mario Molina', 2)]
cur.executemany("insert into libros(titulo, autor, codigoeditorial) values (?,?,?)", valores)
conexion.commit()

print("\nEditoriales:")
imprimir("select * from editoriales")

print("\nLibros:")
imprimir("select * from libros")

print("\nActualizamos el codigo de editorial:")
cur.execute("update editoriales set codigo=10 where codigo=1")
conexion.commit()
imprimir("select * from libros")

print("\nEditoriales:")
imprimir("select * from editoriales")

print("\nEliminamos la editorial codig=2:")
cur.execute("delete from editoriales where codigo=2")
imprimir("select * from libros")
print()
imprimir("select * from editoriales")


conexion.close()





