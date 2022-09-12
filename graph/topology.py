import networkx as nx
from graph.base import GraphBaseModule


class TopologyModule(GraphBaseModule):
    def __init__(self, DG=None):
        self.DG = DG
        if not self.DG:
            super(TopologyModule, self).__init__()
            self.create()

    def mutuals(self, node: str = None, depth_limit: int = None):
        mutual_graph = nx.Graph()

        if depth_limit is None:
            nodes = list(self.DG.nodes())
            num_nodes = len(nodes)

            for i in range(num_nodes):
                for j in range(i+1, num_nodes):
                    if self.DG.has_edge(nodes[i], nodes[j]) and self.DG.has_edge(nodes[j], nodes[i]):
                        mutual_graph.add_edge(nodes[i], nodes[j])

            return mutual_graph

        else:
            not_visited = list()
            not_visited.append(node)

            depth = 0
            while len(not_visited) != 0:
                depth += 1
                current_node = not_visited.pop(0)
                for (source, target) in self.DG.edges(current_node):
                    if self.DG.has_edge(target, source):
                        not_visited.append(target)
                        mutual_graph.add_edge(source, target)

                if depth == depth_limit:
                    break

            return mutual_graph

    def neighbourhood_depth(self, node, neighbour_depth):
        neighbours_graph = nx.DiGraph()
        for source, target in nx.bfs_edges(self.DG, node, depth_limit=neighbour_depth):
            neighbours_graph.add_edge(source, target)

            edge_attributes = {(source, target): self.DG[source][target]}
            nx.set_edge_attributes(neighbours_graph, edge_attributes)

            source_node_attributes = {source: self.DG.nodes(data=True)[source]}
            target_node_attributes = {target: self.DG.nodes(data=True)[target]}

            nx.set_node_attributes(neighbours_graph, source_node_attributes)
            nx.set_node_attributes(neighbours_graph, target_node_attributes)

        return neighbours_graph

        #         neighbours_graph = nx.DiGraph()

        #         visited = set()
        #         not_visited = list()
        #         not_visited.append(node)

        #         depth = 0
        #         while len(not_visited) != 0:
        #             depth += 1
        #             current_node = not_visited.pop(0)
        #             for source, target in self.DG.edges(current_node):
        #                 if target not in visited:
        #                     not_visited.append(target)
        #                     neighbours_graph.add_edge(source, target)

        #             visited.add(current_node)

        #             if depth == neighbor_depth:
        #                 break

        #         return neighbours_graph
