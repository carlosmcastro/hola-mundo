import sqlite3 as sq
#Manejo de datos de fecha, como entero y real.
#En lugar de tipo texto.

#Para el tipo entero, se usa tiempo de unix.
#Para el tipo real, Fecha Juliana.

conexion = sq.connect("bd.db")
cur = conexion.cursor()

cur.executescript(""" 
drop table if exists tabla1;
drop table if exists tabla2;

create table tabla1(
	fecha_hora integer
);
create table tabla2(
	fecha_hora real
);
""")
conexion.commit()

def imprimir(sql_ins):
	cursor = cur.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)

print("\nInsertamos una fila con fecha y hora en 'Tiempo de Unix' [Segundos transcurridos desde el 1 de enero de 1970]")
cur.execute("insert into tabla1 values (strftime('%s', 'now'))")

print("\nTabla1:")
imprimir("select * from tabla1")

print("\nDatos en formato legible:")
#unixepoch unix epoca
imprimir("select datetime(fecha_hora, 'unixepoch', 'localtime') from tabla1")

print("\nDatos en formato asignamo con strftime:")
imprimir("select strftime('%H:%M:%S %d/%m/%Y', datetime(fecha_hora, 'unixepoch', 'localtime')) from tabla1")

print("\nInsertamos otra fila en formato ISO 8601:")
cur.execute("insert into tabla1 values(strftime('%s', '2000-08-23 14:12:10'))")

print("\nMostramos las dos filas:")
print("\nTiempo Unix:")
imprimir("select * from tabla1")
print("\nLegible:")
imprimir("select datetime(fecha_hora, 'unixepoch', 'localtime') from tabla1")

print("\nInsertamos en la tabla2 una fecha en formato de 'Fecha Juliana':")
cur.execute("insert into tabla2 values (strftime('%J', 'now'))")

print("\nHacemos lo mismo, pero con la funcion 'julianday()':")
cur.execute("insert into tabla2 values (julianday('now'))")

conexion.commit()

print("\nMostramos las dos filas:")
print("\nFormato Juliano:")
imprimir("select * from tabla2")
print("\nFormato legible:")
imprimir("select datetime(fecha_hora) from tabla2")

conexion.close()