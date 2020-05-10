import sqlite3 as sq

#aplicación de insert con subconsultas.

conexion = sq.connect("bd.db")
cur = conexion.cursor()

cur.executescript(""" 
drop table if exists alumnos;
drop table if exists aprobados;

create table alumnos(
	documento text primary key,
	nombre text,
	nota real
);
create table aprobados(
	documento text primary key,
	nota real
);
""")
conexion.commit()

def imprimir(sql_ins):
	cursor = cur.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)

valores = [('30000000', 'Ana Acosta', 8),
		    ('30111111', 'Betina Bustos', 9),
		    ('30222222', 'Carlos Caseros', 2.5),
		    ('30333333', 'Daniel Duarte', 7.7),
		    ('30444444', 'Estela Esper', 3.4)]
cur.executemany("insert into alumnos values (?,?,?)", valores)
conexion.commit()
print("\nMostramos los alumnos:")
imprimir("select * from alumnos")

print("\nInsertamos en la tabla aprobados a aquellos alumnos (su documento y nota) que posean una nota igual o mayor a 4:")
cur.execute("insert into aprobados select documento, nota from alumnos where nota>=4")
conexion.commit()

imprimir("select * from aprobados")

conexion.close()