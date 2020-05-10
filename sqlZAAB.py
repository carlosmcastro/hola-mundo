import sqlite3 as sq
#uso de foreign key,
#con la propia tabla

#con conexion.execute("PRAGMA foreign_keys=on")
#el script funciona como corresponde.

conexion = sq.connect("bd.db")

cur = conexion.cursor()

cur.executescript("""
drop table if exists afiliados;

create table afiliados(
	numero integer primary key,
	documento text,
	nombre text,
	afiliadotitular integer references afiliados(numero)
)
""")

def imprimir(sql_ins):
	cursor = cur.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)

valores = [('22222222', 'Perez Juan', None),
		    ('23333333', 'Garcia Maria', None),
		    ('24444444', 'Lopez Susana', None),
		    ('30000000', 'Perez Marcela', 1),
		    ('31111111', 'Morales Luis', 1),
		    ('32222222', 'Garcia Maria', 2)]
cur.executemany("insert into afiliados(documento, nombre, afiliadotitular) values (?,?,?)", valores)
conexion.commit()

print("\nEsta es la tabla de afiliados: ")
imprimir("select * from afiliados")

print("\nNotese que cada afiliado respeta la regla de estar asociado a el numero.")
print("De autoincremento en afiliados, si hay siete afiliados admite afiliarse a 7 valores, no a más.")

print("\nIntentamos insertar un valor que no coincide con los creterios:")

print("Esto no debería permitirlo en SQL puro:")
cur.execute("insert into afiliados(documento, nombre, afiliadotitular) values ('77777777','Rodriguez Pablo',100)")
conexion.commit()
imprimir("select * from afiliados")


print("\nEsto tampoco(eliminamos un valor por numero):")
cur.execute(" delete from afiliados where numero=1;")

imprimir("select * from afiliados")
conexion.close()