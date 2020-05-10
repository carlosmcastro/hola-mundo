import sqlite3 as sq
import re
#uso de check para limitar los valores permitidos en la tabla.
#se debe usar not null antes del check, para limitar valores nulos.
#la expresion regular no tiene este problema (en python al menos).

def imprimir(sql_ins):
	cursor = conexion.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)

def regexp(expresion, item):
	reg = re.compile(expresion)
	return reg.search(str(item)) is not None
	
conexion = sq.connect("bd.db")

conexion.execute("drop table if exists autos")

conexion.create_function("regexp", 2, regexp)

#La expresion regular, toma valores tales que:
#comienza con dos letras, le siguen 3 digitos, y finaliza con 2 letras.
conexion.execute("""create table autos( 
						patente text primary key check(patente regexp '^[A-Z]{2}[0-9]{3}[A-Z]{2}$'),
						marca text,
						modelo integer not null check(modelo >1900),
						precio real check(precio>0)
					)""")
							
print("\nIntentamos insertar un valor con una patente no permitida (123):")
try:							
	conexion.execute("insert into autos(patente, marca, modelo, precio) values('123', 'Fiat 128', 1970, 15000);")
except sq.IntegrityError:
	print("Patente no permitida!!!")
	
print("\nIntentamos insertar un valor con una modelo no permitido (1500):")
try:							
	conexion.execute("insert into autos(patente, marca, modelo, precio) values('AC123FG', 'Fiat 128', 1500, 15000);")
except sq.IntegrityError:
	print("Modelo no permitido!!!")	
	
print("\nInsertamos un valor de registro permitido (por la condicion not null en modelo no admite valores nulos):")
print("Si no se especifica, un valor nulo podría 'saltarse' la condición restrictiva:")
conexion.execute("insert into autos(patente, marca, modelo, precio) values('AC123FG', 'Fiat 128', 1970, 15000);")
conexion.commit()
imprimir("select * from autos")

conexion.close()