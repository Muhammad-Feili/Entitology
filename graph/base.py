import networkx as nx
import pandas as pd
from dtl.graph_dtl import GraphDTL


class GraphBaseModule(object):
    def __init__(self, nodes=None, edges=None, read_from_db=False):
        self.nodes = nodes
        self.edges = edges

        if read_from_db:
            self.graph_dtl = GraphDTL()
            self.nodes = self.graph_dtl.get_nodes()
            self.edges = self.graph_dtl.get_edges


        elif not (self.nodes and self.edges):
            self.nodes = pd.read_csv(
                "static/sample_data/MajedAlasmariAP-nodes.csv")
            self.edges = pd.read_csv(
                "static/sample_data/MajedAlasmariAP-edges.csv")

    def get_graph(self):
        return self.DG

    def create(self):
        self.DG = nx.DiGraph()

        for idx, node in self.nodes.iterrows():

            node_id = node['Id']
            del node['Id']

            attributes = {node_id: node}

            self.DG.add_node(node_id)
            nx.set_node_attributes(self.DG, attributes)

        for idx, edge in self.edges.iterrows():
            source, target = edge['Source'], edge['Target']
            del edge['Source'], edge['Target']

            attributes = {(source, target): edge}

            self.DG.add_edge(source, target)
            nx.set_edge_attributes(self.DG, attributes)

    def show_random(self):
        import matplotlib.pyplot as plt

        plt.figure(figsize=(15, 12))
        nx.draw_random(self.DG)
        plt.show()
