import sqlite3 as sq
#uso de delete en trigger.

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

#conexion.commit()

cur.executescript(""" 
drop trigger if exists disparador_ventas_borrar;
drop trigger if exists disparador_devolucion_libro;

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
	create trigger disparador_devolucion_libro
			before delete on ventas
		begin
			update libros set stock = libros.stock + old.cantidad
				where old.codigolibro=libros.codigo;
		end;
""")


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

print("\nEliminamos la venta:")
cur.execute("delete from ventas where numero=1")
conexion.commit()
ver_tablas()

print("\nNotese que el stock a aumentado.")

conexion.close()