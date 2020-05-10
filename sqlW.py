import sqlite3 as sq
#combinacion cruzada (cross combination)
#es una variacion de n x m

conexion = sq.connect("bd.db")

def imprimir(sql_ins):
	cursor = conexion.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)
		
valores = [('comidas',),('postres',),('hombres',),('mujeres',)]
#por alguna razón executemany no funciona con drop
[conexion.execute("drop table if exists "+i[0]) for i in valores]


conexion.execute("""create table comidas(
						codigo integer primary key,
						nombre text,
						precio real
				)""")
conexion.execute("""create table postres(
						codigo integer primary key,
						nombre text,
						precio real
				)""")
conexion.execute("""create table hombres(
						documento text primary key,
						nombre text,
						domicilio text,
						edad integer
				)""")
conexion.execute("""create table mujeres(
						documento text primary key,
						nombre text,
						domicilio text,
						edad integer
				)""")

valores = [('milanesa y fritas',3.4), ('arroz primavera',2.5), ('pollo',2.8)]
conexion.executemany("insert into comidas (nombre, precio) values (?,?)", valores)
valores = [('flan',1), ('porcion de torta',2.1), ('gelatina',0.9)]
conexion.executemany("insert into postres (nombre, precio) values (?,?)", valores)

valores = [('1', 'Juan Torres', 'Sarmiento 755', 44),
		   ('2', 'Marcelo Oliva', 'San Martin 874', 56),
		   ('3', 'Federico Pereyra', 'Colon 234', 38),
		   ('4', 'Juan Garcia', 'Peru 333', 50)]
conexion.executemany("insert into hombres (documento, nombre, domicilio, edad) values (?,?,?,?)", valores)
valores = [('5', 'Maria Lopez', 'Colon 123', 45),
		   ('6', 'Liliana Garcia', 'Sucre 456', 35),
		   ('7', 'Susana Lopez', 'Avellaneda 98', 41)]
conexion.executemany("insert into mujeres (documento, nombre, domicilio, edad) values (?,?,?,?)", valores)
				
print("\nHacemos la combinacion cruzada de dos tablas:")

print("\nComidas:")
imprimir("select * from comidas")				
print("\nPostres:")
imprimir("select * from postres")

print("\nAl combinarlos (con una columna adicional que suma los preios):")
print("(Esta combinación puede verse como un producto cartesiano)")
imprimir("select c.nombre, p.nombre, c.precio+p.precio as total from comidas as c cross join postres as p")

print("\nREPETIMOS EL PROCESO CON OTRAS DOS TABLAS:")

print("\nHombres:")
imprimir("select * from hombres")				
print("\nMujeres:")
imprimir("select * from mujeres")

print("\nCombinamos las tablas en forma cruzada:")
imprimir("select h.nombre, h.edad, m.nombre, m.edad from hombres as h cross join mujeres as m")

print("\nAhora solo consideramos en la combinacion cruzada a las personas mayores de 40 años:")
imprimir("select h.nombre, h.edad, m.nombre, m.edad from hombres as h cross join mujeres as m where h.edad > 40 and m.edad >40")

print("\nPor ultimo formamos parejas, mientras no tengan una diferencia mayor de 10 años")
imprimir("select h.nombre, h.edad, m.nombre, m.edad from hombres as h cross join mujeres as m where h.edad-m.edad between -10 and 10")

conexion.close()