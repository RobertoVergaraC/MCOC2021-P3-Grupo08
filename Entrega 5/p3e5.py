import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gps
import csv
from shapely.geometry import LineString

# gdf_ geodataframe
zonas_gdf = gps.read_file("eod.json")

#PRIMERO ABRIMOS NUESTRO GRAFO
ox.config(use_cache=True, log_console=True)
G = nx.read_gpickle("Santiago_Grueso.gpickle")

# for i, edge in enumerate(G.edges):
# 	if "geometry" in G.edges[edge[0], edge[1], 0]:
# 		if G.edges[edge[0], edge[1], 0]["geometry"] == np.nan:
# 			G.edges[edge[0], edge[1], 0]["geometry"] = LineString([(G.nodes[edge[0]]["x"],G.nodes[edge[0]]["y"]),(G.nodes[edge[1]]["x"],G.nodes[edge[1]]["y"])])
# 		else:
# 			G.edges[edge[0], edge[1], 0]["geometry"] = G.edges[edge[0], edge[1], 0]["geometry"]
# 	else:
# 		a = LineString([(G.nodes[edge[0]]["x"],G.nodes[edge[0]]["y"]),(G.nodes[edge[1]]["x"],G.nodes[edge[1]]["y"])])
# 		nx.set_edge_attributes(G, a, "geometry")

# TRANSFORMAMOS A GDF
gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)

# csv file name
filename = "mod2.csv"
  
rows = []
with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
    	if row != []:
    		rows.append(row)

Matriz_OD={}
for i in rows:
	Matriz_OD[(int(i[0]), int(i[1]))] = float(i[2])

zonas_seleccionadas_id = []
for key in Matriz_OD:
	zonas_seleccionadas_id.append(key[0])
	zonas_seleccionadas_id.append(key[1])

zonas_seleccionadas = zonas_gdf[zonas_gdf.ID.isin(zonas_seleccionadas_id)]

#gdf_edges_seleccionados = gps.clip(gdf_edges, zonas_seleccionadas)
# print(gdf_edges_seleccionados)

fig, ax = plt.subplots(1, 1)

zonas_seleccionadas.plot(ax=ax, color="#CDCDCD")

gdf_edges[gdf_edges.highway=="tertiary"].plot(ax=ax, color="blue", linewidth=0.5)
gdf_edges[gdf_edges.highway=="secondary"].plot(ax=ax, color="green", linewidth=0.5)
gdf_edges[gdf_edges.highway=="primary"].plot(ax=ax, color="yellow", linewidth=0.5)
gdf_edges[gdf_edges.highway=="motorway"].plot(ax=ax, color="orange", linewidth=0.5)
gdf_edges[gdf_edges.name=="Autopista Vespucio Oriente"].plot(ax=ax, color="red", linewidth=3)

plt.show()