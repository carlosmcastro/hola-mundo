import sqlite3 as sq

#union para unir resultados de dos select.

conexion = sq.connect("bd.db")
cur = conexion.cursor()

cur.executescript("""
drop table if exists alumnos;
drop table if exists profesores;

create table alumnos (
	documento text primary key,
	nombre text,
	domicilio text
);

create table profesores (
	documento text primary key,
	nombre text,
	domicilio text	
);
""")
conexion.commit()

def imprimir(sql_ins):
	cursor = cur.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)

valores = [('30000000', 'Juan Perez', 'Colon 123'),
		    ('30111111', 'Marta Morales', 'Caseros 222'),
		    ('30222222', 'Laura Torres', 'San Martin 987'),
		    ('30333333', 'Mariano Juarez', 'Avellaneda 34'),
		    ('23333333', 'Federico Lopez', 'Colon 987')]
cur.executemany("insert into alumnos(documento, nombre, domicilio) values (?,?,?)", valores)

valores = [('22222222', 'Susana Molina', 'Sucre 345'),
		    ('23333333', 'Federico Lopez', 'Colon 987')]
cur.executemany("insert into profesores(documento, nombre, domicilio) values (?,?,?)", valores)
conexion.commit()

print("\nAlumnos:")
imprimir("select * from alumnos")

print("\nProfesores:")
imprimir("select * from profesores")

print("\nNombre y domicilio de alumnos y profesores (aparece con orden ascendente, por nombre):")
imprimir("select nombre, domicilio from alumnos union select nombre, domicilio from profesores")

print("\nLo mismo incluyendo duplicados:")
imprimir("select nombre, domicilio from alumnos union all select nombre, domicilio from profesores")

print("\nOrdenamos por domicilio:")
imprimir("select nombre, domicilio from alumnos union select nombre, domicilio from profesores order by domicilio")

print("\nAñadimos la condición para diferenciar alumnos de profesores:")
imprimir("select nombre, domicilio, 'alumnos' from alumnos union select nombre, domicilio, 'profesores' from profesores")

print("\nLo mismo que antes pero ordenados por tipo(condicion):")
imprimir("""select nombre, domicilio, 'alumnos' as condicion from alumnos union 
select nombre, domicilio, 'profesores' as condicion from profesores order by condicion""")

conexion.close()






















