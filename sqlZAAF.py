import sqlite3 as sq

#uso de subconsultas.
#select anidado que devuelve un dato.

conexion = sq.connect("bd.db")
cur = conexion.cursor()

cur.executescript(""" 
drop table if exists alumnos;

create table alumnos(
	documento text primary key,
	nombre text,
	nota real
);
""")
conexion.commit()

def imprimir(sql_ins):
	cursor = cur.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)

valores = [('30111111', 'Ana Algarbe', 5.1),
		    ('30222222', 'Bernardo Bustamante', 3.2),
		    ('30333333', 'Carolina Conte', 4.5),
		    ('30444444', 'Diana Dominguez', 9.7),
		    ('30555555', 'Fabian Fuentes', 8.5),
		    ('30666666', 'Gaston Gonzalez', 9.7)]
cur.executemany("insert into alumnos(documento, nombre,nota) values (?,?,?)", valores)

conexion.commit()

print("\nAlumnos:")
imprimir("select * from alumnos")

print("\nAlumnos con la nota más alta:")
imprimir("select alumnos.* from alumnos where nota = (select max(nota) from alumnos)")

print("\nAlumnos y la diferencia con el promedio, donde la nota es menor al promedio:")
imprimir("select alumnos.*, (select avg(nota) from alumnos)-nota as diferencia from alumnos where nota < (select avg(nota) from alumnos)")

print("\nEliminamos las notas menores al promedio:")
cur.execute("delete from alumnos where nota < (select avg(nota) from alumnos)")
imprimir("select * from alumnos")

conexion.close()