import sqlite3 as sq
#Manejo de valores por defecto.

conexion = sq.connect("bd.db")

conexion.execute("drop table if exists prestamos;")

conexion.execute("""create table prestamos (
					codigo integer primary key,
					deudor text,
					devuelto text not null default 'NO'
				);""")
				
def imprimir(sql_ins):
	cursor = conexion.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)

print("\nInsertamos dos elementos, con el valor por defecto y uno con valor 'YES'")
conexion.executemany("insert into prestamos (deudor) values (?)", [('Roberto',),('Juanita',)])
conexion.execute("insert into prestamos (deudor, devuelto) values ('Ramayana', 'YES')")
conexion.commit()
imprimir("select * from prestamos;")

conexion.close()