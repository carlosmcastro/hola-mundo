import sqlite3 as sq
#uso de limit y offset para seleccionar una cantidad de registros.
#offset no puede usarse sin limit.

conexion = sq.connect("bd.db")

conexion.execute("drop table if exists autos")

conexion.execute("""create table autos( 
						patente text primary key,
						marca text,
						modelo integer,
						precio real
					)""")

def imprimir(sql_ins):
	cursor = conexion.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)
					
valores = [('AC123FG', 'Fiat 128', 1970, 15000),
		   ('AC234GG', 'Renault 11', 1980, 40000),
		   ('CD333QQ', 'Peugeot 505', 1990, 80000),
		   ('GD123TY', 'Renault Clio', 1990, 70000),
		   ('CC333MG', 'Renault Megane', 1998, 95000),
		   ('BV543TR', 'Fiat 128', '1975', 20000)]		
conexion.executemany("insert into autos (patente, marca, modelo, precio) values (?,?,?,?)", valores)
conexion.commit()

print("\nMostramos los datos ingresados:")
imprimir("select * from autos")

print("\nOrdenamos por precio, en valores descencientes (de mayor a menor); limitando 3 datos:")
imprimir("select * from autos order by precio desc limit 3")

print("\nOrdenamos por precio, valor por defecto(asc de menor a mayor), mostramos el primer valor desde el segundo valor.")
print("recordar que offset comienza en 0")
imprimir("select * from autos order by precio limit 1 offset 1")

print("\nOrdenamos por precio, de forma descendiente. Usamos la version comprmida de limit.")
print("limit 2,3 el primer valor es el offset y el segundo los valores a tomar:")
imprimir("select * from autos order by precio desc limit 2,3")

print("\nUsamos limit sin ordenar, tomamos 2 valores:")
imprimir("select * from autos limit 2")
					
conexion.close()