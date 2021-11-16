# MCOC2021-P3-Grupo08
Proyecto 3 MCOC

# Grupo 08 

## Integrantes:

* Carmen Benavente Vicuña
* Roberto Alfonso Vergara Cubillos

## Entrega 2

| Figura | Imagen |
| ------------- | ------------- |
| fig1 (Original) | ![fig1](https://github.com/RobertoVergaraC/MCOC2021-P3-Grupo08/blob/main/Entrega%202/fig1.png) |
| fig2 (0 &rightarrow; 9) | ![fig2](https://github.com/RobertoVergaraC/MCOC2021-P3-Grupo08/blob/main/Entrega%202/fig2.png) |
| fig3 (4 &rightarrow; 5) | ![fig3](https://github.com/RobertoVergaraC/MCOC2021-P3-Grupo08/blob/main/Entrega%202/fig3.png) |
| fig4 (0 &rightarrow; 4) | ![fig4](https://github.com/RobertoVergaraC/MCOC2021-P3-Grupo08/blob/main/Entrega%202/fig4.png) |  

## Entrega 3
| INTEGRANTE | MAPA |
| ------------- | ------------- |
| Carmen Benavente Vicuña | ![p3e3_grupo08_benavente](https://user-images.githubusercontent.com/62263342/141379206-a2083e09-35aa-4f76-9882-9393e52d5b22.png) |
| Roberto Alfonso Vergara Cubillos | ![MapaRoberto](https://github.com/RobertoVergaraC/MCOC2021-P3-Grupo08/blob/main/Entrega%203/p3e3_grupo08_vergara.png) |  

## Entrega 4

### Código

#### Creación funciones de costo, grafo, nodos y arcos no bidireccionales
```python
r = lambda f: 10 + f/120
s = lambda f: 14 + 3*f/240 
t = lambda f: 10 + f/240
u = lambda f: 14 + 3*f/240 
v = lambda f: 10 + f/120
w = lambda f: 14 + 3*f/240 
x = lambda f: 10 + f/240
y = lambda f: 14 + 3*f/240 
z = lambda f: 10 + f/120

G = nx.DiGraph()

G.add_node("A", pos = (0, 10))
G.add_node("B", pos = (0, 5))
G.add_node("C", pos = (5, 5))
G.add_node("D", pos = (5, 0))
G.add_node("E", pos = (10, 10))
G.add_node("G", pos = (10, 5))

G.add_edge("A","B", fcosto=r, flujo=0., costo=10., label = "r: 10 + f/120")
G.add_edge("A","C", fcosto=s, flujo=0., costo=14., label = "s: 14 + 3*f/240")
G.add_edge("B","C", fcosto=t, flujo=0., costo=10., label = "t: 10 + f/240")
G.add_edge("B","D", fcosto=u, flujo=0., costo=14., label = "u: 14 + 3*f/240")
G.add_edge("C","E", fcosto=w, flujo=0., costo=10., label = "w: 14 + 3*f/240")
G.add_edge("C","G", fcosto=x, flujo=0., costo=14., label = "x: 10 + f/240")
G.add_edge("D","C", fcosto=v, flujo=0., costo=10., label = "v: 10 + f/120")
G.add_edge("D","G", fcosto=y, flujo=0., costo=14., label = "y: 14 + 3*f/240")
G.add_edge("G","E", fcosto=z, flujo=0., costo=10., label = "z: 10 + f/120")
```

#### Graficamos grafo propuesto
```python
plt.figure(1)
ax1 = plt.subplot(111)
pos = nx.get_node_attributes(G, "pos")
plt.suptitle("Grafo Problema")
nx.draw(G, pos = pos, with_labels=True, font_weight="bold")
labels = nx.get_edge_attributes(G, "label")
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.show()
```
![GrafoEntrega4](https://github.com/RobertoVergaraC/MCOC2021-P3-Grupo08/blob/main/Entrega%204/Grafo%20Entrega%204.png)

#### Creamos Matriz OD y realizamos algoritmo de Wardrop
```python
OD = {
	("A","C") : 1100.,
	("A","D") : 1110.,
	("A","E") : 1020.,
	("B","C") : 1140.,
	("B","D") : 1160.,
	("C","E") : 1170.,
	("C","G") : 1180.,
	("D","C") : 350.,
	("D","E") : 1190.,
	("D","G") : 1200.
}

OD_target = OD.copy()

incrementos = [0.05]*18 + [0.01]*9 + [0.001]*9 + [0.0001]*9 + [0.00001]*9 + [0.000001]*10
#print(sum(incrementos))
for incremento in incrementos:
	#se_asigno_demanda = False

	for key in OD:

		origen = key[0]
		destino = key[1]
		demanda_actual = OD[key]
		demanda_objetivo = OD_target[key]

		if demanda_actual > 0.:
			#Ruta mínima
			path = nx.dijkstra_path(G, origen, destino, weight="costo")

			#Incrementar flujo en la ruta mínima
			Nparadas = len(path)
			p_total = 0
			for i_parada in range(Nparadas-1):
				o = path[i_parada]
				d = path[i_parada + 1]
				flujo_antes = G.edges[o, d]["flujo"]
				G.edges[o, d]["flujo"] += incremento*demanda_objetivo
				G.edges[o, d]["costo"] = G.edges[o, d]["fcosto"](G.edges[o, d]["flujo"])

			OD[key] -= incremento*demanda_objetivo
```  

EXPLICACIÓN ALGORITMOOOOO

#### Graficamos flujo y costo por arcos encontrados
```python
plt.figure(1)
pos = nx.get_node_attributes(G, "pos")
plt.suptitle("Flujo")
nx.draw(G, pos = pos, with_labels=True, font_weight="bold")
labels = nx.get_edge_attributes(G, "flujo")
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

plt.figure(2)
pos = nx.get_node_attributes(G, "pos")
plt.suptitle("Costo")
nx.draw(G, pos = pos, with_labels=True, font_weight="bold")
labels = nx.get_edge_attributes(G, "costo")
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

plt.show()
```

| Flujo | Costos |
| ------------- | ------------- |
| ![flujo](https://github.com/RobertoVergaraC/MCOC2021-P3-Grupo08/blob/main/Entrega%204/Flujo%20Entrega%204.png) | ![costos](https://github.com/RobertoVergaraC/MCOC2021-P3-Grupo08/blob/main/Entrega%204/Costos%20Entrega%204.png) |

### Validación equilibrio de Wardrop
```python
TABLA = []

print(f"Costos\n")
for key in OD:
	origen = key[0]
	destino = key[1]
	tabla = []
	tabla.append(f"{origen}{destino}")

	paths = nx.all_simple_paths(G, origen, destino)
	path = nx.dijkstra_path(G, origen, destino, weight="costo")

	costo_min = 0
	Nparada_min = len(path)
	for j_parada in range(Nparada_min-1):
		o = path[j_parada]
		d = path[j_parada + 1]
		costo_min += G.edges[o, d]["costo"]

	costos_seleccionados = []
	paths_seleccionados = []
	errores_seleccionados = []
	for i in paths:
		costo = 0
		Nparadas = len(i)

		for i_parada in range(Nparadas-1):
			o = i[i_parada]
			d = i[i_parada + 1]
			costo += G.edges[o, d]["costo"]

		if int(costo_min*10) == int(costo*10):
			costos_seleccionados.append(costo)
			paths_seleccionados.append(i)
			if costo_min != costo:
				error = (abs(costo-costo_min)/costo_min)*100
				errores_seleccionados.append(error)
			else:
				errores_seleccionados.append(0)
	tabla.append(paths_seleccionados)
	tabla.append(np.average(costos_seleccionados))
	if len(errores_seleccionados)<=1:
		tabla.append(f"{errores_seleccionados[0]}%")
	else:
		tabla.append(f"{sum(errores_seleccionados)/(len(errores_seleccionados)-1)}%")
	TABLA.append(tabla)

print(tabulate(TABLA, headers=['ORIGEN - DESTINO', 'PATHS SELECCIONADOS', 'COSTOS', 'ERROR COSTOS'], tablefmt='grid'))
```

![Validacion_Wardrop](https://github.com/RobertoVergaraC/MCOC2021-P3-Grupo08/blob/main/Entrega%204/Validaci%C3%B3n%20Wardrop%20Entrega%204.png)  

EXPLICACIÓN VALIDACIÓN

