import sqlite3 as sq
#uso de primary key, valores no nulos y unicos.

conexion = sq.connect("bd.db")

conexion.execute("drop table if exists usuarios;")

conexion.execute("""
					create table usuarios (
						nombre text not null,
						clave text,
						primary key(nombre)
					);
					""")
def imprimir(sql_ins):
	cursor = conexion.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)
		
print("\nInsertamos dos datos a la tabla:")
valores = [("Gonzales", "Patatas"), ("Jimenez", "Papayas")]
conexion.executemany("insert into usuarios (nombre, clave) values (?,?);", valores)
conexion.commit()
imprimir("select * from usuarios;")

print("\nIntentamos insertar un valor repetido (Gonzales) en nombre:")
try:
	conexion.execute("insert into usuarios (nombre, clave) values ('Gonzales', 'Frutas');")
except sq.IntegrityError:
	print("\n\tNo se puede insertar dos valores iguales tipo primary key (clave primaria)")

print("\nIntentamos actualizar un valor con un nombre existente:")
try:	
	conexion.execute("update usuarios set nombre = 'Jimenez' where clave = 'Patatas';")
except sq.IntegrityError:
	print("\n\tNo se puede insertar dos valores iguales tipo primary key (clave primaria)")

conexion.close()