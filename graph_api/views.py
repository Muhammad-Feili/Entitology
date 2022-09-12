import json
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from graph.filter import FilterModule
from graph.metric import MetricModule
from graph.topology import TopologyModule

from graph_api.models import UserAccessLimit
from graph_api.serializers import QuerySerializer
from graph_api.enums import GraphEnums
from graph_api.utils import GraphUtils


class GraphAPI(APIView):

    @method_decorator(login_required)
    def get(self, request, format=None):
        request_body = json.loads(request.body.decode("utf-8"))
        center_node_id = request_body.get("centerNodeId", "")

        neighbourhood_graph = TopologyModule().neighbourhood_depth(center_node_id,
                                                                   neighbour_depth=GraphEnums.NEIGHBOUR_DEPTH.value)

        user_access_limit = UserAccessLimit(request.user).limit
        has_access = UserAccessLimit(request.user).has_access

        if has_access or GraphUtils.check_limitation(neighbourhood_graph, user_access_limit):
            #     return Response(QuerySerializer(neighbourhood_graph).serialize())

            # else:
            applicable_filters = FilterModule(
                neighbourhood_graph).identify_repetitive_features()
            return Response(QuerySerializer(neighbourhood_graph).serialize(features_filters=applicable_filters,
                                                                           center_node_id=center_node_id,
                                                                           limit=user_access_limit,
                                                                           has_access=has_access))

    def post(self, request, format=None):
        method = request.method.decode("utf-8")
        return Response({"message": "{} Method not implemented".format(method)})

    def put(self, request, format=None):
        method = request.method
        return Response({"message": "{} Method not implemented".format(method)})

    def patch(self, request, format=None):
        method = request.method
        return Response({"message": "{} Method not implemented".format(method)})

    def delete(self, request, format=None):
        method = request.method
        return Response({"message": "{} Method not implemented".format(method)})


# @login_required
# def graph_api(request):
#     if request.method == "GET":
#         center_node_id = request.data.get("centerNodeId")
#         neighbourhood_graph = TopologyModule().descendants_at_distance(centerNodeId,
#                                                             neighbour_depth=GraphEnums.NEIGHBOUR_DEPTH.value)
#
#         if UserAccessLimit(request.user).has_access() or GraphUtils.check_limitation(neighbourhood_graph, user_access_limit):
#             return QuerySerializer(neighbourhood_graph).serilize()
#
#         else:
#             applicable_filters = FilterModule().identify_repetitive_features()
#             return QuerySerializer(neighbourhood_graph).serilize(filters)
#
#     else:
#         method = request.method
#         return Response({"message": "{} Method not implemented".format(method)})
#
# @login_required
# def filter(request):
#     if request.method == "GET
#         module = FilterModule()
#
#         function = request.data.get("function")
#         if function == "partition":
#             attr_name = request.data.get("attr_name")
#             attr_value = request.data.get("attr_value")
#
#             filtered_module = module.node_attribute_partition(attr_name, attr_value)
#             query_serilizer = QuerySerializer(filtered_module.get_graph())
#             serialized_data = query_serilizer.serilize("partition", filtered_module)
#
#         elif function == "partition":
#             attr_name = request.data.get("attr_name")
#             attr_value = request.data.get("attr_value")
#
#             filtered_module = module.node_attribute_partition(attr_name, attr_value)
#
#         elif function == "partition":
#             attr_name = request.data.get("attr_name")
#             attr_value = request.data.get("attr_value")
#
#             filtered_module = module.node_attribute_partition(attr_name, attr_value)
#
#         elif function == "partition":
#             attr_name = request.data.get("attr_name")
#             attr_value = request.data.get("attr_value")
#
#             filtered_module = module.node_attribute_partition(attr_name, attr_value
#
#         return JsonResponse(serialized_data, safe=False)
#
#     elif request.method == "POST":
#         pass
#
#     else:
#         return JsonResponse("Not Implemented!")
#
# @login_required
# def metric(request):
#     if request.method == "GET":
#         module = MetricModule()
#
#         function = request.data.get("function")
#         if function == "eigen_centrality
#             metric_module = module.eigen_centrality()
#
#
#         json_data = json.dumps(metric_module)
#
#         return JsonResponse(json_data, safe=False)
#
#     else:
#         return JsonResponse("Not Implemented!")
#
# @login_required
# def topology(request):
#     if request.method == "GET":
#         module = TopologyModule()
#         mutuals = module.mutuals()
#         json_data = json.dumps(mutuals)
#
#         return JsonResponse(json_data, safe=False)
#
#     elif request.method == "POST":
#         pass
#
#     else:
#         return JsonResponse("Not Implemented!")
