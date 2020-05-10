import sqlite3 as sq
#uso de trigger update.

conexion = sq.connect("bd.db")
cur = conexion.cursor()

cur.executescript(""" 
drop table if exists libros;

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

conexion.commit()

print("\nLibros:")
imprimir("select * from libros")

print("\nActualizamos el precio del primer libro:")
cur.execute("update libros set precio=500 where codigo=1")
conexion.commit()
imprimir("select * from libros")

print("\nCreamos un trigger para congelar los precios.")
cur.execute("""
create trigger disparador_congelar_precios_libros
		before update on libros
	begin
		select
			case when new.precio<>old.precio THEN
				raise(ABORT, 'Los precios no pueden cambiarse porque estan congelados :c')
			end
		from libros where new.codigo=libros.codigo;
	end;
""")

print("\nIntentamos actualizar el precio, de nuevo:")
try:
	cur.execute("update libros set precio=1000 where codigo=1")
except sq.IntegrityError:
	print("\nLos precios no pueden cambiarse porque estan congelados :c")
	
print("\nEliminamos el trigger y volvemos a intentar actualizar:")
cur.executescript("""
drop trigger if exists disparador_congelar_precios_libros;
update libros set precio=1000 where codigo=1;
""")
imprimir("select * from libros")

conexion.close()