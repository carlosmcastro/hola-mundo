import sqlite3 as sq
#clave primaria compuesta.
#claves primarias para varios valores.
#basicamente, no se repite el mismo año, con el mismo documento, ni con el mismo deporte, al tiempo.


conexion = sq.connect("bd.db")

conexion.execute("drop table if exists inscriptos")

conexion.execute("""create table inscriptos (
						documento text,
						deporte text,
						año text,
						nombre text,
						matricula text,
						primary key(documento, deporte, año)						
					) """)

def imprimir(sql_ins):
	cursor = conexion.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)

print("\nInscribimos varios alumnos en el mismo deporte en el mismo año (distinto documento):")
valores = [('12222222', 'Juan Perez', 'tenis', 2005, 's'), 
		   ('23333333', 'Marta Garcia', 'tenis', 2005, 's'), 
		   ('34444444', 'Luis Perez', 'tenis', 2005, 'n')]
conexion.executemany("insert into inscriptos (documento, nombre, deporte, año, matricula) values (?,?,?,?,?)", valores)
conexion.commit()
imprimir("select * from inscriptos")

print("\nInscribimos a un mismo alumno a varios deportes un mismo año:")
valores = [('12222222', 'Juan Perez', 'futbol', '2005', 's'), 
		   ('12222222', 'Juan Perez', 'natacion', '2005', 's'), 
		   ('12222222', 'Juan Perez', 'basquet', '2005', 'n')]
conexion.executemany("insert into inscriptos (documento, nombre, deporte, año, matricula) values (?,?,?,?,?)", valores)
conexion.commit()
imprimir("select * from inscriptos")

print("\nInscribimos un socio, con el mismo documento, en el mismo deporte, en distintos años:")
valores = [('12222222', 'Juan Perez', 'tenis', 2006, 's'), 
		   ('12222222', 'Juan Perez', 'tenis', 2007, 's')]
conexion.executemany("insert into inscriptos (documento, nombre, deporte, año, matricula) values (?,?,?,?,?)", valores)
conexion.commit()
imprimir("select * from inscriptos")

print("\nIntentamos ingresar un dato con documento, deporte y año, ya registrado:")
valor = ('12222222','Juan Perez','tenis',2005,'s')
try:
	conexion.execute("insert into inscriptos (documento, nombre, deporte, año, matricula) values (?,?,?,?,?)", valor)
except sq.IntegrityError:
	print("No se puede insertar un valor con documento, deporte y año repetido.")

print("\nIntentamos actualizar para que un dato quede repetido:")
try:
	conexion.execute("update inscriptos set deporte = 'tenis' where documento = '12222222' and deporte = 'futbol' and año = 2005")
except sq.IntegrityError:
	print("No se puede actualizar un valor con documento, deporte y año repetido.")

conexion.close()
















