import sqlite3 as sq
#Los mototes SQL por defecto son tablas sin rowid.
#id que identifica la fila.
#Pero SQLite lo añade por defecto, como autoincremental.
#Por tanto hay un comando para desactivar la creación de rowid.
#Debe tomarse en cuenta que cuando se usa without rowid, debe declararse una
#variable tipo primary key (esto es obligatorio).


conexion = sq.connect("bd.db")
cur = conexion.cursor()

#creamos una tabla sin rowid.
cur.executescript(""" 
drop table if exists usuarios;

create table usuarios(
	nombre text primary key,
	clave text
) without rowid;
""")
conexion.commit()

def imprimir(sql_ins):
	cursor = cur.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)

def insertar():
	valores = [('marcos','zaddwdf1'),
			   ('ana','123qtew'),
			   ('luis','gfd32dsd')]
	cur.executemany("insert into usuarios values (?,?)", valores)

	conexion.commit()
	
insertar()

print("\nUsuarios:")
imprimir("select * from usuarios")

print("\nIntentamos a la columna rowid:")
try:
	imprimir("select rowid from usuarios")
except sq.OperationalError:
	print("\n\tNo se encuentra la columna RowId.")
	
print("\nBorramos la tabla y la volvemos a crear con el RowId activado:")
cur.executescript("""
drop table usuarios;
create table usuarios (
	nombre text primary key,
	clave text
);
""")
insertar()

print("\nMostramos la tabla usuarios, con el RowId:")
imprimir("select rowid, nombre, clave from usuarios")

conexion.close()