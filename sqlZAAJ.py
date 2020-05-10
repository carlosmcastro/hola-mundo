import sqlite3 as sq

conexion = sq.connect("bd.db")
cur = conexion.cursor()

cur.executescript(""" 
drop table if exists socios;
drop table if exists inscriptos;

create table socios(
	numero integer primary key,
	documento text,
	nombre text,
	domicilio text
);
create table inscriptos(
	numerosocio integer not null,
	deporte text not null,
	cuotas integer,
	primary key(numerosocio, deporte)
);
""")
conexion.commit()

def imprimir(sql_ins):
	cursor = cur.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)

valores = [('23333333', 'Alberto Paredes', 'Colon 111'),
		    ('24444444', 'Carlos Conte', 'Sarmiento 755'),
		    ('25555555', 'Fabian Fuentes', 'Caseros 987'),
		    ('26666666', 'Hector Lopez', 'Sucre 344')]
cur.executemany("insert into socios(documento, nombre, domicilio) values (?,?,?)", valores)
valores = [(1, 'tenis', 1),
		    (1, 'basquet', 2),
		    (1, 'natacion', 1),
		    (2, 'tenis', 9),
		    (2, 'natacion', 1),
		    (2, 'basquet', 0),
		    (2, 'futbol', 2),
		    (3, 'tenis', 8),
		    (3, 'basquet', 9),
		    (3, 'natacion', 0),
		    (4, 'basquet', 10)]
#esto es nuevo: Si los valores son tal cual en total ingresados, puede oviarse el parametro despues de la tabla.
cur.executemany("insert into inscriptos values (?,?,?)", valores)

conexion.commit()

print("\nSocios:")
imprimir("select * from socios")

print("\nInscriptos:")
imprimir("select * from inscriptos")

print("\nNombre de socio, domicilio, y cantidad de deportes a los que esta inscripto:")
imprimir("select nombre, domicilio, (select count(*) from inscriptos as i where i.numerosocio=s.numero) as deportes from socios as s")

print("\nNombre de los socios, cuotas a pagar(10 por deporte), y pagos realizados:")
imprimir("""select nombre, (select (count(*)*10) from inscriptos as i 
			where i.numerosocio=s.numero) as total, (select sum(i.cuotas) 
			from inscriptos as i where i.numerosocio=s.numero) as pagas from socios as s""")

print("\nLo mismo que antes con Join:")
imprimir("""select nombre, count(deporte)*10 as total, sum(cuotas) as pagas from inscriptos 
			as i join socios as s on numerosocio=numero group by nombre""")
#es importante el uso de group by en esta ultima sentencia.

conexion.close()