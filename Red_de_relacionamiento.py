import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import community  # Necesitas instalar esta biblioteca usando pip install python-louvain

# Cargar los datos desde el enlace de GitHub
url = "https://raw.githubusercontent.com/Cha0smagick/Fraud_Fake_database/main/Datos%20de%20prueba.csv"
df = pd.read_csv(url)

# Crear un grafo vacío
G = nx.Graph()

# Agregar nodos y conexiones al grafo
for index, row in df.iterrows():
    pais_ciudad = f"{row['País de emisión']} - {row['Ciudad']}"
    G.add_node(pais_ciudad, tipo='persona', fraude=row['Resultado'] == 'Fraude')
    for campo in df.columns:
        if campo != 'País de emisión' and campo != 'Ciudad' and campo != '¿Online o presencial?':
            G.add_edge(pais_ciudad, row[campo], tipo='conexión')

# Layout de la red
pos = nx.spring_layout(G, seed=42)

# Detección de comunidades usando el algoritmo de Louvain
partition = community.best_partition(G)

# Crear un mapeo de colores para las comunidades
colores_comunidades = [partition[nodo] for nodo in G.nodes()]

# Crear un mapeo de colores para los nodos relacionados con el fraude
fraude_colors = {node: 'red' if 'fraude' in G.nodes[node] else 'blue' for node in G.nodes()}

# Dibujar la red con colores distintivos
plt.figure(figsize=(12, 12))

# Estilo de nodos y etiquetas
node_labels = {node: node for node in G.nodes() if isinstance(node, str) and ' - ' in node}
nx.draw_networkx_nodes(G, pos, node_size=200, node_color=[fraude_colors[node] for node in G.nodes()], cmap=plt.cm.get_cmap('viridis', max(colores_comunidades) + 1), alpha=0.7)
nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8, font_color='black', font_weight='bold')

# Estilo de conexiones
edges = G.edges()
edge_colors = ['blue' if G[u][v]['tipo'] == 'conexión' else 'gray' for u, v in edges]
nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=edge_colors, width=1, alpha=0.7)

plt.title("Red de Personas y Documentos con Comunidades")
plt.axis('off')  # Ocultar ejes
plt.show()
