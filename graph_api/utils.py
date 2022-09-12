class GraphUtils:
    @staticmethod
    def check_limitation(graph, user_access_limit):
        num_nodes = len(graph.nodes())

        if num_nodes <= user_access_limit:
            return True
        else:
            return False
