import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.title("Social Network Analysis - Interactive Graph Visualization")

# Load CSV file
csv_path = "symmetric_matrix.csv"
df_corrected = pd.read_csv(csv_path, index_col=0)

# Extract country information from node labels
nodes = df_corrected.index.tolist()
countries = {node: node.split('(')[-1].strip(')') for node in nodes}

# Create a mapping of countries to unique colors
unique_countries = list(set(countries.values()))
color_map = {country: f"rgba({np.random.randint(0,255)},{np.random.randint(0,255)},{np.random.randint(0,255)},0.8)" 
             for country in unique_countries}

# Create graph
G = nx.Graph()

# Add nodes with country-based coloring
for node in nodes:
    G.add_node(node, color=color_map[countries[node]], team=countries[node])

# Add edges based on the adjacency matrix
for i, node1 in enumerate(nodes):
    for j, node2 in enumerate(nodes):
        if df_corrected.iloc[i, j] > 0 and i < j:  # To avoid duplicate edges
            G.add_edge(node1, node2)

# Get positions for nodes using force-directed layout
pos = nx.spring_layout(G, seed=42)

# Extract edge and node trace data for Plotly visualization
edge_x, edge_y = [], []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

tedge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.5, color='#888'),
                        hoverinfo='none', mode='lines')

node_x, node_y, node_color, node_text = [], [], [], []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    node_color.append(G.nodes[node]['color'])
    node_text.append(node)  # Display node label on hover

node_trace = go.Scatter(
    x=node_x, y=node_y, mode='markers+text', hoverinfo='text',
    marker=dict(size=10, color=node_color, line=dict(width=2)),
    text=node_text, textposition="top center"
)

# Create legend traces for each country
legend_traces = []
for country, color in color_map.items():
    legend_traces.append(go.Scatter(
        x=[None], y=[None], mode='markers',
        marker=dict(size=10, color=color, line=dict(width=2)),
        name=country
    ))

# Create the interactive network graph
fig = go.Figure(data=[edge_trace, node_trace] + legend_traces)
fig.update_layout(showlegend=True, hovermode='closest',
                  margin=dict(b=0, l=0, r=0, t=0),
                  xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                  yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))

# Show interactive plot in Streamlit
st.plotly_chart(fig)
