import sqlite3 as sq
#buscamos patrones con like y not like.

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
		
valores = [('Sertal', 'Roche', 5.2, 100), 
		   ('Buscapina', 'Roche', 4.1, 200), 
		   ('Amoxidal 500', 'Bayer', 15.6, 100), 
		   ('Paracetamol 500', 'Bago', 1.9, 200), 
		   ('Bayaspirina', 'Bayer', 2.1, 150), 
		   ('Amoxidal jarabe', 'Bayer', 5.1, 250), 
		   ('Sertal compuesto', 'Bayer', 5.1, 130), 
		   ('Paracetamol 1000', 'Bago', 2.9, 90), 
		   ('Amoxinil', 'Roche', 17.8, 230)]		
conexion.executemany("insert into medicamentos (nombre, laboratorio, precio, cantidad) values (?,?,?,?)", valores)
print("\nImprimimos los valores ingresados:")
imprimir("select * from medicamentos")

print("\nMostramos los medicamentos que comiencen por 'Amox':")
imprimir("select * from medicamentos where nombre like 'Amox%'")

print("\nMostramos los medicamentos que comiencen por 'Paracetamol' y precio menor a 2")
imprimir("select * from medicamentos where nombre like 'Paracetamol%' and precio <2")

print("\nMostramos los medicamentos que no contengan la cadena 'compuesto':")
imprimir("select * from medicamentos where nombre not like '%compuesto%'")

print("\nEliminamos los registros que contengan laboratorios con la letra y:")
conexion.execute("delete from medicamentos where laboratorio like '%y%'")
conexion.commit()
imprimir("select * from medicamentos")

print("\nActualizamos aquellos valores con nombre que comience por 'Paracetamos' y un precio mayor a 2, a un preco 5:")
conexion.execute("update medicamentos set precio = 5 where nombre like 'Paracetamol%' and precio>2")
conexion.commit()
imprimir("select * from medicamentos")

print("\nMostramos los medicamentos que terminen por 'l':")
imprimir("select nombre from medicamentos where nombre like '%l'")

print("\nMostramos los medicamentos que tengan 8 a más caracteres")
imprimir("select nombre from medicamentos where nombre like '"+"_"*8+"%'")

#comodines:
# % varios caracteres
# _ un caracter

conexion.close()