import sqlite3 as sq
#Uso de stftime para manejar el formato de visualizacion de fechas.

conexion = sq.connect("bd.db")
cur = conexion.cursor()

cur.executescript(""" 
drop table if exists asistencia;

create table asistencia(
	dni text,
	fechahora text,
	primary key(dni, fechahora)
);
""")
conexion.commit()

def imprimir(sql_ins):
	cursor = cur.execute(sql_ins)
	for fila in cursor.fetchall():
		print(fila)

valores = [('11111111', '2018-09-14 08:00:00'),
		    ('22222222', '2018-09-14 06:12:00'),
		    ('33333333', '2018-09-14 18:05:00'),
		    ('11111111', '2018-09-15 08:02:00'),
		    ('22222222', '2018-09-15 06:00:00'),
		    ('33333333', '2018-12-15 14:00:00')]
cur.executemany("insert into asistencia values (?,?)", valores)

conexion.commit()

print("\nAsistencia:")
imprimir("select * from asistencia")

print("\nEn formato día/mes/año:")
#%d día, %m mes, %Y año.
imprimir("select dni, strftime('%d/%m/%Y', fechahora) from asistencia")

print("\nEn formato Horas:Minutos :")
imprimir("select dni, strftime('%H:%M', fechahora) from asistencia")


print("\nImprimir el nombre del mes en cada fecha:")
imprimir("""select dni, case strftime('%m', fechahora)
			when '01' THEN 'Enero'
			when '02' THEN 'Febrero'
			when '03' THEN 'Marzo'
			when '04' THEN 'Abril'
			when '05' THEN 'Mayo'
			when '06' THEN 'Junio'
			when '07' THEN 'Julio'
			when '08' THEN 'Agosto'
			when '09' THEN 'Septiembre'
			when '10' THEN 'Octubre'
			when '11' THEN 'Noviembre'
			when '12' THEN 'Diciembre'
			end as mes
			from asistencia;			
""")

#Notese que este select no posee from, ya que no extrae datos de tabla alguna.
print("\nHoy es DÍA de MES de AÑO:")
imprimir("""select 'Hoy es ' || strftime('%d', date('now')) || ' de ' || case strftime('%m', date('now'))
			when '01' THEN 'Enero'
			when '02' THEN 'Febrero'
			when '03' THEN 'Marzo'
			when '04' THEN 'Abril'
			when '05' THEN 'Mayo'
			when '06' THEN 'Junio'
			when '07' THEN 'Julio'
			when '08' THEN 'Agosto'
			when '09' THEN 'Septiembre'
			when '10' THEN 'Octubre'
			when '11' THEN 'Noviembre'
			when '12' THEN 'Diciembre'
			end || ' de ' || strftime('%Y', date('now')) as fecha;
""")

print("\nHORA horas y MINUTO minutos y SEGUNDO segundos:")
imprimir("""select strftime('%H', time('now', 'localtime'))||' Horas y '||strftime('%M', time('now', 'localtime'))||' minutos y '||
			strftime('%S', time('now', 'localtime'))||' segundos'
""")

print("\nDía de la semana:")
#a veces comienza desde el 0, en lugar del 1
imprimir("""select case strftime('%w', datetime('now'))
			WHEN '1'THEN 'Domingo'
			WHEN '2'THEN 'Lunes'
			WHEN '3'THEN 'Martes'
			WHEN '4'THEN 'Miercoles'
			WHEN '5'THEN 'Jueves'
			WHEN '6'THEN 'Viernes'
			WHEN '7'THEN 'Sabado'
			END as diasemana
""")

print("\nDía [001-366]:")
imprimir("select strftime('%j', date('now')) as diaño")

print("\nDía en fecha Julina:")
print("[Es el número de días y fracción transcurridos desde el mediodía del 1º de enero del año 4713 a. C.]")
imprimir("select strftime('%J', date('now')) as diajuliano")

print("\nCantidad de segundos desde 01/01/1970:")
imprimir("select strftime('%s', datetime('now')) as segundos70")

print("\nSemana del año [00-53]:")
imprimir("select strftime('%W', date('now')) as semenaño")

#'now', puede usarse en lugar de date, time, y datetime. Y en ciertas ocasiones es más preciso.
print("\nSegundos fraccionarios en formato SS.SSS:")
imprimir("select strftime('%f', 'now') as segunfrac")

print("\nUso de comodín %")
imprimir("select strftime('%%Y %Y', date('now')) as comodini")

conexion.close()