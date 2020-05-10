import sqlite3 as sq
#uso de procesos de seleccion anidados.
#como tablas derivadas, para usar en otras tablas.
#Uno de los usos más complejos de subconsultas.


conexion = sq.connect("bd.db")
cur = conexion.cursor()

cur.executescript(""" 
drop table if exists clientes;
drop table if exists facturas;
drop table if exists detalles;

create table clientes(
	codigo integer primary key,
	nombre text,
	domicilio text
);
create table facturas(
	numero integer primary key,
	codigocliente integer
);
create table detalles(
	numerofactura integer,
	numeroitem integer,
	articulo text,
	precio real,
	cantidad integer,
	primary key(numerofactura, numeroitem)
);
""")
conexion.commit()

def imprimir(sql_ins):
	cursor = cur.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)

valores = [('Juan Lopez', 'Colon 123'),
		    ('Luis Torres', 'Sucre 987'),
		    ('Ana Garcia', 'Sarmiento 576')]
cur.executemany("insert into clientes(nombre, domicilio) values (?,?)", valores)
valores = [(1200, 1),
		    (1201, 2),
		    (1202, 3),
		    (1300, 1)]
cur.executemany("insert into facturas values (?,?)", valores)
valores = [(1200, 1, 'lapiz', 1, 100),
		    (1200, 2, 'goma', 0.5, 150),
		    (1201, 1, 'regla', 1.5, 80),
		    (1201, 2, 'goma', 0.5, 200),
		    (1201, 3, 'cuaderno', 4, 90),
		    (1202, 1, 'lapiz', 1, 200),
		    (1202, 2, 'escuadra', 2, 100),
		    (1300, 1, 'lapiz', 1, 300)]
cur.executemany("insert into detalles values (?,?,?,?,?)", valores)

conexion.commit()

print("\nClientes:")
imprimir("select * from clientes")
print("\nFacturas:")
imprimir("select * from facturas")
print("\nDetalles:")
imprimir("select * from detalles")

print("\nFacturas y la suma total a partir de los detalles:")
imprimir("""select f.*, (select sum(cantidad*d.precio) from detalles as d 
			where f.numero=d.numerofactura) as total from facturas as f""")

print("\nUsaremos el resultado previo como tabla derivada.")

print("\nNúmero de factura, nombre de cliente, y monto total (el primer y tercer dato son propios de la tabla derivada):")
imprimir("""select td.numero, c.nombre, td.total from clientes as c join 
			(select f.*, (select sum(cantidad*d.precio) from detalles as d
			where f.numero=d.numerofactura) as total from facturas as f) as td
			where td.codigocliente = c.codigo""")

conexion.close()