import sqlite3 as sq
#ordenar valores.
#uso de not and y or

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
		
print("\nIngresamos unos datos a la tabla:")
valores = [('Sertal', 'Roche', 5.2, 100), 
		   ('Buscapina', 'Roche', 4.1, 200), 
		   ('Amoxidal 500', 'Bayer', 15.6, 100), 
		   ('Paracetamol 500', 'Bago', 1.9, 200), 
		   ('Bayaspirina', 'Bayer', 2.1, 150), 
		   ('Amoxidal jarabe', 'Bayer', 5.1, 250)]
conexion.executemany("insert into medicamentos (nombre, laboratorio, precio, cantidad) values (?,?,?,?)", valores)
conexion.commit()

print("\nMostramos los datos:")
imprimir("select * from medicamentos")

print("\nOrdenamos por precio de mayor a menor.")
imprimir("select * from medicamentos order by precio desc")

print("\nOrdenamos por cantidad de menor a mayor(por defecto). Y a traves de su numero de posicion.")
imprimir("select * from medicamentos order by 5")

print("\nAnidamos el orden. Primero ordenamos por laboratorio en orden descendente.")
print("Y por cada laboratorio se ordena por cantidad en orden ascendente.")
imprimir("select * from medicamentos order by laboratorio desc, cantidad asc")

print("\nAHORA APLICAMOS EL USO DE NOT, AND y OR")

print("\nMostramos los nombres que sean del laboratorio Roche y con precio menor a 5:")
imprimir("select codigo, nombre from medicamentos where laboratorio='Roche' and precio<5")

print("\nMostramos los valores que sean de Roche o el precio menor a 5:")
imprimir("select * from medicamentos where laboratorio='Roche' or precio<5")

print("\nMostramos los valores que no sean de Bayer:")
imprimir("select * from medicamentos where not laboratorio='Bayer'")

print("\nMostramos los valores que no sean de Bayer y la cantidad sea 100:")
imprimir("select * from medicamentos where not laboratorio='Bayer' and cantidad = 100")

print("\nEliminamos todos los registros que sean de Bayer y con el precio mayor a 10:")
conexion.execute("delete from medicamentos where laboratorio='Bayer' and precio>10")
conexion.commit()
imprimir("select * from medicamentos")

print("\nActualizamos a 200 la cantidad de los laboratorio Roche con precio mayor a 5")
conexion.execute("update medicamentos set cantidad = 200 where laboratorio = 'Roche' and precio>5")
conexion.commit()
imprimir("select * from medicamentos")

print("\nEliminamos los registros que sean de Bayer o con el precio menor a 3")
conexion.execute("delete from medicamentos where laboratorio = 'Bayer' or precio<3")
conexion.commit()
imprimir("select * from medicamentos")

conexion.close()














