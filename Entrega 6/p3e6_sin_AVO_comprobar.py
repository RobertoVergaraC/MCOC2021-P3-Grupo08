import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gps
import csv
from tabulate import tabulate

def weightfun_arriba(n1, n2, arco):
	arco = arco[0]

	f = arco["flujo"]*1.15

	if "lanes" in arco:
		if str(type(arco["lanes"])) == "<class 'list'>":
			arco["lanes"] = [int(i) for i in arco["lanes"]]
			p = np.average(arco["lanes"])
		else:
			p = int(arco["lanes"]) 
	else:
		p = 1
	if p<=0:
		p=1
	
	q = f/5400
	
	if "length" in arco:
		L = float(arco["length"])
	else:
		L = 100

	if "highway" in arco:
		street_type = arco["highway"]
	else:
		street_type = "NO ROUTE"

	if street_type == "motorway":
		v = 25
		u = 5
	elif street_type == "primary" or street_type == "secondary":
		v = 15
		u = 3
	else:
		v = 8
		u = 2
	
	costo = (L/v) + (5-u)*12 + (900/(u*p))*(10*q - u*p + np.sqrt((10*q-u*p)**2 + (q/9)))

	return costo


def weightfun_abajo(n1, n2, arco):
	arco = arco[0]

	f = arco["flujo"]*0.75

	if "lanes" in arco:
		if str(type(arco["lanes"])) == "<class 'list'>":
			arco["lanes"] = [int(i) for i in arco["lanes"]]
			p = np.average(arco["lanes"])
		else:
			p = int(arco["lanes"]) 
	else:
		p = 1
	if p<=0:
		p=1
	
	q = f/5400
	
	if "length" in arco:
		L = float(arco["length"])
	else:
		L = 100

	if "highway" in arco:
		street_type = arco["highway"]
	else:
		street_type = "NO ROUTE"

	if street_type == "motorway":
		v = 25
		u = 5
	elif street_type == "primary" or street_type == "secondary":
		v = 15
		u = 3
	else:
		v = 8
		u = 2
	
	costo = (L/v) + (5-u)*12 + (900/(u*p))*(10*q - u*p + np.sqrt((10*q-u*p)**2 + (q/9)))

	return costo*0.95

def weightfun_normal(n1, n2, arco):
	arco = arco[0]

	f = arco["flujo"]

	if "lanes" in arco:
		if str(type(arco["lanes"])) == "<class 'list'>":
			arco["lanes"] = [int(i) for i in arco["lanes"]]
			p = np.average(arco["lanes"])
		else:
			p = int(arco["lanes"]) 
	else:
		p = 1
	if p<=0:
		p=1
	
	q = f/5400
	
	if "length" in arco:
		L = float(arco["length"])
	else:
		L = 100

	if "highway" in arco:
		street_type = arco["highway"]
	else:
		street_type = "NO ROUTE"

	if street_type == "motorway":
		v = 25
		u = 5
	elif street_type == "primary" or street_type == "secondary":
		v = 15
		u = 3
	else:
		v = 8
		u = 2
	
	costo = (L/v) + (5-u)*12 + (900/(u*p))*(10*q - u*p + np.sqrt((10*q-u*p)**2 + (q/9)))

	return costo


# gdf_ geodataframe
zonas_gdf = gps.read_file("eod.json")

#PRIMERO ABRIMOS NUESTRO GRAFO
ox.config(use_cache=True, log_console=True)
G = nx.read_gpickle("Wardrop_sin_AVO.gpickle")

# csv file name
filename = "mod_final.csv"
  
rows = []
with open(filename, 'r') as csvfile:
	csvreader = csv.reader(csvfile)
	for row in csvreader:
		if row != []:
			rows.append(row)

Matriz_OD={}
for i in rows:
	if i[0] != 324 or i[1] != 324:
		Matriz_OD[(int(i[0]), int(i[1]))] = float(i[2])

zonas_seleccionadas_id = []
for key in Matriz_OD:
	zonas_seleccionadas_id.append(key[0])
	zonas_seleccionadas_id.append(key[1])

zonas_seleccionadas_id = sorted(set(zonas_seleccionadas_id))

zonas_seleccionadas = zonas_gdf[zonas_gdf.ID.isin(zonas_seleccionadas_id)]

# TRANSFORMAMOS A GDF
gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)


#COLUMNAS A GRAFICAR
# 1) Origen-Destino
# 2) RUTAS CON = COSTO
# 3) VALOR AVERAGE COSTOS
# lista = [[1,2,3],[1,2,3]...[1,2,3]]
TABLA = []

#Chequear costos
print(f"Costos\n")
contador = 1
for key in Matriz_OD:
	origen = key[0]
	destino = key[1]
	tabla = []

	#ORIGEN
	possible_nodes = gps.sjoin(gdf_nodes, zonas_seleccionadas[zonas_seleccionadas.ID==origen], op="within")
	try:
		origen = possible_nodes.sample().index[0]
	except:
		try:
			p = zonas_seleccionadas[zonas_seleccionadas.ID==key[0]].representative_point()
			cx_zona_origen, cy_zona_origen = float(p.x), float(p.y)
		except:
			try:
				cx_zona_origen, cy_zona_origen = float(zonas_seleccionadas[zonas_seleccionadas.ID==key[0]].centroid.x), float(zonas_seleccionadas[zonas_seleccionadas.ID==key[0]].centroid.y)
				
				distancia_minima = np.infty

				for i, node in enumerate(G.nodes):
					cx_nodo = G.nodes[node]["x"]
					cy_nodo = G.nodes[node]["y"]
			
					dist_nodo = np.sqrt((cx_nodo-cx_zona_origen)**2 + (cy_nodo-cy_zona_origen)**2)
			
					if dist_nodo < distancia_minima:
						distancia_minima = dist_nodo
						origen = node

			except:
				continue


	#DESTINO
	possible_nodes = gps.sjoin(gdf_nodes, zonas_seleccionadas[zonas_seleccionadas.ID==destino], op="within")
	try:
		destino = possible_nodes.sample().index[0]
	except:
		try:
			p = zonas_seleccionadas[zonas_seleccionadas.ID==key[1]].representative_point()
			cx_zona_destino, cy_zona_destino = float(p.x), float(p.y)
		except:
			try:
				cx_zona_destino, cy_zona_destino = float(zonas_seleccionadas[zonas_seleccionadas.ID==key[1]].centroid.x), float(zonas_seleccionadas[zonas_seleccionadas.ID==key[1]].centroid.y)
			
				distancia_minima = np.infty

				for i, node in enumerate(G.nodes):
					cx_nodo = G.nodes[node]["x"]
					cy_nodo = G.nodes[node]["y"]
			
					dist_nodo = np.sqrt((cx_nodo-cx_zona_destino)**2 + (cy_nodo-cy_zona_destino)**2)
			
					if dist_nodo < distancia_minima:
						distancia_minima = dist_nodo
						destino = node
			except:
				continue

	#print(f"COSTOS VIAJE RUTAS MÁS CORTAS {origen}{destino}")
	try:
		paths_arriba = list(nx.all_shortest_paths(G, origen, destino, weight=weightfun_arriba))
		paths_abajo = list(nx.all_shortest_paths(G, origen, destino, weight=weightfun_abajo))
		paths = list(nx.all_shortest_paths(G, origen, destino, weight=weightfun_normal))
		path = list(nx.dijkstra_path(G, origen, destino, weight="costo"))

		paths_final = paths_abajo + paths_arriba + paths
		new_k = []
		for elem in paths_final:
		    if elem not in new_k:
		        new_k.append(elem)
		paths_final = new_k
		#print(paths_final)

		tabla.append(f"{key[0]} - {key[1]}")

		costo_min = 0
		Nparada_min = len(path)
		for j_parada in range(Nparada_min-1):
			o = path[j_parada]
			d = path[j_parada + 1]
			costo_min += G.edges[o, d, 0]["costo"]

		costos_seleccionados = []
		paths_seleccionados = 0
		errores_seleccionados = []
		for i in paths_final:
			costo = 0
			Nparadas = len(i)

			for i_parada in range(Nparadas-1):
				o = i[i_parada]
				d = i[i_parada + 1]
				costo += G.edges[o, d, 0]["costo"]

			if (costo_min*0.95) <= costo and costo <= (costo_min*1.05):
				costos_seleccionados.append(costo)
				paths_seleccionados+=1
				if costo_min != costo:
					error = (abs(costo-costo_min)/costo_min)*100
					#print(f"RUTAS: {i} con un costo de {costo} con un error de {error}%.")
					errores_seleccionados.append(error)
				else:
					#print(f"RUTAS: {i} con un costo de {costo}")
					errores_seleccionados.append(0)
		tabla.append(paths_seleccionados)
		tabla.append(np.average(costos_seleccionados))
		if len(errores_seleccionados)<=1:
			tabla.append(f"{errores_seleccionados[0]}%")
		else:
			tabla.append(f"{sum(errores_seleccionados)/(len(errores_seleccionados)-1)}%")
		TABLA.append(tabla)
		print(f"El contador va en = {contador} de 1252")
		contador+=1
	except:
		print("Par OD no posible")
		contador+=1

print(tabulate(TABLA, headers=['ORIGEN - DESTINO (ZONAS)', 'CANTIDAD PATHS SELECCIONADOS', 'COSTOS', 'ERROR COSTOS'], tablefmt='grid'))