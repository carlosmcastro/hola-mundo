import sqlite3 as sq
#Uso de vistas.
#una especie de tablas virtuales.
#En ellas se inserta una consulta.
#Que puede consultarse como una tabla normal.
#Más no insertar, actualizar o eliminar elementos.
#Ya que depende de otras tablas.
#Si la o las tablas a la que esta asociada cambian.
#La vista tambien se ve alterada.

#Es util para obtener datos concretos y para consultas repetitivas.


conexion = sq.connect("bd.db")
cur = conexion.cursor()

cur.executescript(""" 
drop table if exists secciones;
drop table if exists empleados;

create table secciones(
	codigo integer primary key,
	nombre text,
	sueldo real
);
create table empleados(
	legajo integer primary key,
	documento text,
	sexo text,
	apellido text,
	nombre text,
	domicilio text,
	seccion integer,
	cantidadhijos integer,
	estadocivil text
);

""")
conexion.commit()

def imprimir(sql_ins):
	cursor = cur.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)

valores = [('Administracion', 300),
		    ('Contaduría', 400),
		    ('Sistemas', 500)]
cur.executemany("insert into secciones(nombre, sueldo) values (?,?)", valores)
valores = [('22222222', 'f', 'Lopez', 'Ana', 'Colon 123', 1, 2, 'casado'),
		    ('23333333', 'm', 'Lopez', 'Luis', 'Sucre 235', 1, 0, 'soltero'),
		    ('24444444', 'm', 'Garcia', 'Marcos', 'Sarmiento 1234', 2, 3, 'divorciado'),
		    ('25555555', 'm', 'Gomez', 'Pablo', 'Bulnes 321', 3, 2, 'casado'),
		    ('26666666', 'f', 'Perez', 'Laura', 'Peru 1254', 3, 3, 'casado')]
cur.executemany("insert into empleados(documento, sexo, apellido, nombre, domicilio, seccion, cantidadhijos, estadocivil) values (?,?,?,?,?,?,?,?)", valores)

conexion.commit()

print("\nSecciones:")
imprimir("select * from secciones")
print("\nEmpleados")
imprimir("select * from empleados")

print("\nEliminamos la vista previa si ya existe:")
cur.execute("drop view if exists vista_empleados")

print("\nCreamos y visualizamos la vista_empleados:")
cur.execute("""
create view vista_empleados as
	select (apellido||' '||e.nombre) as nombre, sexo,
		s.nombre as seccion, cantidadhijos
		from empleados as e
		join secciones as s
		on codigo=seccion;
""")
imprimir("select * from vista_empleados")

print("\nConsultamos la vista como una tabla:")
print("[Cantidad de personas por seccion]")
imprimir("select seccion, count(*) as cantidad from vista_empleados group by seccion")

print("\nInsertamos un empleado en la tabla 'empleados'")
cur.execute("insert into empleados(documento,sexo,apellido,nombre,domicilio,seccion,cantidadhijos,estadocivil) values('27777777','f','Rodriguez','Pablo','Colon 33',3,3,'casado'); ")
imprimir("select * from empleados")

print("\nVisualizamos otra vez la vista (notando que el empleado añadido en la tabla tambien aparece en la vista asociada)")
imprimir("select * from vista_empleados")

conexion.close()