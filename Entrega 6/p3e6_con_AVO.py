import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gps
import csv

# gdf_ geodataframe
zonas_gdf = gps.read_file("eod.json")

#PRIMERO ABRIMOS NUESTRO GRAFO
ox.config(use_cache=True, log_console=True)
G = nx.read_gpickle("Santiago_con_AVO.gpickle")

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

zonas_seleccionadas.plot(ax=ax, color="#CDCDCD")

gdf_edges_seleccionados[gdf_edges_seleccionados.highway=="motorway"].plot(ax=ax, color="orange", linewidth=0.5)
gdf_edges_seleccionados[gdf_edges_seleccionados.highway=="primary"].plot(ax=ax, color="yellow", linewidth=0.5)
gdf_edges_seleccionados[gdf_edges_seleccionados.highway=="secondary"].plot(ax=ax, color="green", linewidth=0.5)
gdf_edges_seleccionados[gdf_edges_seleccionados.highway=="tertiary"].plot(ax=ax, color="blue", linewidth=0.5)

gdf_edges[gdf_edges.name=="Autopista Vespucio Oriente"].plot(ax=ax, color="red", linewidth=3)

plt.show()