import sqlite3 as sq
#suboconsultas correlacionadas.
#subconsultas entre tablas, con datos correlacionados.
#Muy util!!


conexion = sq.connect("bd.db")
cur = conexion.cursor()

cur.executescript(""" 
drop table if exists facturas;
drop table if exists detalles;

create table facturas(
	numero integer primary key,
	cliente text
);
create table detalles(
	numerofactura integer not null,
	numeroitem integer not null,
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

valores = [(1200, 'Juan Lopez'),
		    (1201, 'Luis Torres'),
		    (1202, 'Ana Garcia'),
		    (1300, 'Juan Lopez')]
cur.executemany("insert into facturas(numero, cliente) values (?,?)", valores)
valores = [(1200, 1, 'lapiz', 1, 100),
		    (1200, 2, 'goma', 0.5, 150),
		    (1201, 1, 'regla', 1.5, 80),
		    (1201, 2, 'goma', 0.5, 200),
		    (1201, 3, 'cuaderno', 4, 90),
		    (1202, 1, 'lapiz', 1, 200),
		    (1202, 2, 'escuadra', 2, 100),
		    (1300, 1, 'lapiz', 1, 300)]
cur.executemany("insert into detalles(numerofactura, numeroitem, articulo, precio, cantidad) values (?,?,?,?,?)", valores)

conexion.commit()

print("\nFacturas:")
imprimir("select * from facturas")
print("\nDetalles:")
imprimir("select * from detalles")

print("\nSeleccionamos las facturas con numero y cliente. Junto a la cantidad de productos comprados y el costo gastado:")
#f.* es equivalente a *, pero sirve f.* para tomar en cuenta de donde provienen los datos.
imprimir("""select f.*, (select count(d.numerofactura) from detalles 
			as d where f.numero=d.numerofactura) as cantidad, 
			(select sum(precio) from detalles as d where f.numero = d.numerofactura) as total
			from facturas as f""")
#si dentro de sum se realiza precio*cantidad, va a tomar la cantidad definida en detalles.
#y puede anidarse el primer select en el segundo si se desea.

conexion.close()