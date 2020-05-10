import sqlite3 as sq
#uso de between para filtrar valores intermedios.
#Incluyendo los extremos.

conexion = sq.connect("bd.db")

conexion.execute("drop table if exists autos")

conexion.execute("""create table autos (
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
		   ('GD123TY', 'Renault Clio', 1995, 70000), 
		   ('CC333MG', 'Renault Megane', 1998, 95000), 
		   ('BV543QE', 'Fiat 128', 1975, 20000)]
conexion.executemany("insert into autos (patente, marca, modelo, precio) values (?,?,?,?)", valores)
conexion.commit()
print("\nMostramos los datos:")
imprimir("select * from autos")

print("\nAutos entre 1970 y 1990; y se ordenan los datos por el modelo:")
imprimir("select * from autos where modelo between 1970 and 1990 order by modelo")

print("\nAutos entre un precio de 50000 y 100000 (sin ordenar):")
imprimir("select * from autos where precio between 50000 and 100000")

print("\nSeleccionamos usando jerarquia alfabetica, para seleccionar los valores entre.")
print("Fiat 128 y Peugeot 505:")
imprimir("select * from autos where marca between 'Fiat 128' and 'Peugeot 505'")

conexion.close()