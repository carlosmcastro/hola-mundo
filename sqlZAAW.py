import sqlite3 as sq
#manejo de fechas.
#al ingresar fechas es importante respetar el formato:
# ISO 8601.
#eso te permite ordenar y agrupar fechas.

conexion = sq.connect("bd.db")
cur = conexion.cursor()

cur.executescript(""" 
drop table if exists empleados;
drop table if exists asistencia;

create table empleados(
	legajo integer primary key,
	nombre	text,
	fecha_ingreso text
);
create table asistencia(
	dni text,
	fecha_hora text,
	primary key(dni, fecha_hora)
);
""")
conexion.commit()

def imprimir(sql_ins):
	cursor = cur.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)

valores = [('Rodriguez Pablo', '2000-01-01'),
		    ('Martinez Ana', '1978-12-23'),
		    ('Lopez Oscar', '2017-08-29')]
cur.executemany("insert into empleados(nombre, fecha_ingreso) values (?,?)", valores)
valores = [('11111111', '2018-09-14 08:00:00'),
		    ('22222222', '2018-09-14 06:12:00'),
		    ('33333333', '2018-09-14 18:05:00'),
		    ('11111111', '2018-09-15 08:02:00'),
		    ('22222222', '2018-09-15 06:00:00'),
		    ('33333333', '2018-09-15 14:00:00')]
cur.executemany("insert into asistencia values (?,?)", valores)

conexion.commit()

print("\nVemos la tabla de empleados ordenada por fecha.")
print("\nAscendente:")
imprimir("select * from empleados order by fecha_ingreso")
print("\nDescendente:")
imprimir("select * from empleados order by fecha_ingreso desc")

print("\nPodemos hacer esto gracias al formato ISO 8601.")

print("\nVemos la tabla de asistencia ordenada por fecha y hora (ascendente):")
imprimir("select * from asistencia order by fecha_hora")
print("\nMostramos solo la fecha, sin la hora:")

#date() y time(), aprovecha le formato de fecha para obtener la fecha y hora.
imprimir("select dni, date(fecha_hora) from asistencia")
print("\nMostramos solo la hora, sin la fecha:")
imprimir("select dni, time(fecha_hora) from asistencia")

print("\nAsistencia ingreso entre 00:00:00 y las 12:00:00 :")
imprimir("select * from asistencia where time(fecha_hora)>='00:00:00' and time(fecha_hora)<='12:00:00'")
print("\nLo mismo pero con between:")
imprimir("select * from asistencia where time(fecha_hora) between '00:00:00' and '12:00:00'")
print("\nLo mismo, pero ordenados los horarios de menor a mayor:")
imprimir("select * from asistencia where time(fecha_hora) between '00:00:00' and '12:00:00' order by time(fecha_hora)")

#usamos date y datetime para almacenar datos de tiempo propios del sistema.
print("\nAlmacenamos en empleados la fecha actual:")
cur.execute("insert into empleados(nombre, fecha_ingreso) values ('Berrotaran Mariuz', date('now'))")
imprimir("select * from empleados")

print("\nInsertamos en asistencia la fecha actual con la hora.")
cur.execute("insert into asistencia values('11111111', datetime('now','localtime'))")
imprimir("select * from asistencia")

print("\nInsertamos la fecha actual, con horario UTC en asistencia:")
cur.execute("insert into asistencia values('11111111', datetime('now'))")
imprimir("select * from asistencia")

conexion.close()