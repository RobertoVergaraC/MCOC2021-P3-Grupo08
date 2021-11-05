import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math as math

G = nx.Graph()   #Graph asume bidireccionalidad en todos los arcos

G.add_node(0, pos=[1.0, 2.0])
G.add_node(1, pos=[4.0, 3.0])
G.add_node(2, pos=[1.0, 6.0])
G.add_node(3, pos=[7.0, 3.0])
G.add_node(4, pos=[10.0, 1.0])
G.add_node(5, pos=[0.0, 10.0])
G.add_node(6, pos=[4.0, 0.0])
G.add_node(7, pos=[5.0, 8.0])
G.add_node(8, pos=[9.0, 7.0])
G.add_node(9, pos=[8.0, 10.0])

G.add_edge(0, 1, lim_vel = 40)
G.add_edge(0, 2, lim_vel = 120)
G.add_edge(0, 6, lim_vel = 120)
G.add_edge(1, 2, lim_vel = 40)
G.add_edge(1, 3, lim_vel = 60)
G.add_edge(1, 7, lim_vel = 40)
G.add_edge(2, 5, lim_vel = 40)
G.add_edge(3, 4, lim_vel = 60)
G.add_edge(3, 6, lim_vel = 40)
G.add_edge(3, 7, lim_vel = 60)
G.add_edge(3, 8, lim_vel = 40)
G.add_edge(4, 6, lim_vel = 120)
G.add_edge(4, 8, lim_vel = 120)
G.add_edge(5, 7, lim_vel = 120)
G.add_edge(7, 9, lim_vel = 60)
G.add_edge(8, 9, lim_vel = 60)


pos = nx.get_node_attributes(G, "pos")
labels = nx.get_edge_attributes(G, "lim_vel")

colores = []
edgelist = []
for ni, nf, data in G.edges(data=True):
	if data["lim_vel"] == 120:
		colores.append("gray")
	elif data["lim_vel"] == 60:
		colores.append("green")
	elif data["lim_vel"] == 40:
		colores.append("saddlebrown")
	else:
		colores.append("k")

	edgelist.append((ni,nf))


fig1, ax = plt.subplots()
ax.grid(True)
ax.set_axisbelow(True)

nx.draw_networkx_nodes(G, pos=pos, ax=ax)
nx.draw_networkx_labels(G, pos=pos)
nx.draw_networkx_edges(G, pos, edgelist=edgelist, edge_color=colores, width=2)

ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
ax.set_ylabel('Y (km)')
ax.set_xlabel('X (km)')
plt.xticks([0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0],[0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0])
plt.yticks([0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0],[0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0])

plt.savefig("fig1", dpi = 300, bbox_inches = 'tight')
plt.show()



#Ahora definimos rutas con su tiempo de viaje

def distancia(nodo1, nodo2):
	 poss = nx.get_node_attributes(G, "pos")
	 dist1 = poss[nodo1]
	 dist2 = poss[nodo2]

	 return math.dist(dist1, dist2)

ruta01 = nx.dijkstra_path(G, source=0, target=9, weight = "lim_vel")
ruta02 = nx.dijkstra_path(G, source=4, target=5, weight = "lim_vel")
ruta03 = nx.dijkstra_path(G, source=0, target=4, weight = "lim_vel")

tiempo_viaje_01 = 0.
tiempo_viaje_02 = 0.
tiempo_viaje_03 = 0.
Nparadas = [len(ruta01), len(ruta02), len(ruta03)]

for j in range(len(Nparadas)):
	for i in range(Nparadas[j]-1):
		if j + 1 == 1:
			parada_i = ruta01[i]
			parada_f = ruta01[i+1]
			tiempo_viaje_tramo_i = (distancia(parada_i, parada_f)*1)/G.edges[parada_i, parada_f]["lim_vel"]
			tiempo_viaje_01 += tiempo_viaje_tramo_i
		elif j + 1 == 2:
			parada_i = ruta02[i]
			parada_f = ruta02[i+1]
			tiempo_viaje_tramo_i = (distancia(parada_i, parada_f)*1)/G.edges[parada_i, parada_f]["lim_vel"]
			tiempo_viaje_02 += tiempo_viaje_tramo_i
		elif j + 1 == 3:
			parada_i = ruta03[i]
			parada_f = ruta03[i+1]
			tiempo_viaje_tramo_i = (distancia(parada_i, parada_f)*1)/G.edges[parada_i, parada_f]["lim_vel"]
			tiempo_viaje_03 += tiempo_viaje_tramo_i

# print(f"Tiempo de Viaje ruta 01 = {np.round(tiempo_viaje_01, 2)} [hrs], lo que corresponde a {np.round(tiempo_viaje_01*60, 2)} [min]")
# print(f"Tiempo de Viaje ruta 02 = {np.round(tiempo_viaje_02, 2)} [hrs], lo que corresponde a {np.round(tiempo_viaje_02*60, 2)} [min]")
# print(f"Tiempo de Viaje ruta 03 = {np.round(tiempo_viaje_03, 2)} [hrs], lo que corresponde a {np.round(tiempo_viaje_03*60, 2)} [min]")

#Ahora definimos colores y ancho de las rutas

colores01 = []
edgelist01 = []
width01 = []
for ni, nf in G.edges:
	if ni in ruta01 and nf in ruta01:
		colores01.append("r")
		width01.append(5)
	else:
		colores01.append("gray")
		width01.append(1)
	edgelist01.append((ni,nf))

colores02 = []
edgelist02 = []
width02 = []
for ni, nf in G.edges:
	if ni in ruta02 and nf in ruta02:
		colores02.append("r")
		width02.append(5)
	else:
		colores02.append("gray")
		width02.append(1)
	edgelist02.append((ni,nf))

colores03 = []
edgelist03 = []
width03 = []
for ni, nf in G.edges:
	if ni in ruta03 and nf in ruta03:
		colores03.append("r")
		width03.append(5)
	else:
		colores03.append("gray")
		width03.append(1)
	edgelist03.append((ni,nf))



#Por último graficamos!

fig2, ax = plt.subplots()
ax.grid(True)
ax.set_axisbelow(True)

nx.draw_networkx_nodes(G, pos=pos, ax=ax)
nx.draw_networkx_labels(G, pos=pos)
nx.draw_networkx_edges(G, pos, edgelist=edgelist01, edge_color=colores01, width=width01)

ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
ax.set_ylabel('Y (km)')
ax.set_xlabel('X (km)')
plt.xticks([0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0],[0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0])
plt.yticks([0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0],[0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0])

plt.savefig("fig2", dpi = 300, bbox_inches = 'tight')
plt.show()



fig3, ax = plt.subplots()
ax.grid(True)
ax.set_axisbelow(True)

nx.draw_networkx_nodes(G, pos=pos, ax=ax)
nx.draw_networkx_labels(G, pos=pos)
nx.draw_networkx_edges(G, pos, edgelist=edgelist02, edge_color=colores02, width=width02)

ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
ax.set_ylabel('Y (km)')
ax.set_xlabel('X (km)')
plt.xticks([0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0],[0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0])
plt.yticks([0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0],[0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0])

plt.savefig("fig3", dpi = 300, bbox_inches = 'tight')
plt.show()



fig4, ax = plt.subplots()
ax.grid(True)
ax.set_axisbelow(True)

nx.draw_networkx_nodes(G, pos=pos, ax=ax)
nx.draw_networkx_labels(G, pos=pos)
nx.draw_networkx_edges(G, pos, edgelist=edgelist03, edge_color=colores03, width=width03)

ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
ax.set_ylabel('Y (km)')
ax.set_xlabel('X (km)')
plt.xticks([0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0],[0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0])
plt.yticks([0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0],[0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0])

plt.savefig("fig4", dpi = 300, bbox_inches = 'tight')
plt.show()