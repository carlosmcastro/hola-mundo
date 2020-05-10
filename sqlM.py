import sqlite3 as sq
#contar valores en tablas.
#y funciones de agrupamiento (sum, max, min, avg)

conexion = sq.connect("bd.db")

conexion.execute("drop table if exists medicamentos")

conexion.execute("""create table medicamentos(
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
					
valores = [('Sertal', None, None, 100), 
		   ('Buscapina', None, 4.1, None), 
		   ('Amoxidal 500', 'Bayer', 15.6, 100), 
		   ('Paracetamol 500', 'Bago', 1.9, 200), 
		   ('Bayaspirina', 'Bayer', 2.1, 150), 
		   ('Amoxidal jarabe', 'Bayer', 5.1, 250), 
		   ('Sertal compuesto', 'Bayer', 5.1, 130), 
		   ('Paracetamol 1000', 'Bago', 2.9, 90), 
		   ('Amoxinil', 'Roche', 17.8, 230)]
conexion.executemany("insert into medicamentos (nombre, laboratorio, precio, cantidad) values (?,?,?,?)", valores)
conexion.commit()

print("\nImprimimos los datos de la tabla:")
imprimir("select * from medicamentos")

print("\nMostramos la cantidad de registros (filas de la tabla):")
imprimir("select count(*) from medicamentos") #con cursor.fetchone() en este caso es suficiente.

print("\nMostramos la cantidad de registros no nulos de laboratorios")
imprimir("select count(laboratorio) from medicamentos")

print("\nAsignamos alias al precio y la cantidad, y mostramos la cantidad de valores no nulos de cada uno:")
imprimir("select count(precio) as conprecio, count(cantidad) as concantidad from medicamentos")

print("\nMostramos la cantidad de precios de medicamentos que tengan nombres que comiencen con 'B':")
imprimir("select count(precio) from medicamentos where nombre like 'B%'")

print("\nUSO DE MAX, MIN, SUM Y AVG:")

print("\nMostramos el precio más costoso y luego su nombre y precio.:")
imprimir("select max(precio) from medicamentos")
imprimir("select nombre, max(precio) from medicamentos")

print("\nMostramos la menor cantidad disponible y luego su nombre y cantidad.:")
imprimir("select min(cantidad) from medicamentos")
imprimir("select nombre, min(cantidad) from medicamentos")

print("\nMostramos el precio promedio:")
imprimir("select avg(precio) from medicamentos")

print("\nMostramos la cantidad total de expensas en productos:")
imprimir("select sum(cantidad) from medicamentos")

print("\nMostramos la cantidad total de expensas de productos Bayer")
imprimir("select sum(cantidad) from medicamentos where laboratorio='Bayer'")

conexion.close()
















