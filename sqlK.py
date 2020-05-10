import sqlite3 as sq
#uso de in, para encontrar valores entre intervalos ó en conjuntos de datos.

conexion = sq.connect("bd.db")

conexion.execute("drop table if exists medicamentos")

conexion.execute("""create table medicamentos ( 
						codigo integer primary key,
						nombre text,
						laboratorio text,
						precio real,
						cantidad integer
					)""")

def imprimir(sql_ins):
	cursor = conexion.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)
					
valores = [('Sertal', 'Roche', 5.2, 1), 
		   ('Buscapina', 'Roche', 4.1, 3), 
		   ('Amoxidal 500', 'Bayer', 15.6, 100), 
		   ('Paracetamol 500', 'Bago', 1.9, 20), 
		   ('Bayaspirina', 'Bayer', 2.1, 150), 
		   ('Amoxidal jarabe', 'Bayer', 5.1, 250)]
conexion.executemany("insert into medicamentos (nombre, laboratorio, precio, cantidad) values (?,?,?,?)", valores)

print("\nMostramos los valores ingresados:")
imprimir("select * from medicamentos")

print("\nRecuperamos nombre y precio; de aquellos medicamentos que sean del laboratorio Bayer o Bago:")
imprimir("select nombre, precio from medicamentos where laboratorio in ('Bayer', 'Bago')")

print("\nComparamos el uso con between e in:")

print("\nBetween:")
imprimir("select * from medicamentos where cantidad between 1 and 5")

print("\nIn:")
imprimir("select * from medicamentos where cantidad in (1,2,3,4,5)")
conexion.close()