import sqlite3 as sq
#operadores aritméticos y de concatenación
#el uso de as para alias, funciona si se visuzaliza el titulo de la columna.

conexion = sq.connect("bd.db")

conexion.execute("drop table if exists articulos")

conexion.execute("""create table articulos (
						codigo integer primary key,
						nombre text,
						descripcion text,
						precio real, 
						cantidad integer
					);""")

def imprimir(sql_ins):
	cursor = conexion.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)
					
print("\nInsertamos algunos articulos.")
valores = [('impresora', 'MULTIFUNCION HP 2135', 1800, 10),
		   ('impresora', 'MULTIFUNCION EPSON EXPRESSION XP241 WI-FI', 2500, 30),
		   ('monitor', 'Samsung 23', 1200, 10),
		   ('teclado', 'ingles Biswal', 100, 50),
		   ('teclado', 'español Biswal', 90, 50)]
conexion.executemany("insert into articulos (nombre, descripcion, precio, cantidad) values (?,?,?,?)", valores)
conexion.commit()

#Uso de alias.
print("\nVemos los el precio de todos los articulos (ultimo valor): ")
imprimir("select *, precio*cantidad as monto_total from articulos")

print("\nConcatenamos el nombre y la descripcion de los elementos con ' - ':")
imprimir("select nombre||' - '||descripcion from articulos")

print("\nActualizamos el precio a un descueto del 50%:")
#recordar no se puede hacer precio-=precio*0.5
conexion.execute("update articulos set precio = precio - precio*0.5")
imprimir("select * from articulos")

conexion.close()