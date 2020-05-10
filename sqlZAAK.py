import sqlite3 as sq
#uso de exists y not exists en subconsultas.
#exists no devuelve valores más halla de valores booleanos.
#existe o no existe.

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

print("\nFacturas:")
imprimir("select * from facturas")
print("\nDetalles:")
imprimir("select * from detalles")

print("\nLista de clientes que compraron al menos un lapiz:")
imprimir("""select cliente, numero from facturas as f where exists 
			(select * from detalles as d where d.numerofactura=f.numero and d.articulo='lapiz')""")
			
print("\nLista de clientes que no compraron siquiera un lapiz:")
imprimir("""select cliente, numero from facturas as f where not exists 
			(select * from detalles as d where d.numerofactura=f.numero and d.articulo='lapiz')""")
			
conexion.close()