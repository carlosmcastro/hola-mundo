import sqlite3 as sq
#uso de inner join, resumido join.
#combinaciones internas.
#si un valor de la primera tabla no aparece en la segunda, el registro no aparece.


conexion = sq.connect("bd.db")

conexion.execute("drop table if exists provincias")
conexion.execute("drop table if exists clientes")

conexion.execute("""create table provincias(
						codigo integer primary key,
						nombre text
					)""")
conexion.execute("""create table clientes(
						codigo integer primary key,
						nombre text,
						domicilio text,
						ciudad text,
						codigoprovincia integer
					)""")
					
def imprimir(sql_ins):
	cursor = conexion.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)

valores = [('Cordoba',),('Santa Fe',),('Corrientes',)]
conexion.executemany("insert into provincias(nombre) values (?)", valores)

valores = [('Lopez Marcos', 'Colon 111', 'CÃ³rdoba', 1),
		   ('Perez Ana', 'San Martin 222', 'Cruz del Eje', 1),
		   ('Garcia Juan', 'Rivadavia 333', 'Villa Maria', 1),
		   ('Perez Luis', 'Sarmiento 444', 'Rosario', 2),
		   ('Pereyra Lucas', 'San Martin 555', 'Cruz del Eje', 1),
		   ('Gomez Ines', 'San Martin 666', 'Santa Fe', 2),
		   ('Torres Fabiola', 'Alem 777', 'Ibera', 7)]
conexion.executemany("insert into clientes(nombre, domicilio, ciudad, codigoprovincia) values (?,?,?,?)", valores)
conexion.commit()

print("\nMostramos la tabla de provincias:")
imprimir("select * from provincias")

print("\nMostramos la tabla de clientes:")
imprimir("select * from clientes")

#Notese que el dato con 7 no aparece, por no estar en la segunda tabla.
print("\nObtenemos los datos de ambas tablas, con alias:")
imprimir("select c.nombre, domicilio, ciudad, p.nombre from clientes as c join provincias as p on c.codigoprovincia=p.codigo")

print("\nObtenemos la misma informacion, pero ordenada por nombre de provincia:")
imprimir("select c.nombre, domicilio, ciudad, p.nombre from clientes as c join provincias as p on c.codigoprovincia=p.codigo order by p.nombre")

print("\nRecuperamos los clientes de la provincia de Santa Fe:")
imprimir("select c.nombre, domicilio, ciudad from clientes as c join provincias as p on c.codigoprovincia=p.codigo where p.nombre = 'Santa Fe'")		   
		   
conexion.close()