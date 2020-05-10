import sqlite3 as sq

conexion = sq.connect("bd.db")

#executescript permite ejecutar un script entero en python de SQL.
#así que aquí si importan los ;
conexion.executescript("""drop table if exists comidas;
						  create table comidas (
								codigo integer primary key,
								nombre text,
								precio ral,
								rubro text
						  )""")

def imprimir(sql_ins):
	cursor = conexion.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)
		
valores = [('ravioles', 5, 'plato'),
		   ('tallarines', 4, 'plato'),
		   ('milanesa', 7, 'plato'),
		   ('cuarto de pollo', 6, 'plato'),
		   ('flan', 2.5, 'postre'),
		   ('porcion torta', 3.5, 'postre')]
conexion.executemany("insert into comidas (nombre, precio, rubro) values (?,?,?)", valores)
conexion.commit()

print("\nEsta es la tabla de la que disponemos:")
imprimir("select * from comidas")

print("\nHacemos una autocombinacion con cross join:")
imprimir("select c1.nombre, c2.nombre, c1.precio+c2.precio as total from comidas as c1 cross join comidas as c2")

print("\nHacemos lo mismo que antes, pero solo permitimos que se de entre platos y postres:")
imprimir("select c1.nombre, c2.nombre, c1.precio+c2.precio as total from comidas as c1 cross join comidas as c2 where c1.rubro='plato' and c2.rubro='postre'")

print("\nTambien se puede hacer esto con join (join inner):")
#la seccion: on c1.codigo <> c2.codigo es excesiva para este caso, pero en otros puede ser util.
#omitiendola para este caso, genera el mismo resultado.
imprimir("select c1.nombre, c2.nombre, c1.precio+c2.precio as total from comidas as c1 join comidas as c2 on c1.codigo <> c2.codigo where c1.rubro='plato' and c2.rubro='postre'")

conexion.close()