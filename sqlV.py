import sqlite3 as sq
#uso de outer join por izquierda.
#left join.
#combina tablas, mostrando datos faltantes, priorizando.
#la primera tabla.

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
		   ('Torres Fabiola', 'Alem 777', 'Ibera', 3),
		   ('Garcia Luis', 'Sucre 475', 'Santa Rosa', 5)]
conexion.executemany("insert into clientes(nombre, domicilio, ciudad, codigoprovincia) values (?,?,?,?)", valores)
conexion.commit()

print("\nMostramos las provincias:")
imprimir("select * from provincias")

print("\nMostramos los clientes:")
imprimir("select * from clientes")

print("\nHacemos un inner Join, notar que 'García Luis' no aparece, porque su codigoprovincia no existe en la tabla de provincias:")
imprimir("select c.nombre, ciudad, domicilio, p.nombre from clientes as c join provincias as p on c.codigoprovincia=p.codigo")

print("\nMostramos todos los clintes con un outer Join (tipo left join):")
print("Notar que rellena el dato faltante con null(sql, None en python)")
imprimir("select c.nombre, ciudad, domicilio, p.nombre from clientes as c left join provincias as p on c.codigoprovincia=p.codigo")

print("\nAlteramos el orden de las tablas (notar que al ser left join, 'García Luis ya no aparece')")
#puede colocarse codigoprovincia en lugar de c.codigoprovincia, porque al existir en solo una tabla no genera redudancia.
imprimir("select c.nombre, domicilio, ciudad, p.nombre from provincias as p left join clientes as c on codigoprovincia=p.codigo")

print("\nMostramos los clientes cuyo codigo de provincia no existe(es tipo null), ordenados por nombre de cliente:")
imprimir("select c.nombre, domicilio, ciudad, p.nombre from clientes as c left join provincias as p on codigoprovincia=p.codigo where p.nombre is null order by c.nombre")

print("\nAhora mostramos todos los datos de los clientes en Cordoba:")
imprimir("select c.nombre, domicilio, ciudad, p.nombre from clientes as c left join provincias as p on codigoprovincia=p.codigo where p.nombre = 'Cordoba'")

conexion.close()