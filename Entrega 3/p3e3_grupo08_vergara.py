import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
import geopandas as gps

# gdf_ geodataframe
zonas_gdf = gps.read_file("eod.json")

colores_zonas = []
id_zonas_a_graficar = [316, 301, 302, 308, 309, 297, 314, 315, 298, 310]
zonas_seleccionadas = zonas_gdf[zonas_gdf.ID.isin(id_zonas_a_graficar)]

for idx, row in zonas_seleccionadas.iterrows():
	if id_zonas_a_graficar[0] == int(row["ID"]):
		colores_zonas.append("#FFB2B2")
	else:
		colores_zonas.append("#CDCDCD")



ox.config(use_cache=True, log_console=True)

north = -33.37
south = -33.44
east = -70.47
west = -70.56

G = ox.graph_from_bbox(north, south, east, west, network_type="drive", clean_periphery=True)

gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)
gdf_edges_seleccionados = gps.clip(gdf_edges, zonas_seleccionadas)

colores_calles = []
alphas_calles = []
for index, row in gdf_edges_seleccionados.iterrows():
	attr = row["highway"]
	if attr =="motorway":
		colores_calles.append("red")
		alphas_calles.append(1)
	elif attr =="secondary":
		colores_calles.append("yellow")
		alphas_calles.append(1)
	elif attr =="tertiary":
		colores_calles.append("blue")
		alphas_calles.append(1)
	elif attr =="primary":
		colores_calles.append("green")
		alphas_calles.append(1)
	elif attr =="residential":
		colores_calles.append("black")
		alphas_calles.append(1)
	else:
		colores_calles.append("white")
		alphas_calles.append(0)

fig, ax = plt.subplots(1, 1)
plt.suptitle(f"Zona Las Condes: {id_zonas_a_graficar[0:1]}; Vecinos: {id_zonas_a_graficar[1:]}\nRoberto Vergara C")
zonas_seleccionadas.plot(ax=ax, color=colores_zonas)
gdf_edges_seleccionados.plot(ax=ax, color=colores_calles, alpha=alphas_calles, linewidth=1)
#plt.savefig("p3e3_grupo08_vergara", dpi = 500, bbox_inches = 'tight')
plt.show()