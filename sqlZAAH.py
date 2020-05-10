import sqlite3 as sq
#Uso de subconsultas con multiples tablas.
#Cuando devuelve varios valores.
#Parte 2

conexion = sq.connect("bd.db")
cur = conexion.cursor()

cur.executescript(""" 
drop table if exists ciudades;
drop table if exists clientes;

create table ciudades(
	codigo integer primary key,
	nombre text
);
create table clientes(
	codigo integer primary key,
	nombre text,
	domicilio text,
	codigociudad integer
);
""")
conexion.commit()

def imprimir(sql_ins):
	cursor = cur.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)

valores = [('Cordoba',),
		    ('Cruz del Eje',),
		    ('Carlos Paz',),
		    ('La Falda',),
		    ('Villa Maria',)]
cur.executemany("insert into ciudades(nombre) values (?)", valores)
valores = [('Lopez Marcos', 'Colon 111', 1),
		    ('Lopez Hector', 'San Martin 222', 1),
		    ('Perez Ana', 'San Martin 333', 2),
		    ('Garcia Juan', 'Rivadavia 444', 3),
		    ('Perez Luis', 'Sarmiento 555', 3),
		    ('Gomez Ines', 'San Martin 666', 4),
		    ('Torres Fabiola', 'Alem 777', 5),
		    ('Garcia Luis', 'Sucre 888', 5)]
cur.executemany("insert into clientes(nombre, domicilio, codigociudad) values (?,?,?)", valores)

conexion.commit()

print("\nCiudades:")
imprimir("select * from ciudades")
print("\nClientes:")
imprimir("select * from clientes")

print("\nMostramos las ciudades donde los clientes son de la calle San Martin:")
imprimir("select nombre from ciudades where codigo in (select codigociudad from clientes where domicilio like 'San Martin %')")

print("\nLo mismo con uso de join y distinct:")
imprimir("select distinct ci.nombre from ciudades as ci join clientes as cl on codigociudad=ci.codigo where domicilio like 'San Martin %'")

print("\nMostramos las ciudades donde los clientes no empiezan por P:")
imprimir("select nombre from ciudades where codigo not in (select codigociudad from clientes where nombre like 'P%')")

print("\nMostramos los codigo ciudad de aquellos clientes que comienzan con P:")
imprimir("select codigociudad from clientes where nombre like 'P%'")

conexion.close()