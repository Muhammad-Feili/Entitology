import re
import networkx as nx
import pandas as pd
from graph.base import GraphBaseModule
from collections import Counter


class FilterModule(GraphBaseModule):
    def __init__(self, DG=None):
        self.DG = DG
        if not self.DG:
            super(FilterModule, self).__init__()
            self.create()

    # attr_value can be a regex
    def node_attribute_partition(self, attr_name: str, attr_value: str):
        filtered_nodes = [node for node, value in self.DG.nodes(
            data=True) if re.search(str(attr_value), str(value.get(attr_name, "")))]
        return filtered_nodes

    # attr_value can be a regex
    def edge_attribute_partition(self, attr_name: str, attr_value: str):
        filtered_edges = [(source, target) for source, target, value in self.DG.edges(
            data=True) if re.search(str(attr_value), str(value.get(attr_name, "")))]
        return filtered_edges

    def node_quantitative_attribute(self, attr_name: str, attr_range: tuple = None):
        start, end = attr_range
        filtered_nodes = [node for node, value in self.DG.nodes(data=True) if value.get(
            attr_name, None) <= end and value.get(attr_name, None) >= start]
        return filtered_nodes

    def edge_quantitative_attribute(self, attr_name: str, attr_range: tuple = None):
        start, end = attr_range
        filtered_edges = [(source, target) for source, target, value in self.DG.edges(
            data=True) if value.get(attr_name, None) <= end and value.get(attr_name, None) >= start]
        return filtered_edges

    def search(self, attrs_names, attr_value):  # , close_items: bool = False):
        # matched_nodes = list()
        # matched_edges = list()

        close_nodes = list()
        # close_edges = list()

        for attr_name in attrs_names:
            # matched_nodes += [node for node, value in self.DG.nodes(
            #     data=True) if re.fullmatch(str(attr_value), str(value.get(attr_name, "")))]
            close_nodes += [node for node, value in self.DG.nodes(
                data=True) if re.search(str(attr_value), str(value.get(attr_name, "")))]

            # matched_edges += [(source, target) for source, target, value in self.DG.edges(
            #     data=True) if re.fullmatch(str(attr_value), str(value.get(attr_name, "")))]
            # if close_items:
            #     close_edges += [(source, target) for source, target, value in self.DG.edges(
            #         data=True) if re.search(str(attr_value), str(value.get(attr_name, "")))]

        # matched_items = {"nodes": matched_nodes, "edges": matched_edges}
        closed_items = {"nodes": close_nodes}  # , "edges": close_edges}

        # if close_items:
        #     return matched_items, closed_items
        # return matched_items
        return closed_items

#     def get_edges_feature_names(self):
#         feature_names = list()
#         for _, _, features in self.DG.edges(data=True):
#             feature_names = features.keys()
#             break
#         return feature_names

#     def get_all_edges_features(self):
#         edge_feature_names = self.get_edges_feature_names()
#         edge_features = dict()
#         for feature_name in edge_feature_names:
#             edge_features[feature_name] = list()

#         for _, _, features in self.DG.edges(data=True):
#             for feature_name, feature_value in features.items():
#                 edge_features[feature_name].append(feature_value)

#         return edge_features

    def get_nodes_feature_names(self):
        feature_names = list()
        for _, features in self.DG.nodes(data=True):
            feature_names = features.keys()
            break
        return feature_names

    def get_all_nodes_features(self):
        node_feature_names = self.get_nodes_feature_names()
        node_features = dict()
        for feature_name in node_feature_names:
            node_features[feature_name] = list()

        for _, features in self.DG.nodes(data=True):
            for feature_name, feature_value in features.items():
                node_features[feature_name].append(feature_value)

        return node_features

    def identify_string_feature_type(self, feature_values):
        feature_type = None
        for value in feature_values:
            if value is not None:
                if type(value) is str:
                    feature_type = "str"
                    break
        return feature_type

    def check_repetitivity(self, feature_values):
        feature_type = self.identify_string_feature_type(feature_values)
        if feature_type != "str":
            return False

        value_counts = dict(Counter(feature_values))

        if any(map(lambda item: item[1] > 1 and not pd.isna(item[0]), value_counts.items())):
            return True
        else:
            return False

    def get_repetitive_features(self, features):
        repetitive_features = dict()
        for feature_name, feature_values in features.items():
            if re.search(feature_name, "_class") or self.check_repetitivity(feature_values):
                repetitive_features[feature_name] = feature_values
            else:
                continue

        return repetitive_features

    def validate_frequencies(self, frequencies):
        validated_frequencies = dict()
        for value, count in frequencies.items():
            if count >= 2:  # and not pd.isna(value):
                validated_frequencies[value] = count

        return validated_frequencies

    def compute_repetitive_features_frequencies(self, repetitive_features):
        for feature_name, feature_values in repetitive_features.items():
            frequencies = Counter(feature_values)
            revised_frequencies = self.validate_frequencies(frequencies)
            repetitive_features[feature_name] = dict(revised_frequencies)

        return repetitive_features

    def identify_repetitive_features(self):
        nodes_features = self.get_all_nodes_features()
        nodes_repetitive_features = self.get_repetitive_features(
            nodes_features)
        node_repeatetie_feature_frequencies = self.compute_repetitive_features_frequencies(
            nodes_repetitive_features)

#         edges_features = self.get_all_edges_features()
#         edges_repetitive_features = self.get_repetitive_features(
#             edges_features)
#         edge_repeatetie_feature_frequencies = self.compute_repetitive_features_frequencies(
#             edges_repetitive_features)

        feature_filters = self.create_filters(
            node_repeatetie_feature_frequencies)

        return feature_filters

    def create_filters(self, features_frequencies):
        features_filters = dict()
        all_features_names = list(self.get_nodes_feature_names())
        for feature_name, feature_frequencies in features_frequencies.items():
            features_filters[feature_name] = self.identify_frequent_variable_properties(
                feature_name, feature_frequencies)
            all_features_names.remove(feature_name)

        numerical_features_filters = self.identify_numerical_features_filters(
            all_features_names)
        for key, value in numerical_features_filters.items():
            features_filters[key] = value

        return features_filters

    def get_node_feature_values_range(self, feature_name):
        values = list()
        for _, features in self.DG.nodes(data=True):
            values.append(features[feature_name])

        values = [x for x in values if pd.isna(x) == False]
        return min(values), max(values)

    def is_numerical(self, feature_name):
        feature_type = None
        for _, features in self.DG.nodes(data=True):
            tpe = type(features[feature_name])
            if (tpe is float and not pd.isna(features[feature_name])) or tpe is int:
                return True
            else:
                continue

        return False

    def identify_numerical_features_filters(self, possible_numerical_features):
        numerical_features_filters = dict()
        for feature_name in possible_numerical_features:
            if self.is_numerical(feature_name):
                min_value, max_value = self.get_node_feature_values_range(
                    feature_name)
                numerical_features_filters[feature_name] = {"editable": True,
                                                            "enable": True,
                                                            "type": "range",
                                                            "options": [min_value, max_value],
                                                            "value": [min_value, max_value]}

            else:
                continue

        return numerical_features_filters

    def identify_frequent_variable_properties(self, feature_name, feature_frequencies):
        sorted_items = dict(
            sorted(feature_frequencies.items(), key=lambda item: item[1]))

        if "_class" in feature_name:
            return {"editable": True,
                    "enable": True,
                    "type": "enum-eq",
                    # frontend gets the count of each frequent value as options
                    "options": list(sorted_items.values()),
                    "value": list(sorted_items.keys())}
        else:
            return {"editable": True,
                    "enable": True,
                    "type": "string",
                    # frontend gets the count of each frequent value as options
                    "options": list(sorted_items.values()),
                    "value": list(sorted_items.keys())}
