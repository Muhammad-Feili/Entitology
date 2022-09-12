import networkx as nx
from graph.base import GraphBaseModule


# compute on database
class MetricModule(GraphBaseModule):
    def __init__(self, DG=None):
        self.DG = DG
        if not self.DG:
            super(MetricModule, self).__init__()
            self.create()

    def eigen_centrality(self):
        eigen_centrality = nx.eigenvector_centrality(self.DG)
        return eigen_centrality

    def degree(self, node: str):
        outdeg = self.DG.out_degree(node)
        indeg = self.DG.in_degree(node)

        degree = {"outDegree": outdeg, "inDegree": indeg, "totalDegree": indeg+outdeg}
        return degree

    def weighted_degree(self, node: str, weight: str = "Weight"):
        outdeg = self.DG.out_degree(node, weight=weight)
        indeg = self.DG.in_degree(node, weight=weight)

        degree = {"outDegree": outdeg, "inDegree": indeg, "totalDegree": indeg+outdeg}
        return degree
