import sqlite3 as sq
#autoincremento en valores de tablas.
#Util para la asignación automatica de id.

conexion = sq.connect("bd.db")

conexion.execute("drop table if exists medicamentos;")

#Para definir el autoincremento de un valor en python.
#Se usa primay key para un valor entero que no defina el usuario.
#termina siendo un alias de rowid.
#rowid es un valor autoincrementado por defecto en el sistema.
conexion.execute("""create table medicamentos (
						codigo integer primary key,
						nombre text,
						laboratorio text,
						precio real,
						cantidad integer
					);""")
					
def imprimir(sql_ins):
	cursor = conexion.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)
		
print("\nInsertamos elementos sin declarar el codigo, para que autoincremente.")
valores = [('Sertal','Roche',5.2,100),
	       ('Buscapina','Roche',4.10,200), 
		   ('Amoxidal 500','Bayer',15.60,100)]
conexion.executemany("insert into medicamentos (nombre, laboratorio, precio, cantidad) values (?,?,?,?)", valores)
conexion.commit()

print("\nVemos como el codigo se a autoincrementado:")
imprimir("select * from medicamentos;")

print("\nSi vemos los valores de rowid, notamos que codigo, funciona como alias de rowid:")
imprimir("select rowid from medicamentos;")

print("\nSi reasignamos codigo, empieza a contar desde ese número (por ejemplo 33):")
conexion.execute("insert into medicamentos (codigo, nombre, laboratorio, precio, cantidad) values (33, 'uh', '33', 2.3, 213)")
conexion.executemany("insert into medicamentos (nombre, laboratorio, precio, cantidad) values (?,?,?,?)", valores)
conexion.commit()
imprimir("select * from medicamentos;")

print("\nrowid sigue siendo el valor autoincrementado originalmente: ")
imprimir("select rowid from medicamentos;")

conexion.close()