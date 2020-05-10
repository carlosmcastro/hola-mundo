import sqlite3 as sq
#manejo de errores con trigger raise en SQL.
#como generar errores.

conexion = sq.connect("bd.db")
cur = conexion.cursor()

cur.executescript(""" 
drop table if exists ventas;
drop table if exists libros;

create table ventas(
	numero integer primary key,
	codigolibro integer,
	precio real,
	cantidad integer
);
create table libros(
	codigo integer primary key,
	titulo text,
	autor text,
	editorial text,
	precio real,
	stock integer
);
""")
conexion.commit()

def imprimir(sql_ins):
	cursor = cur.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)

valores = [('Uno', 'Richard Bach', 'Planeta', 15, 100),
		    ('Ilusiones', 'Richard Bach', 'Planeta', 18, 50),
		    ('El aleph', 'Borges', 'Emece', 25, 200),
		    ('Aprenda PHP', 'Mario Molina', 'Emece', 45, 200)]
cur.executemany("insert into libros(titulo, autor, editorial, precio, stock) values (?,?,?,?,?)", valores)

#borramos el disparador si existe.
cur.execute("drop trigger if exists disparador_ventas_borrar")

#creamos el disparador
cur.execute(""" 
	create trigger disparador_ventas_borrar
			before insert on ventas
		begin
			select
				case when new.cantidad>libros.stock THEN
					raise (ABORT, 'No hay stock (reservas) suficiente de ese libro')
				end
			from libros where new.codigolibro=libros.codigo;
			update libros set stock=libros.stock-new.cantidad
				where new.codigolibro=libros.codigo;
		end;
""")
conexion.commit()

def ver_tablas():
	print("\nLibros:")
	imprimir("select * from libros")
	print("\nVentas:")
	imprimir("select * from ventas")

ver_tablas()

print("\nInsertamos un valor en ventas:")
cur.execute("insert into ventas(codigolibro, precio, cantidad) values (1, 15, 1)")
conexion.commit()
ver_tablas()

print("\nNotese que el stock (reservas) de dicho libro a disminuido.")

print("\nSobrepasemos las reservas(stock) para desencadenar el trigger raise:")
print("[Se va a ejecutar un error]")
cur.execute("insert into ventas(codigolibro, precio, cantidad) values (1, 15, 100)")

conexion.close()