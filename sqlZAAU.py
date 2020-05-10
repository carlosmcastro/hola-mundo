import sqlite3 as sq
#trigger clausula when.
#condiciona la aparicion del trigger, sin necesidad del uso de select case.

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

#notese el condicionador con when en el disparador.
cur.executescript("""
drop trigger if exists disparador_claves_anteriores;

create trigger disparador_claves_anteriores
		before update on usuarios
		when new.clave<>old.clave
	begin
		insert into clavesanteriores values(old.nombre, old.clave);
	end;
""")


conexion.commit()

def imprimir(sql_ins):
	cursor = cur.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)

print("\nInsertamos a un usuario:")
cur.execute("insert into usuarios values ('Pepe', 'UruguayChilli25')")
conexion.commit()

def ver_tablas():
	print("\nUsuarios:")
	imprimir("select * from usuarios")
	print("\nClaves Anteriores:")
	imprimir("select * from clavesanteriores")

ver_tablas()

print("\nActualizamos la clave:")
cur.execute("update usuarios set clave='UUEEchojo34' where nombre='Pepe'")
ver_tablas()

print("\nActualizamos la clave, con el mismo valor que tenía:")
cur.execute("update usuarios set clave='UUEEchojo34' where nombre='Pepe'")
ver_tablas()

print("\nNotese que la inserción no se realizo, ya que la clave nueva es igual a la vieja.")

conexion.close()