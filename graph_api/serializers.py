import json


class QuerySerializer:
    def __init__(self, DG):
        self.DG = DG

    def serialize(self, features_filters=None, settings=None, center_node_id=None, limit=None, has_access=None):
        query_result = dict()

        query_result["graph"] = self.create_graph_interface(
            features_filters=features_filters, settings=settings, center_node_id=center_node_id)
        query_result["user"] = self.create_user_data(limit, has_access)

        return json.dumps(query_result)

    def create_graph_interface(self, node_new_feature=None, edge_new_feature=None, features_filters=None, settings=None, center_node_id=None):
        nodes = dict()
        if node_new_feature:
            for node, features in self.DG.nodes(data=True):
                features = dict(features).update(node_new_feature)
                nodes[node] = features
        else:
            nodes = {node: features for node,
                     features in self.DG.nodes(data=True)}

        edges = dict()
        if edge_new_feature:
            for source, target, features in self.DG.edges(data=True):
                features = dict(features).update(edge_new_feature)
                features["from"], features["to"] = source, target
                edges[features["Id"]] = features

        else:
            for source, target, features in self.DG.edges(data=True):
                features["from"], features["to"] = source, target
                edges[features["Id"]] = features

        meta = self.create_graph_meta(
            features_filters, settings, center_node_id)
        return {"nodes": nodes,
                "edges": edges,
                "meta": meta}

    def create_graph_meta(self, features_filters=None, settings=None, center_node_id=None):
        settings = self.create_settings(settings)
        filters = self.create_filters(features_filters)

        return {"settings": settings,
                "filters": filters,
                "centerNodeId": center_node_id}

    def create_settings(self, settings=None):
        serialized_settings = dict()
        serialized_settings["layout"] = {"enable": True,
                                         "editable": True,
                                         "type": "enum-eq",
                                         "options": ['forceatlas2', 'force'],
                                         "value": 'forceatlas2'}

        serialized_settings["nodeLabelStyle"] = {"enable": True,
                                                 "editable": True,
                                                 "type": "other",
                                                 "value": {"fixed": True, "size": 10, "color": "blue"}}

        return serialized_settings

    def create_filters(self, features_filters=None):
        serilized_filters = dict()
        serilized_filters["nodeMetrics"] = {"enable": True,
                                            "editable": True,
                                            "type": "object",
                                            "children": features_filters}

        serilized_filters["depth"] = {"enable": True,
                                      "editable": True,
                                      "type": "enum-leq",
                                      "options": [1, 2, 3],
                                      "value": 3}

        return serilized_filters

    def create_user_data(self, limit=None, has_access=None):
        return {"nodeCountLimit": limit,
                "hasAccess": has_access}
