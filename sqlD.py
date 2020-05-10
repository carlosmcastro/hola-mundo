import sqlite3 as sq
#manejo de datos tipo null.
#recordar que null es un dato nulo, más no vacio.
#uso de is null y de is not null

conexion = sq.connect("bd.db")

conexion.execute("drop table if exists libros;")

def imprimir(sql_ins):
	cursor = conexion.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)

#para evitar que titulo y autor admitan valores nulos.
conexion.execute("""create table libros(
					titulo text not null,
					autor text not null,
					editorial text null,
					precio real
					);""")

#sqlite convierte el valor None a null y viceversa.
valores = [("El aleph", "Borges", "Emece", None),
		   ("Alicia en el Pais de las maravillas", "Lewis Carrol", None, 25)]

print("Insertamos valores nulos a la tabla: ")
conexion.executemany("insert into libros (titulo, autor, editorial, precio) values (?,?,?,?);", valores)
conexion.commit()

imprimir("select * from libros;")

try:
	conexion.execute("insert into libros (titulo, autor, editorial, precio) values (null, 'Borges', 'Siglo XXI', 25.6);")			
except sq.IntegrityError:
	print("\nEl titulo no puede ser nulo.")
					
print("\nPara extraer registros nulos no usamos los operadores relacionaes vistos previamente.")
print("Usamnos 'is'")
print("\nVeamos los datos con precios que sean tipo null:")
imprimir("select * from libros where precio is null;")

print("\nVeamos los datos con precios que no sean null:")
imprimir("select * from libros where precio is not null")

print("\nRecordar que los datos de tipo null, son disitintos de 0 o '' ")

conexion.close()