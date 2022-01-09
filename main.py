import csv 

#Creando listas
imports=[]
exports=[]
lista_datos=[]

##Agregando el CSV##
with open (r"C:\Users\hp1\Documents\Emtech\Analisis_02_Puc_Echeverria\synergy_logistics_database.csv", "r") as archivo: 
    registros=csv.DictReader(archivo)
    for registro in registros:
        lista_datos.append(registro)
        if registro["direction"]=="Imports":
           imports.append(registro)
        else:
          exports.append(registro)
                   
##Rutas más concurridas de acuerdo al número de corridas.##
##Se crea una funcion para importaciones y exportaciones## 
def routes_imp_exp (direccion):
  account = 0
  corridas_contada = []
  corridas_conteo = []

  for ruta in lista_datos:
      if ruta["direction"] == direccion:
         ruta_actual = [ruta["origin"], ruta["destination"]]
         if ruta_actual not in corridas_contada:
            for ruta_bd in lista_datos:
              if ruta_actual == [ruta_bd["origin"], ruta_bd["destination"]]:
                 account += 1

            corridas_contada.append(ruta_actual)
            corridas_conteo.append([ruta["origin"], ruta["destination"], account])
            account = 0
            #Se crean contadores y se agregan los elementos a nuecas listas. 
            
##Se ordenan las listas nuevas##
  corridas_conteo.sort(reverse = True, key = lambda x:x[2])
  return corridas_conteo

conteo_exports = routes_imp_exp("Exports")
conteo_imports = routes_imp_exp("Imports") 

##Se crean dos listas para presentar los 10 valores más significativos para cada ruta de exportación e importación
rutas_exports=conteo_exports[0:10]
rutas_imports=conteo_imports[0:10]

#A continuacion se imprimen las rutas más recorridas ##
total_corridas_import= []
total_corridas_export= []
print("las 10 rutas más concurridas de importación son:")
for elemento in rutas_imports:
    total_corridas_import.append(elemento[2])
    print(f" {elemento[0]}-{elemento[1]} con {elemento[2]} corridas")
    
all_sum_imp = sum(total_corridas_import)
print (f'Siendo un total de {all_sum_imp} corridas') 

print("\n")

print("las 10 rutas de exportación que más se recorren son:")
for elemento in rutas_exports:
    total_corridas_export.append(elemento[2])    
    print(f"{elemento[0]}-{elemento[1]} con {elemento[2]} corridas")

all_sum_exp = sum(total_corridas_export)
print (f'Siendo un total de {all_sum_exp} corridas') 

##Se define la funcion para los transportes mas utilizados de acuerdo ##
##con el valor generado para las importaciones y exportaciones##
def valor_transporte(direccion):
	contados = []
	valores_transporte = []

	for viaje in lista_datos:
		actual = [direccion, viaje["transport_mode"]] 
		valor = 0
		operaciones = 0

		if actual in contados:
			continue

		for movimiento in lista_datos:
			if actual == [movimiento["direction"], movimiento["transport_mode"]]:
				valor += int(movimiento["total_value"])
				operaciones += 1
		
		contados.append(actual)
		valores_transporte.append([direccion, viaje["transport_mode"], valor, operaciones])
	
	valores_transporte.sort(reverse = True, key = lambda x:x[2])
	return valores_transporte

##Se imprimen los resultados##
print("\n")

print("Exportaciones de acuerdo al transporte utilizado")
value_countries = valor_transporte("Exports")
for elemento in value_countries:
  print(f"Tipo de transporte: {elemento[1]}      Valor de exportaciones: {elemento[2]}     Veces utilizado: {elemento[3]}")

print("\n")
print("Importaciones de acuerdo con el transporte utilizado")
valor_importacion=valor_transporte("Imports")
for elemento in valor_importacion: 
   print(f"Tipo de transporte: {elemento[1]}      Valor de exportaciones: {elemento[2]}     Veces utilizado: {elemento[3]}")


##Paises que generan el 80% del valor de exportaciones e importaciones## 
def mount_per_country(lista):
##Para obtener el total, cada ganancia obtenida se agregara a "total_de_ganancias". 
##La funcion sum y len serán utiles para obtener el total de ganancias netas 
    ganancias = {}
    total_de_ganancias = []
    for elemento in lista:
        if elemento['origin'] not in ganancias:
           ganancias[elemento['origin']] = elemento['total_value']
           total_de_ganancias.append(int(elemento['total_value']))
        else:
            sumatoria_de_ganancias = int(elemento['total_value']) + int(ganancias[elemento['origin']])
            ganancias[elemento['origin']] = sumatoria_de_ganancias
            total_de_ganancias.append(int(elemento['total_value']))

##Ganancias totales y paises que aportan con el mayor numero de ganancias 
    print(f"Ganancia Total: {(sum(total_de_ganancias))} ")
    i = 0
    for value, key in sorted(ganancias.items(), key= lambda x: x[1], reverse= True):
        if i <= 80:
            porcentaje= (key * 100) / sum(total_de_ganancias)
            print(value,"   Ganancia: ",(key), " Porcentaje", round(porcentaje, 2), "% del total")
            i += round(porcentaje, 2)

##Resultados
print("\n")
print("Paises que generan el 80% del valor total de las importaciones:")
mount_per_country(imports)

print("\n")
print("Paises que generan el 80% de las exportaciones")
mount_per_country(exports)