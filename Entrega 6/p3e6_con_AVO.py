import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gps
import csv
import matplotlib.patches as mpatches

# gdf_ geodataframe
zonas_gdf = gps.read_file("eod.json")

#PRIMERO ABRIMOS NUESTRO GRAFO
ox.config(use_cache=True, log_console=True)
G = nx.read_gpickle("Santiago_con_AVO.gpickle")

#Crear atributo pos y encontrar x max, xmin, y max e y min
x_max = 0
x_min = np.infty
y_max = 0
y_min = np.infty
nx.set_node_attributes(G, 1, "pos")
for i, node in enumerate(G.nodes):
	new_pos = (G.nodes[node]["x"], G.nodes[node]["y"])
	if abs(G.nodes[node]["x"]) > abs(x_max):
		x_max = G.nodes[node]["x"]
	if abs(G.nodes[node]["x"]) < abs(x_min):
		x_min = G.nodes[node]["x"]
	if abs(G.nodes[node]["y"]) > abs(y_max):
		y_max = G.nodes[node]["y"]
	if abs(G.nodes[node]["y"]) < abs(y_min):
		y_min = G.nodes[node]["y"]
	G.nodes[node]["pos"] = new_pos

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

print(f"Cantidad de Zonas: {len(zonas_seleccionadas_id)}")

viajes_totales = 0
for key in Matriz_OD:
	viajes_totales += float(Matriz_OD[key]) 

print(f"Cantidad de Viajes: {viajes_totales}")

gdf_edges_seleccionados = gps.clip(gdf_edges, zonas_seleccionadas)


#Graficamos Calles y Zonas
plt.figure()
ax = plt.subplot(111)

plt.suptitle("Santiago con AVO calles y con zonas seleccionadas")

zonas_seleccionadas.plot(ax=ax, color="#CDCDCD")

gdf_edges_seleccionados[gdf_edges_seleccionados.highway=="motorway"].plot(ax=ax, color="orange", linewidth=0.5)
gdf_edges_seleccionados[gdf_edges_seleccionados.highway=="primary"].plot(ax=ax, color="yellow", linewidth=0.5)
gdf_edges_seleccionados[gdf_edges_seleccionados.highway=="secondary"].plot(ax=ax, color="green", linewidth=0.5)
gdf_edges_seleccionados[gdf_edges_seleccionados.highway=="tertiary"].plot(ax=ax, color="blue", linewidth=0.5)

plt.savefig("Santiago con AVO calles y con zonas seleccionadas", dpi = 300, bbox_inches = 'tight')

#plt.show()

#REALIZAMOS GRAFO

fig, ax = plt.subplots()

zonas_gdf.plot(ax=ax, color='#CDCDCD')

plt.suptitle("Grafo Santiago con AVO")

pos = nx.get_node_attributes(G, "pos")
nx.draw(G, pos = pos, ax = ax, with_labels=False, font_weight = 50, font_size=2, width=0.2, node_size=3, arrowsize=6, edge_color="red")
	
plt.savefig("Grafo Santiago con AVO", dpi = 300, bbox_inches = 'tight')

#plt.show()

#REALIZAMOS GRAFO (Dividido en 16 zonas)
x = ((x_min-x_max)/4)
y = ((y_min-y_max)/4)
zonas_a_graficar = [[(x_max + x*0, x_max + x*1),(y_max + y*3, y_max + y*4)],[(x_max + x*1, x_max + x*2),(y_max + y*3, y_max + y*4)],[(x_max + x*2, x_max + x*3),(y_max + y*3, y_max + y*4)],[(x_max + x*3, x_max + x*4),(y_max + y*3, y_max + y*4)],
					[(x_max + x*0, x_max + x*1),(y_max + y*2, y_max + y*3)],[(x_max + x*1, x_max + x*2),(y_max + y*2, y_max + y*3)],[(x_max + x*2, x_max + x*3),(y_max + y*2, y_max + y*3)],[(x_max + x*3, x_max + x*4),(y_max + y*2, y_max + y*3)],
					[(x_max + x*0, x_max + x*1),(y_max + y*1, y_max + y*2)],[(x_max + x*1, x_max + x*2),(y_max + y*1, y_max + y*2)],[(x_max + x*2, x_max + x*3),(y_max + y*1, y_max + y*2)],[(x_max + x*3, x_max + x*4),(y_max + y*1, y_max + y*2)],
					[(x_max + x*0, x_max + x*1),(y_max + y*0, y_max + y*1)],[(x_max + x*1, x_max + x*2),(y_max + y*0, y_max + y*1)],[(x_max + x*2, x_max + x*3),(y_max + y*0, y_max + y*1)],[(x_max + x*3, x_max + x*4),(y_max + y*0, y_max + y*1)]]
coordenadas = [1,1]
for i in zonas_a_graficar:
	fig, ax = plt.subplots()

	zonas_gdf.plot(ax=ax, color='#CDCDCD')

	ax.set(xlim = i[0], ylim = i[1])

	plt.suptitle(f"Grafo Santiago con AVO {coordenadas}")

	pos = nx.get_node_attributes(G, "pos")
	nx.draw(G, pos = pos, ax = ax, with_labels=False, font_weight = 50, font_size=2, width=0.2, node_size=3, arrowsize=6, edge_color="red")
	
	plt.savefig(f"Grafo Santiago con AVO parte {coordenadas}", dpi = 300, bbox_inches = 'tight')
	
	if coordenadas[1] == 4:
		coordenadas[0] += 1
		coordenadas[1] = 1
	else:
		coordenadas[1] += 1

	#plt.show()



#PARTIMOS CON WARDROP
def weightfun(n1, n2, arco):
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


nx.set_edge_attributes(G, 0, "flujo")
nx.set_edge_attributes(G, 0, "costo")


Matriz_OD_target = Matriz_OD.copy()

incrementos = [0.1]*9 + [0.01]*9 + [0.001]*9 + [0.0001]*10
#print(sum(incrementos)==1)
for incremento in incrementos:
	for key in Matriz_OD:

		origen = key[0]
		destino = key[1]
		demanda_actual = Matriz_OD[key]
		demanda_objetivo = Matriz_OD_target[key]
		
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

		if demanda_actual > 0.:
			#Ruta mínima
			try:
				path = list(nx.dijkstra_path(G, origen, destino, weight=weightfun))

				#Incrementar flujo en la ruta mínima
				Nparadas = len(path)
				for i_parada in range(Nparadas-1):
					o = path[i_parada]
					d = path[i_parada + 1]
					G.edges[o, d, 0]["flujo"] += incremento*demanda_objetivo

				Matriz_OD[key] -= incremento*demanda_objetivo
				#print("DALE WN TODO ES POSIBLE")
			except:
				#print("No es posible")
				continue

costo_max = 0
flujo_max = 0
contador = 0
costo_total = 0
for i, edge in enumerate(G.edges):
	arco = G.edges[edge]

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
	costo_total += costo
	G.edges[edge]["costo"] = costo

	if f!= 0:
		contador+=1

	if costo_max<costo:
		costo_max = costo
	if flujo_max<f:
		flujo_max = f

print(f"flujo_max = {flujo_max}")
print(f"costo_max = {costo_max}")
print(f"Arcos usados = {contador}")
print(f"Costo Total = {costo_total}")


nx.write_gpickle(G, "Wardrop_con_AVO.gpickle")


colores_flujo = []
colores_costo = []

for i, edge in enumerate(G.edges):
	if G.edges[edge]["flujo"] < flujo_max/5:
		colores_flujo.append("blue")
	elif G.edges[edge]["flujo"] < 2*flujo_max/5:
		colores_flujo.append("green")
	elif G.edges[edge]["flujo"] < 3*flujo_max/5:
		colores_flujo.append("yellow")
	elif G.edges[edge]["flujo"] < 4*flujo_max/5:
		colores_flujo.append("orange")
	else:
		colores_flujo.append("red")

	if G.edges[edge]["costo"] < costo_max/5:
		colores_costo.append("blue")
	elif G.edges[edge]["costo"] < 2*costo_max/5:
		colores_costo.append("green")
	elif G.edges[edge]["costo"] < 3*costo_max/5:
		colores_costo.append("yellow")
	elif G.edges[edge]["costo"] < 4*costo_max/5:
		colores_costo.append("orange")
	else:
		colores_costo.append("red")


fig, ax = plt.subplots()
zonas_seleccionadas.plot(ax=ax, color='#CDCDCD')
pos = nx.get_node_attributes(G, "pos")
plt.suptitle("Flujo con AVO")
nx.draw(G, pos = pos, ax = ax, with_labels=False, font_weight = 50, font_size=2, width=0.2, node_size=3, arrowsize=6, edge_color=colores_flujo)
# labels = nx.get_edge_attributes(G, "flujo")
# nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
caso1 = mpatches.Patch(color = "blue", label=f"[{0}, {flujo_max/5}]")
caso2 = mpatches.Patch(color = "green", label=f"[{flujo_max/5}, {2*flujo_max/5}]")
caso3 = mpatches.Patch(color = "yellow", label=f"[{2*flujo_max/5}, {3*flujo_max/5}]")
caso4 = mpatches.Patch(color = "orange", label=f"[{3*flujo_max/5}, {4*flujo_max/5}]")
caso5 = mpatches.Patch(color = "red", label=f"[{4*flujo_max/5}, {flujo_max}]")
plt.legend(handles = [caso1, caso2, caso3, caso4, caso5], loc='upper right')

plt.savefig("Flujo con AVO", dpi = 300, bbox_inches = 'tight')

fig, ax = plt.subplots()
zonas_seleccionadas.plot(ax=ax, color='#CDCDCD')
pos = nx.get_node_attributes(G, "pos")
plt.suptitle("Costo con AVO")
nx.draw(G, pos = pos, ax = ax, with_labels=False, font_weight = 50, font_size=2, width=0.2, node_size=3, arrowsize=6, edge_color=colores_costo)
# labels = nx.get_edge_attributes(G, "costo")
# nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
caso1 = mpatches.Patch(color = "blue", label=f"[{0}, {costo_max/5}]")
caso2 = mpatches.Patch(color = "green", label=f"[{costo_max/5}, {2*costo_max/5}]")
caso3 = mpatches.Patch(color = "yellow", label=f"[{2*costo_max/5}, {3*costo_max/5}]")
caso4 = mpatches.Patch(color = "orange", label=f"[{3*costo_max/5}, {4*costo_max/5}]")
caso5 = mpatches.Patch(color = "red", label=f"[{4*costo_max/5}, {costo_max}]")
plt.legend(handles = [caso1, caso2, caso3, caso4, caso5], loc='upper right')

plt.savefig("Costo con AVO", dpi = 300, bbox_inches = 'tight')




#REALIZAMOS GRAFO (Dividido en 16 zonas)
x = ((x_min-x_max)/4)
y = ((y_min-y_max)/4)
zonas_a_graficar = [[(x_max + x*0, x_max + x*1),(y_max + y*3, y_max + y*4)],[(x_max + x*1, x_max + x*2),(y_max + y*3, y_max + y*4)],[(x_max + x*2, x_max + x*3),(y_max + y*3, y_max + y*4)],[(x_max + x*3, x_max + x*4),(y_max + y*3, y_max + y*4)],
					[(x_max + x*0, x_max + x*1),(y_max + y*2, y_max + y*3)],[(x_max + x*1, x_max + x*2),(y_max + y*2, y_max + y*3)],[(x_max + x*2, x_max + x*3),(y_max + y*2, y_max + y*3)],[(x_max + x*3, x_max + x*4),(y_max + y*2, y_max + y*3)],
					[(x_max + x*0, x_max + x*1),(y_max + y*1, y_max + y*2)],[(x_max + x*1, x_max + x*2),(y_max + y*1, y_max + y*2)],[(x_max + x*2, x_max + x*3),(y_max + y*1, y_max + y*2)],[(x_max + x*3, x_max + x*4),(y_max + y*1, y_max + y*2)],
					[(x_max + x*0, x_max + x*1),(y_max + y*0, y_max + y*1)],[(x_max + x*1, x_max + x*2),(y_max + y*0, y_max + y*1)],[(x_max + x*2, x_max + x*3),(y_max + y*0, y_max + y*1)],[(x_max + x*3, x_max + x*4),(y_max + y*0, y_max + y*1)]]
coordenadas = [1,1]
for i in zonas_a_graficar:
	fig, ax = plt.subplots()

	zonas_seleccionadas.plot(ax=ax, color='#CDCDCD')

	ax.set(xlim = i[0], ylim = i[1])

	plt.suptitle(f"Grafo Flujo Santiago con AVO {coordenadas}")

	pos = nx.get_node_attributes(G, "pos")
	nx.draw(G, pos = pos, ax = ax, with_labels=False, font_weight = 50, font_size=2, width=0.2, node_size=3, arrowsize=6, edge_color=colores_flujo)
	
	caso1 = mpatches.Patch(color = "blue", label=f"[{0}, {flujo_max/5}]")
	caso2 = mpatches.Patch(color = "green", label=f"[{flujo_max/5}, {2*flujo_max/5}]")
	caso3 = mpatches.Patch(color = "yellow", label=f"[{2*flujo_max/5}, {3*flujo_max/5}]")
	caso4 = mpatches.Patch(color = "orange", label=f"[{3*flujo_max/5}, {4*flujo_max/5}]")
	caso5 = mpatches.Patch(color = "red", label=f"[{4*flujo_max/5}, {flujo_max}]")
	plt.legend(handles = [caso1, caso2, caso3, caso4, caso5], loc='upper right')

	plt.savefig(f"Grafo Flujo Santiago con AVO parte {coordenadas}", dpi = 300, bbox_inches = 'tight')
	
	if coordenadas[1] == 4:
		coordenadas[0] += 1
		coordenadas[1] = 1
	else:
		coordenadas[1] += 1


x = ((x_min-x_max)/4)
y = ((y_min-y_max)/4)
zonas_a_graficar = [[(x_max + x*0, x_max + x*1),(y_max + y*3, y_max + y*4)],[(x_max + x*1, x_max + x*2),(y_max + y*3, y_max + y*4)],[(x_max + x*2, x_max + x*3),(y_max + y*3, y_max + y*4)],[(x_max + x*3, x_max + x*4),(y_max + y*3, y_max + y*4)],
					[(x_max + x*0, x_max + x*1),(y_max + y*2, y_max + y*3)],[(x_max + x*1, x_max + x*2),(y_max + y*2, y_max + y*3)],[(x_max + x*2, x_max + x*3),(y_max + y*2, y_max + y*3)],[(x_max + x*3, x_max + x*4),(y_max + y*2, y_max + y*3)],
					[(x_max + x*0, x_max + x*1),(y_max + y*1, y_max + y*2)],[(x_max + x*1, x_max + x*2),(y_max + y*1, y_max + y*2)],[(x_max + x*2, x_max + x*3),(y_max + y*1, y_max + y*2)],[(x_max + x*3, x_max + x*4),(y_max + y*1, y_max + y*2)],
					[(x_max + x*0, x_max + x*1),(y_max + y*0, y_max + y*1)],[(x_max + x*1, x_max + x*2),(y_max + y*0, y_max + y*1)],[(x_max + x*2, x_max + x*3),(y_max + y*0, y_max + y*1)],[(x_max + x*3, x_max + x*4),(y_max + y*0, y_max + y*1)]]
coordenadas = [1,1]
for i in zonas_a_graficar:
	fig, ax = plt.subplots()

	zonas_seleccionadas.plot(ax=ax, color='#CDCDCD')

	ax.set(xlim = i[0], ylim = i[1])

	plt.suptitle(f"Grafo Costo Santiago con AVO {coordenadas}")

	pos = nx.get_node_attributes(G, "pos")
	nx.draw(G, pos = pos, ax = ax, with_labels=False, font_weight = 50, font_size=2, width=0.2, node_size=3, arrowsize=6, edge_color=colores_costo)
	
	caso1 = mpatches.Patch(color = "blue", label=f"[{0}, {costo_max/5}]")
	caso2 = mpatches.Patch(color = "green", label=f"[{costo_max/5}, {2*costo_max/5}]")
	caso3 = mpatches.Patch(color = "yellow", label=f"[{2*costo_max/5}, {3*costo_max/5}]")
	caso4 = mpatches.Patch(color = "orange", label=f"[{3*costo_max/5}, {4*costo_max/5}]")
	caso5 = mpatches.Patch(color = "red", label=f"[{4*costo_max/5}, {costo_max}]")
	plt.legend(handles = [caso1, caso2, caso3, caso4, caso5], loc='upper right')

	plt.savefig(f"Grafo Costo Santiago con AVO parte {coordenadas}", dpi = 300, bbox_inches = 'tight')
	
	if coordenadas[1] == 4:
		coordenadas[0] += 1
		coordenadas[1] = 1
	else:
		coordenadas[1] += 1
