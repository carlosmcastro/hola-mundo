import sqlite3 as sq
#El tipado de SQL en general es estatico.
#Pero en SQLite es dinamico, excepto para los datos primary key.
#Esto permite ingresar datos tipo texto en campos integer.
#O generar campos "sin tipo".


conexion = sq.connect("bd.db")
cur = conexion.cursor()

cur.executescript(""" 
drop table if exists tabla1;
drop table if exists personas;
drop table if exists articulos;

create table tabla1(
		codigo integer primary key,
		campo1
);
create table personas(
	nombre text,
	cantidad_hijos integer
);
create table articulos(
	codigo integer primary key,
	descripcion text,
	precio real
);
""")
conexion.commit()

def imprimir(sql_ins):
	cursor = cur.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)

valores = [(1,),
		   (5.25,),
		   ('admin',),
		   (None,)]
cur.executemany("insert into tabla1(campo1) values (?)", valores)

valores = [('juan', 2),
		   ('ana', 7),
		   ('luis', 'no tiene')]
cur.executemany("insert into personas values (?,?)", valores)

conexion.commit()

print("\nTabla1 (notese que el campo1 'sin tipo', le asigna automaticamente un tipo apropiado a cada dato):")
#typeof() devuelve el tipo del dato ingresado.
imprimir("select *, typeof(campo1) from tabla1")

print("\nPersonas (notese que cantidad_hijos es tipo integer, y se a ingresado un dato tipo text):")
imprimir("select *, typeof(cantidad_hijos) from personas")

print("\nEl tipo integer sigue siendo necesario, por ejemplo para sumar los datos de esa columna:")
imprimir("select sum(cantidad_hijos) from personas")
print("\nNotese que suma todos los datos tipo integer e ignora el dato tipo text en los calculos.")
print("Esto es propio de SQLite respecto a otros gestores de bases de datos.")

print("\nIntentamos insertar un dato distinto a integer en el codigo de tabla Articulos:")
try:
	cur.execute("insert into articulos values('hola', 'papas', 12.5)")
except sq.IntegrityError:
	print("\n\tNo se puede insertar un dato tipo text en un dato integer primary key,")

conexion.close()