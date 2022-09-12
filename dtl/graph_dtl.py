from dtl.dao.graph_dao import GraphDao
from runtime_config import RuntimConfig


class GraphDTL:
    def __init__(self):
        self.dao = GraphDao()

    def get_nodes(self, node_table=RuntimConfig.NODE_TABLE_NAME):
        query = "SELECT * FROM {}".format(node_table)
        return self.dao.get_rows(query)

    def get_edges(self, edge_table=RuntimConfig.EDGE_TABLE_NAME):
        query = "SELECT * FROM {}".format(edge_table)
        return self.dao.get_rows(query)
