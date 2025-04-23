import networkx as nx
from datetime import datetime
from models import Resource, Request

def allocate_resources(resources, requests):
    """
    Uses Maximum Flow algorithm to optimally allocate resources to requests.

    Args:
        resources: List of Resource objects available for allocation
        requests: List of Request objects to be fulfilled

    Returns:
        List of (resource_id, request_id) tuples representing allocations
    """
    # Create a directed graph
    G = nx.DiGraph()

    # Add source and sink nodes
    G.add_node('source')
    G.add_node('sink')

    # Add resource nodes and connect from source
    for resource in resources:
        resource_node = f"r_{resource.id}"
        G.add_node(resource_node)
        G.add_edge('source', resource_node, capacity=1)

    # Add request nodes and connect to sink
    for request in requests:
        request_node = f"q_{request.id}"
        G.add_node(request_node)
        G.add_edge(request_node, 'sink', capacity=1)

    # Connect resources to compatible requests
    for resource in resources:
        for request in requests:
            # Check if resource type matches request type
            if resource.category == request.resource_type:
                # Check if time windows overlap
                if (resource.available_from <= request.needed_to and
                        resource.available_to >= request.needed_from):
                    # Create an edge with capacity=1 and priority as weight
                    G.add_edge(
                        f"r_{resource.id}",
                        f"q_{request.id}",
                        capacity=1,
                        priority=request.priority
                    )

    # Run maximum flow algorithm
    flow_value, flow_dict = nx.maximum_flow(G, 'source', 'sink')

    # Extract the allocations from the flow
    allocations = []
    for resource in resources:
        resource_node = f"r_{resource.id}"
        for request in requests:
            request_node = f"q_{request.id}"

            if (resource_node in flow_dict and
                    request_node in flow_dict[resource_node] and
                    flow_dict[resource_node][request_node] > 0):

                # Add the allocation
                allocations.append((resource.id, request.id))

    return allocations