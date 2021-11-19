import networkx as nx
import osmnx as ox
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gps

ox.config(use_cache=True, log_console=True)

north = -33.06
south = -33.98
east = -70.27
west = -71.45

#Vespucio Oriente esta en Construction
G = ox.graph_from_bbox(north, south, east, west, network_type="drive", clean_periphery=True, custom_filter='["highway"~"motorway|primary|secondary|tertiary|construction"]')

for i, edge in enumerate(G.edges):
	if "highway" in G.edges[edge[0], edge[1], 0] and "name" in G.edges[edge[0], edge[1], 0]:
		if G.edges[edge[0], edge[1], 0]["highway"] == "construction" and G.edges[edge[0], edge[1], 0]["name"] == "Autopista Vespucio Oriente":
			G.edges[edge[0], edge[1], 0]["highway"] = "motorway"


zonas_gdf = gps.read_file("eod.json")


gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)

fig, ax = plt.subplots(1, 1)

zonas_gdf.plot(ax=ax, color="#CDCDCD")

gdf_edges[gdf_edges.highway=="tertiary"].plot(ax=ax, color="blue", linewidth=0.5)
gdf_edges[gdf_edges.highway=="secondary"].plot(ax=ax, color="green", linewidth=0.5)
gdf_edges[gdf_edges.highway=="primary"].plot(ax=ax, color="yellow", linewidth=0.5)
gdf_edges[gdf_edges.highway=="motorway"].plot(ax=ax, color="orange", linewidth=0.5)
gdf_edges[gdf_edges.name=="Autopista Vespucio Oriente"].plot(ax=ax, color="red", linewidth=3)

plt.show()


nx.write_gpickle(G, "Santiago_Grueso.gpickle")