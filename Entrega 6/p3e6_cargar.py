import osmnx as ox
import networkx as nx

ox.config(use_cache=True, log_console=True)

north = -33.06
south = -33.98
east = -70.27
west = -71.45

#Vespucio Oriente esta en Construction
G_AVO = ox.graph_from_bbox(north, south, east, west, network_type="drive", clean_periphery=True, custom_filter='["highway"~"motorway|primary|secondary|tertiary|construction"]')

for i, edge in enumerate(G_AVO.edges):
	if "highway" in G_AVO.edges[edge[0], edge[1], 0] and "name" in G_AVO.edges[edge[0], edge[1], 0]:
		if G_AVO.edges[edge[0], edge[1], 0]["highway"] == "construction" and G_AVO.edges[edge[0], edge[1], 0]["name"] == "Autopista Vespucio Oriente":
			G_AVO.edges[edge[0], edge[1], 0]["highway"] = "motorway"

G = ox.graph_from_bbox(north, south, east, west, network_type="drive", clean_periphery=True, custom_filter='["highway"~"motorway|primary|secondary|tertiary"]')

nx.write_gpickle(G_AVO, "Santiago_con_AVO.gpickle")

nx.write_gpickle(G, "Santiago_sin_AVO.gpickle")