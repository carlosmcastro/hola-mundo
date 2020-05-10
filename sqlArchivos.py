import sqlite3 as sq
#Manejo de datos blob (archivos)


conexion = sq.connect("bd.db")
cur = conexion.cursor()

cur.executescript(""" 
drop table if exists usuarios;

create table usuarios(
	nombre text primary key,
	clave text,
	foto blob
);
""")
conexion.commit()

def imprimir(sql_ins):
	cursor = cur.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)
		
#Convierte a binario para almacenarlo.
def Archivo_A_Binario(archi):
	with open(archi, 'rb') as f:
		return f.read()
	
print("\nInsertamos el archivo con la funcion transformandolo a binario:")
cur.execute("insert into usuarios values (?,?,?)", ('PakaAlbaca', '123AlReves', Archivo_A_Binario('perfil.jpg')))

conexion.commit()

print("\nVemos el archivo binario almacenado:")
input("Presiona Enter.")
imprimir("select foto from usuarios where nombre='PakaAlbaca'")

print("\nY escribimos el archivo de la base de dato a perfil_nuevo.jpg.")
leer = cur.execute("select foto from usuarios where nombre='PakaAlbaca'")
for i in leer.fetchone():
	with open('perfil_nuevo.jpg', 'wb') as f:
		f.write(i)

conexion.close()