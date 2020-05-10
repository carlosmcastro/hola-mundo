import sqlite3 as sq
#trigger permite generar eventos al insertar, eliminar, o actualizar.
#la tabla.

conexion = sq.connect("bd.db")
cur = conexion.cursor()

cur.executescript(""" 
drop table if exists usuarios;
drop table if exists clavesanteriores;

create table usuarios(
	nombre text primary key,
	clave text
);
create table clavesanteriores(
	nombre text,
	clave text
);
""")

#Borramos el disparador si existía previamente.
cur.execute("drop trigger if exists disparador_claves_anteriores")

#Creamos el trigger(disparador)
#se activa el disparador cuando se actualiza la tabla usuarios.
#inserta en clavesanteriores con la palabra clave old el nombre y clave vieja.
#tambien existe new, que sería el dato actualizante.
cur.execute("""
	create trigger disparador_claves_anteriores
			before update
			on usuarios
		begin
			insert into clavesanteriores(nombre, clave) values(old.nombre, old.clave);
		end;
""")
conexion.commit()

def imprimir(sql_ins):
	cursor = cur.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)

cur.execute("insert into usuarios(nombre, clave) values ('marcos','123abc')")

conexion.commit()

print("\nInsertamos unos elementos (notese que no se activa el trigger porque solo estamos insertando elementos)")

print("\nUsuarios:")
imprimir("select * from usuarios")
print("\nClaves Anteriores:")
imprimir("select * from clavesanteriores")

print("\nActualizamos la clave (aquí si se activa el trigger insertando los viejos datos a clavesanteriores):")
cur.execute("update usuarios set clave='3232' where nombre='marcos'")

print("\nUsuarios")
imprimir("select * from usuarios")
print("\nClaves Anteriores")
imprimir("select * from clavesanteriores")

print("\nVolvemos a actualizar la clave:")
cur.execute("update usuarios set clave='Alairalaira' where nombre='marcos'")

print("\nUsuarios")
imprimir("select * from usuarios")
print("\nClaves Anteriores")
imprimir("select * from clavesanteriores")

conexion.close()