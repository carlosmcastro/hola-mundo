import sqlite3 as sq
#uso de group by para agrupar tipos al ejecutar funciones.
#uso de having para filtrar (similar a where), pero permite filtrar con funciones, como count() ó avg().
#uso de distinct para mostrar solo valores sin duplicar.

conexion = sq.connect("bd.db")

conexion.execute("drop table if exists clientes")

conexion.execute("""create table clientes (
					codigo integer primary key,
					nombre text,
					domicilio text,
					ciudad text,
					provincia text,
					telefono text
				)""")

def imprimir(sql_ins):
	cursor = conexion.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)
		
valores = [('Lopez Marcos', 'Colon 111', 'Cordoba', 'Cordoba', None), 
		   ('Perez Ana', 'San Martin 222', 'Cruz del Eje', 'Cordoba', '4578585'), 
		   ('Garcia Juan', 'Rivadavia 333', 'Villa Maria', 'Cordoba', '4578445'), 
		   ('Perez Luis', 'Sarmiento 444', 'Rosario', 'Santa Fe', None), 
		   ('Pereyra Lucas', 'San Martin 555', 'Cruz del Eje', 'Cordoba', '4253685'), 
		   ('Gomez Ines', 'San Martin 666', 'Santa Fe', 'Santa Fe', '0345252525'), 
		   ('Torres Fabiola', 'Alem 777', 'Villa del Rosario', 'Cordoba', '4554455'), 
		   ('Lopez Carlos', 'Irigoyen 888', 'Cruz del Eje', 'Cordoba', None), 
		   ('Ramos Betina', 'San Martin 999', 'Cordoba', 'Cordoba', '4223366'), 
		   ('Lopez Lucas', 'San Martin 1010', 'Posadas', 'Misiones', '0457858745')]
conexion.executemany("insert into clientes (nombre, domicilio, ciudad, provincia, telefono) values (?,?,?,?,?)", valores)
conexion.commit()

print("\nMostramos los registros de clientes:")
imprimir("select * from clientes")

print("\nMostramos la cantidad de registros de clientes:")
imprimir("select count(*) from clientes")

print("\nMostramos la cantidad de registros de clientes por cada ciudad (realiza un doble agrupamiento de ciudad, provincia):")
imprimir("select ciudad, provincia, count(*) from clientes group by ciudad, provincia order by provincia")
		   
print("\nEsto tambien puede hacerse con sum(), max y avg(), etc")

print("\nUSO DE HAVING:")

print("\nObtenemos ciudad y provincia, sin considerar las que tienen menos de dos clientes:")
imprimir("select ciudad, provincia, count(*) as cantidad from clientes group by ciudad, provincia having count(*)>1")

print("\nPodemos omitir el count(*) con having:")
imprimir("select ciudad, provincia from clientes group by ciudad, provincia having count(*)>1")


print("\nUSO DE DISTINCT:")

print("\nMostramos las provincias sin repetir:")
imprimir("select distinct provincia from clientes")

print("\nContamos las distintas provincias:")
imprimir("select count(distinct provincia) as cantidad from clientes")

print("\nMostramos las ciudades sin repetir:")
imprimir("select distinct ciudad from clientes")

print("\nContamos las distintas provincias:")
imprimir("select count(distinct ciudad) from clientes")

print("\nObtenemos las distintas ciudades de la provincia de Cordoba:")
imprimir("select distinct ciudad from clientes where provincia = 'Cordoba'")

print("\nContamos las distintas ciudades de cada provincia:")
imprimir("select provincia, count(distinct ciudad) from clientes group by provincia")

conexion.close()




















