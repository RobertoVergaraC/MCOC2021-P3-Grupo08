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
for incremento in incrementos:
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
			for i_parada in range(Nparadas-1):
				o = path[i_parada]
				d = path[i_parada + 1]
				flujo_antes = G.edges[o, d]["flujo"]
				G.edges[o, d]["flujo"] += incremento*demanda_objetivo
				G.edges[o, d]["costo"] = G.edges[o, d]["fcosto"](G.edges[o, d]["flujo"])

			OD[key] -= incremento*demanda_objetivo
```  

Para realizar el algoritmo, en primer lugar, es importante definir un diccionario con una clave de tiplo tupla en donde el primer elemento corresponde al origen, el segundo al destino y el valor de esta clave, será la demanda. Luego, realizamos una copia de este diccionario, ya que el primer diccionario será al que se le irá quitando la demanda cada vez que se asigna y el segundo tendrá los valores de demanda objetivos (demanda total).  

Posteriormente definimos la lista incrementos, la cual corresponde a porcentajes, los cuales multiplicados por la demanda objetivo, serán los valores que se incrementaran en los flujos y dismunuirán en el diccionario origen destino (hasta tener demandas todas iguales a 0).  

A continuación se da inicio al algoritmo; 
1) Recorremos incremento, ya que según esos valores es cuanto se incrementará en flujos. Lógicamente la suma de los valores de incrementos serán iguales a 1 (quitamos el 100% de la demanda).
2) Recorremos el diccionario en donde identificamos nuestro par origen-destino, la demanda actual (la cual por cada vez que se recorre es menor) y la demanda objetivo (demanda total). Importante señalar que el algoritmo va agregando flujo en cada par OD uno a la vez, es decir, agrega flujo con el incremento para el par AC, luego para el par AD hasta terminar el diccionario y luego vuelve a AC para seguir agregando flujo según el segundo valor del incremento. De esta manera el resultado de Wardrop es mucho más efectivo, ya que va realizando todos los pares OD al "mismo tiempo".
3) A continuación, definimos la condición de que si la demanda actual todavía es mayor a 0, entonces se calcula la ruta con menor costo (esta se calcula según el atributo "costo", el cual parte con un valor inicial considerando todos los flujos iguales a 0) y se procede a recorrer los arcos de esta para ir agregando el flujo (+=incremento * demanda) y modificando los costos según este último (al incrementar el flujo, el costo lo va haciendolo de manera paralela según su función definida por enunciado).
4) Por último, todo el flujo agregado a los diferentes arcos de la ruta con menor costo son retirados del diccionario de matriz origen destino.
5) Se repite todo el proceso hasta que todas las demandas sean iguales a 0.  

Al ir incrementando los flujos con relación a porcentajes de la demanda, la solución encontrada tiene valores más exactos, ya que según cuantos viajes haya de un origen a un destino, sus rutas posibles pasan a ser más relevantes, esto es lógico, porque tienen una mayor cantidad de flujo.  

Por último, cabe destacar lo mencionado en el punto 2), ya que al ir agregando flujos recorriendo toda la matriz OD, encontramos un valor mucho más exacto que al terminar un par OD y luego seguir con el siguiente, pues de esta forma si se toman en cuentas las externalidades que surgen de otros viajes que pueden afectar a otros pares OD.  

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

| Flujos | Costos |
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

Aquí se trabajo con la variable "tabla" la cual es donde se van incluyendo los valores respectivos a cada una de las rutas mínimas encontradas. En una primera instancia, se encontro la ruta mínima por medio de la función dijkstra_path, para luego calcular el costo de dicha ruta. Una vez encontrados estas varibables, se comenzó a comparar el costo de cada una de las rutas encontradas con una tolerancia de un decimal, es decir que se consideran que los costos son iguales si es que son iguales hasta el primer decimal. Todas las rutas que tengan el mismo costo de la ruta mínima encontrada originalmente, se consideraron como rutas mínimas y fueron presentadas en la tabla. Finalmente se guardan los valores de los costos y errores de cada una de estas rutas y se presentaron en la variable "TABLA" que es presentada en la imagen de arriba. Además, cabe agregar que los costos finales de las rutas seleccionadas se encontraron realizando el promedio de todos los costos, así, se llega a un valor incluso más preciso, ya que el algoritmo para encontrar los costos siempre encontrará una ruta levemente más "cara" y una levemente más "barata", y al calcular el promedio se encuentra una solución más exacta.  

Se puede ver en la tabla que todos los errores son muy bajos, menores al 0,01%, considerando los valores entregados por la pauta del control y por esto mismo se puede decir que todos los costos de estas rutas mínimas son equivalentes.  

De esta manera, se valida el equilibrio de Wardrop, donde todas las rutas mínimas tienen el mismo costo.


## Entrega 5

En el siguiente gráfico se muestran las zonas seleccionadas para el estudio, con las calles importantes dentro de estas. Se puede evidenciar que en naranjo se encuentran las calles clasificadas como "motorway", en amarillo las "primary", en verde las "secondary", en azul las "tertiary" y en rojo donde iría la Autopista Vespucio Oriente, conocida como AVO.

![AVO](https://github.com/RobertoVergaraC/MCOC2021-P3-Grupo08/blob/main/Entrega%205/Avenida%20%C3%81merico%20Vespucio%20Oriente.png)

### ¿Cómo seleccionó las zonas a incluir?

En pocas palabras, se realizó "un waze" que identificara si entre 2 zonas AVO era una ruta válida.  
Explicando un poco más; a partir de las demandas entregadas por enunciado se seleccionaron todas las zonas de interés. Luego, a cada zona se le calculó el nodo más cercano al punto representativo de la zona y se procedió a analizar las rutas con los costos más "baratos" (nx.all_shortest_path). Para realizar esto, era necesario definir un "peso" para identificar las rutas menos costosas. Este peso seguía el comportamiento entregado por enunciado, para esto, se realizó una función la cual contemplaba que no había flujo (suponiendo como casos iniciales) y que las rutas de la Kennedy y Autopista Central tenían distancias más grandes de las reales, para así forzar el uso de AVO en más zonas.  
Una vez conocidas las rutas menos costosas forzando el uso de AVO, simplemente se observaba si la ruta pasaba por AVO y si es que era así, se guardaban las zonas de origen y destino como zonas de interés.  
Lógicamente las zonas identificadas como de interés fueron las seleccionadas.  

### ¿Cuántas zonas quedaron seleccionadas son?

En total según nuestro sistema para seleccionar las zonas, se consideran 455 zonas. Estás zonas fueron escogidas con los criterios mencionados anteriormente.  
A continuación se puede observar una imagen clara de las zonas finales de interés:  

![Zonas de Interés](https://github.com/RobertoVergaraC/MCOC2021-P3-Grupo08/blob/main/Entrega%205/ZONAS%20SELECCIONADAS.png)  

### ¿Cuántos viajes deberá asignar?

La cantidad de viajes se asignarán según los viajes que se encuentren en la matriz de Origen y Destino de Santiago entregada por la documentación del curso, considerando todos los viajes que se dan entre las 455 zonas seleccionadas para este análisis. Sería un total de 365735 viajes aproximadamente.  

### ¿Cuales son los pares OD que espera Ud. que generen mayor flujo en AVO?

Nosotros creemos que los pares OD o los arcos que generen mayor flujo van a ser las zonas que esten cercanas a AVO pero que tengan que irse hacia zonas limítrofes de Santiago o viceversa, es decir que las que tengan que atravesar Santiago y que AVO sea el camino más recto o directo hacia su destino. Consideramos que de la zona correspondiente a Maipú hacia la zona de Las Condes, o desde la zona de Huachuraba hasta la zona de Las Condes, siendo estos pares de origen y destino conectando zonas dormitorio con zonas empresariales o de oficinas.  

#### *COMENTARIOS GENERALES: En esta entrega se presentan 3 archivos .py, el primero (p3e5_cargar) simplemente carga el mapa de santiago, agrega como "motorway" a AVO y lo guarda en versión .gpickle. Luego el segundo archivo .py (p3e5_ejecutar) realiza el algoritmo explicado en la segunda pregunta entregando además un nuevo archivo .csv con las zonas de interés con sus respectivas demandas. Por último, el archivo p3e5.py entrega toda la información pedida por enunciado, se imprime el mapa con las zonas seleccionadas en gris y mostrando las calles con sus respectivos colores, además entrega la demanda total y la cantidad de zonas encontradas en p3e5_ejecutar.*  

## Entrega 6  

#### INFORME