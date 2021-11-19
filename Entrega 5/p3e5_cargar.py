import networkx as nx
import osmnx as ox
import numpy as np
from math import sin, cos, sqrt, atan2, radians
from shapely.geometry import LineString

def length(lat1, lon1, lat2, lon2):
	lat1 = radians(lat1)
	lon1 = radians(lon1)
	lat2 = radians(lat2)
	lon2 = radians(lon2)

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	return 6373*c

ox.config(use_cache=True, log_console=True)

north = -33.0
south = -34.0
east = -70.2
west = -71.6

G = ox.graph_from_bbox(north, south, east, west, network_type="drive", clean_periphery=True, custom_filter='["highway"~"motorway|primary|secondary|tertiary"]')

#CREAMOS AVO!
G.add_edge(479444375, 479444385, osmid=np.nan, oneway=False, lanes=4, ref=np.nan, name="Américo Vespucio Oriente", highway="motorway", maxspeed=80, length=length(G.nodes[479444375]["x"],G.nodes[479444375]["y"],G.nodes[479444385]["x"],G.nodes[479444385]["y"]), geometry=LineString([(G.nodes[479444375]["x"],G.nodes[479444375]["y"]),(G.nodes[479444385]["x"],G.nodes[479444385]["y"])]), bridge=np.nan, width=np.nan, tunnel=np.nan, access=np.nan, junction=np.nan)
G.add_edge(479444385, 13880414, osmid=np.nan, oneway=False, lanes=4, ref=np.nan, name="Américo Vespucio Oriente", highway="motorway", maxspeed=80, length=length(G.nodes[479444385]["x"],G.nodes[479444385]["y"],G.nodes[13880414]["x"],G.nodes[13880414]["y"]), geometry=LineString([(G.nodes[479444385]["x"], G.nodes[479444385]["y"]),(G.nodes[13880414]["x"], G.nodes[13880414]["y"])]), bridge=np.nan, width=np.nan, tunnel=np.nan, access=np.nan, junction=np.nan)
G.add_edge(13880414, 1703795253, osmid=np.nan, oneway=False, lanes=4, ref=np.nan, name="Américo Vespucio Oriente", highway="motorway", maxspeed=80, length=length(G.nodes[13880414]["x"],G.nodes[13880414]["y"],G.nodes[1703795253]["x"],G.nodes[1703795253]["y"]), geometry=LineString([(G.nodes[13880414]["x"], G.nodes[13880414]["y"]),(G.nodes[1703795253]["x"], G.nodes[1703795253]["y"])]), bridge=np.nan, width=np.nan, tunnel=np.nan, access=np.nan, junction=np.nan)
G.add_edge(1703795253, 254034293, osmid=np.nan, oneway=False, lanes=4, ref=np.nan, name="Américo Vespucio Oriente", highway="motorway", maxspeed=80, length=length(G.nodes[1703795253]["x"],G.nodes[1703795253]["y"],G.nodes[254034293]["x"],G.nodes[254034293]["y"]), geometry=LineString([(G.nodes[1703795253]["x"], G.nodes[1703795253]["y"]),(G.nodes[254034293]["x"], G.nodes[254034293]["y"])]), bridge=np.nan, width=np.nan, tunnel=np.nan, access=np.nan, junction=np.nan)
G.add_edge(254034293, 15073520, osmid=np.nan, oneway=False, lanes=4, ref=np.nan, name="Américo Vespucio Oriente", highway="motorway", maxspeed=80, length=length(G.nodes[254034293]["x"],G.nodes[254034293]["y"],G.nodes[15073520]["x"],G.nodes[15073520]["y"]), geometry=LineString([(G.nodes[254034293]["x"], G.nodes[254034293]["y"]),(G.nodes[15073520]["x"], G.nodes[15073520]["y"])]), bridge=np.nan, width=np.nan, tunnel=np.nan, access=np.nan, junction=np.nan)
G.add_edge(15073520, 13880337, osmid=np.nan, oneway=False, lanes=4, ref=np.nan, name="Américo Vespucio Oriente", highway="motorway", maxspeed=80, length=length(G.nodes[15073520]["x"],G.nodes[15073520]["y"],G.nodes[13880337]["x"],G.nodes[13880337]["y"]), geometry=LineString([(G.nodes[15073520]["x"], G.nodes[15073520]["y"]),(G.nodes[13880337]["x"], G.nodes[13880337]["y"])]), bridge=np.nan, width=np.nan, tunnel=np.nan, access=np.nan, junction=np.nan)
G.add_edge(13880337, 148849888, osmid=np.nan, oneway=False, lanes=4, ref=np.nan, name="Américo Vespucio Oriente", highway="motorway", maxspeed=80, length=length(G.nodes[13880337]["x"],G.nodes[13880337]["y"],G.nodes[148849888]["x"],G.nodes[148849888]["y"]), geometry=LineString([(G.nodes[13880337]["x"], G.nodes[13880337]["y"]),(G.nodes[148849888]["x"], G.nodes[148849888]["y"])]), bridge=np.nan, width=np.nan, tunnel=np.nan, access=np.nan, junction=np.nan)
G.add_edge(148849888, 1264487023, osmid=np.nan, oneway=False, lanes=4, ref=np.nan, name="Américo Vespucio Oriente", highway="motorway", maxspeed=80, length=length(G.nodes[148849888]["x"],G.nodes[148849888]["y"],G.nodes[1264487023]["x"],G.nodes[1264487023]["y"]), geometry=LineString([(G.nodes[148849888]["x"], G.nodes[148849888]["y"]),(G.nodes[1264487023]["x"], G.nodes[1264487023]["y"])]), bridge=np.nan, width=np.nan, tunnel=np.nan, access=np.nan, junction=np.nan)
G.add_edge(1264487023, 1818495760, osmid=np.nan, oneway=False, lanes=4, ref=np.nan, name="Américo Vespucio Oriente", highway="motorway", maxspeed=80, length=length(G.nodes[1264487023]["x"],G.nodes[1264487023]["y"],G.nodes[1818495760]["x"],G.nodes[1818495760]["y"]), geometry=LineString([(G.nodes[1264487023]["x"], G.nodes[1264487023]["y"]),(G.nodes[1818495760]["x"], G.nodes[1818495760]["y"])]), bridge=np.nan, width=np.nan, tunnel=np.nan, access=np.nan, junction=np.nan)
G.add_edge(1818495760, 1830996610, osmid=np.nan, oneway=False, lanes=4, ref=np.nan, name="Américo Vespucio Oriente", highway="motorway", maxspeed=80, length=length(G.nodes[1818495760]["x"],G.nodes[1818495760]["y"],G.nodes[1830996610]["x"],G.nodes[1830996610]["y"]), geometry=LineString([(G.nodes[1818495760]["x"], G.nodes[1818495760]["y"]),(G.nodes[1830996610]["x"], G.nodes[1830996610]["y"])]), bridge=np.nan, width=np.nan, tunnel=np.nan, access=np.nan, junction=np.nan)
G.add_edge(1830996610, 5059317755, osmid=np.nan, oneway=False, lanes=4, ref=np.nan, name="Américo Vespucio Oriente", highway="motorway", maxspeed=80, length=length(G.nodes[1830996610]["x"],G.nodes[1830996610]["y"],G.nodes[5059317755]["x"],G.nodes[5059317755]["y"]), geometry=LineString([(G.nodes[1830996610]["x"], G.nodes[1830996610]["y"]),(G.nodes[5059317755]["x"], G.nodes[5059317755]["y"])]), bridge=np.nan, width=np.nan, tunnel=np.nan, access=np.nan, junction=np.nan)
G.add_edge(5059317755, 240424226, osmid=np.nan, oneway=False, lanes=4, ref=np.nan, name="Américo Vespucio Oriente", highway="motorway", maxspeed=80, length=length(G.nodes[5059317755]["x"],G.nodes[5059317755]["y"],G.nodes[240424226]["x"],G.nodes[240424226]["y"]), geometry=LineString([(G.nodes[5059317755]["x"], G.nodes[5059317755]["y"]),(G.nodes[240424226]["x"], G.nodes[240424226]["y"])]), bridge=np.nan, width=np.nan, tunnel=np.nan, access=np.nan, junction=np.nan)
G.add_edge(240424226, 1225556658, osmid=np.nan, oneway=False, lanes=4, ref=np.nan, name="Américo Vespucio Oriente", highway="motorway", maxspeed=80, length=length(G.nodes[240424226]["x"],G.nodes[240424226]["y"],G.nodes[1225556658]["x"],G.nodes[1225556658]["y"]), geometry=LineString([(G.nodes[240424226]["x"], G.nodes[240424226]["y"]),(G.nodes[1225556658]["x"], G.nodes[1225556658]["y"])]), bridge=np.nan, width=np.nan, tunnel=np.nan, access=np.nan, junction=np.nan)
G.add_edge(1225556658, 1225556586, osmid=np.nan, oneway=False, lanes=4, ref=np.nan, name="Américo Vespucio Oriente", highway="motorway", maxspeed=80, length=length(G.nodes[1225556658]["x"],G.nodes[1225556658]["y"],G.nodes[1225556586]["x"],G.nodes[1225556586]["y"]), geometry=LineString([(G.nodes[1225556658]["x"], G.nodes[1225556658]["y"]),(G.nodes[1225556586]["x"], G.nodes[1225556586]["y"])]), bridge=np.nan, width=np.nan, tunnel=np.nan, access=np.nan, junction=np.nan)
G.add_edge(1225556586, 500326627, osmid=np.nan, oneway=False, lanes=4, ref=np.nan, name="Américo Vespucio Oriente", highway="motorway", maxspeed=80, length=length(G.nodes[1225556586]["x"],G.nodes[1225556586]["y"],G.nodes[500326627]["x"],G.nodes[500326627]["y"]), geometry=LineString([(G.nodes[1225556586]["x"], G.nodes[1225556586]["y"]),(G.nodes[500326627]["x"], G.nodes[500326627]["y"])]), bridge=np.nan, width=np.nan, tunnel=np.nan, access=np.nan, junction=np.nan)
G.add_edge(500326627, 253269320, osmid=np.nan, oneway=False, lanes=4, ref=np.nan, name="Américo Vespucio Oriente", highway="motorway", maxspeed=80, length=length(G.nodes[500326627]["x"],G.nodes[500326627]["y"],G.nodes[253269320]["x"],G.nodes[253269320]["y"]), geometry=LineString([(G.nodes[500326627]["x"], G.nodes[500326627]["y"]),(G.nodes[253269320]["x"], G.nodes[253269320]["y"])]), bridge=np.nan, width=np.nan, tunnel=np.nan, access=np.nan, junction=np.nan)
G.add_edge(253269320, 276087185, osmid=np.nan, oneway=False, lanes=4, ref=np.nan, name="Américo Vespucio Oriente", highway="motorway", maxspeed=80, length=length(G.nodes[253269320]["x"],G.nodes[253269320]["y"],G.nodes[276087185]["x"],G.nodes[276087185]["y"]), geometry=LineString([(G.nodes[253269320]["x"], G.nodes[253269320]["y"]),(G.nodes[276087185]["x"], G.nodes[276087185]["y"])]), bridge=np.nan, width=np.nan, tunnel=np.nan, access=np.nan, junction=np.nan)
G.add_edge(276087185, 376245268, osmid=np.nan, oneway=False, lanes=4, ref=np.nan, name="Américo Vespucio Oriente", highway="motorway", maxspeed=80, length=length(G.nodes[276087185]["x"],G.nodes[276087185]["y"],G.nodes[376245268]["x"],G.nodes[376245268]["y"]), geometry=LineString([(G.nodes[276087185]["x"], G.nodes[276087185]["y"]),(G.nodes[376245268]["x"], G.nodes[376245268]["y"])]), bridge=np.nan, width=np.nan, tunnel=np.nan, access=np.nan, junction=np.nan)
G.add_edge(376245268, 1939726851, osmid=np.nan, oneway=False, lanes=4, ref=np.nan, name="Américo Vespucio Oriente", highway="motorway", maxspeed=80, length=length(G.nodes[376245268]["x"],G.nodes[376245268]["y"],G.nodes[1939726851]["x"],G.nodes[1939726851]["y"]), geometry=LineString([(G.nodes[376245268]["x"], G.nodes[376245268]["y"]),(G.nodes[1939726851]["x"], G.nodes[1939726851]["y"])]), bridge=np.nan, width=np.nan, tunnel=np.nan, access=np.nan, junction=np.nan)


nx.write_gpickle(G, "Santiago_Grueso.gpickle")