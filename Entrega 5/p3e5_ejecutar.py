import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gps
import csv

def weightfun(n1, n2, arco):
	arco = arco[0]
	f = 0
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
	costo = (L/v) + (5-u)*12 + (900/(u*p))*(10*q - u*p +np.sqrt((10*q-u*p)**2 + (q/9)))
	return costo

# gdf_ geodataframe
zonas_gdf = gps.read_file("eod.json")

#PRIMERO ABRIMOS NUESTRO GRAFO
ox.config(use_cache=True, log_console=True)
G = nx.read_gpickle("Santiago_Grueso.gpickle")


# TRANSFORMAMOS A GDF
gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)

# csv file name
filename = "mod.csv"
  
rows = []

with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        rows.append(row)

Matriz_OD={}
for i in rows:
	Matriz_OD[(int(i[0]), int(i[1]))] = float(i[2])

zonas_seleccionadas_id = []
for key in Matriz_OD:
	zona_origen = key[0]
	zona_destino = key[1]

	#Representative Point Origen
	p = zonas_gdf[zonas_gdf.ID==zona_origen].representative_point()
	try:
		cx_zona_origen, cy_zona_origen = float(p.x), float(p.y)
	except:
		try:
			cx_zona_origen, cy_zona_origen = float(zonas_gdf[zonas_gdf.ID==zona_origen].centroid.x), float(zonas_gdf[zonas_gdf.ID==zona_origen].centroid.y)
		except:
			print("NO HAY PUNTO")

	distancia_minima = np.infty

	for i, node in enumerate(G.nodes):
		cx_nodo = G.nodes[node]["x"]
		cy_nodo = G.nodes[node]["y"]
	    
		dist_nodo = np.sqrt((cx_nodo-cx_zona_origen)**2 + (cy_nodo-cy_zona_origen)**2)
	    
		if dist_nodo < distancia_minima:
			distancia_minima = dist_nodo
			nodo_origen = node

	#Representative Point Destino
	p = zonas_gdf[zonas_gdf.ID==zona_destino].representative_point()
	try:
		cx_zona_destino, cy_zona_destino = float(p.x), float(p.y)
	except:
		try:
			cx_zona_destino, cy_zona_destino = float(zonas_gdf[zonas_gdf.ID==zona_destino].centroid.x), float(zonas_gdf[zonas_gdf.ID==zona_destino].centroid.y)
		except:
			print("NO HAY PUNTO")

	distancia_minima = np.infty

	for i, node in enumerate(G.nodes):
		cx_nodo = G.nodes[node]["x"]
		cy_nodo = G.nodes[node]["y"]
	    
		dist_nodo = np.sqrt((cx_nodo-cx_zona_destino)**2 + (cy_nodo-cy_zona_destino)**2)
	    
		if dist_nodo < distancia_minima:
			distancia_minima = dist_nodo
			nodo_destino = node
	try:
		take_paths = list(nx.all_shortest_paths(G, nodo_origen, nodo_destino, weight=weightfun))
		#print(take_paths)

		for take_path in take_paths:
			Nparadas = len(take_path)

			for i_parada in range(Nparadas-1):
				n1 = take_path[i_parada]
				n2 = take_path[i_parada+1]
				tomar_arco = 0

				arco = G.edges[n1, n2, tomar_arco]

				if "name" in arco:
					nombre = str(arco["name"])
				else:
					nombre = "CALLE SIN NOMBRE"

				if nombre.find("Américo Vespucio Oriente") >=0:
					zonas_seleccionadas_id.append(zona_origen)
					zonas_seleccionadas_id.append(zona_destino)
	except:
		print("SIN RUTAS POSIBLES")

zonas_seleccionadas_id = sorted(set(zonas_seleccionadas_id))
zonas_seleccionadas = zonas_gdf[zonas_gdf.ID.isin(zonas_seleccionadas_id)]
#print(zonas_seleccionadas_id)
#print(zonas_seleccionadas)

#gdf_edges_seleccionados = gps.clip(gdf_edges, zonas_seleccionadas)

plt.figure()
ax = plt.subplot(111)

zonas_seleccionadas.plot(ax=ax, color="#CDCDCD")

gdf_edges[gdf_edges.highway=="tertiary"].plot(ax=ax, color="blue", linewidth=0.5)
gdf_edges[gdf_edges.highway=="secondary"].plot(ax=ax, color="green", linewidth=0.5)
gdf_edges[gdf_edges.highway=="primary"].plot(ax=ax, color="yellow", linewidth=0.5)
gdf_edges[gdf_edges.highway=="motorway"].plot(ax=ax, color="orange", linewidth=0.5)
gdf_edges[gdf_edges.name=="Américo Vespucio Oriente"].plot(ax=ax, color="red", linewidth=5)

# gdf_edges_seleccionados[gdf_edges_seleccionados.highway=="tertiary"].plot(ax=ax, color="blue", linewidth=0.5)
# gdf_edges_seleccionados[gdf_edges_seleccionados.highway=="secondary"].plot(ax=ax, color="green", linewidth=0.5)
# gdf_edges_seleccionados[gdf_edges_seleccionados.highway=="primary"].plot(ax=ax, color="yellow", linewidth=0.5)
# gdf_edges_seleccionados[gdf_edges_seleccionados.highway=="motorway"].plot(ax=ax, color="orange", linewidth=0.5)
# gdf_edges_seleccionados[gdf_edges_seleccionados.name=="Américo Vespucio Oriente"].plot(ax=ax, color="red", linewidth=5)
plt.show()

Matriz_OD_final={}

for key in Matriz_OD:
	if key[0] in zonas_seleccionadas_id or key[1] in zonas_seleccionadas_id:
		Matriz_OD_final[(int(key[0]), int(key[1]))] = float(Matriz_OD[key])


a_file = open("mod2.csv", "w")

writer = csv.writer(a_file)
for key, value in Matriz_OD_final.items():
    writer.writerow([key[0], key[1], value])

a_file.close()