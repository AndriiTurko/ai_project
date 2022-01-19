import osmnx as ox


def find_possible_distances_and_times_of_routes(graph_area, origin_coordinates, destination_coordinates,
                                                traffic_jam, amount_of_paths=5):

    print("Creating the graph of the area from OSM data.")
    G = ox.graph_from_place(graph_area, network_type='drive', simplify=False)

    # OSM data are sometime incomplete so we use the speed module of osmnx to add missing edge speeds and travel times
    G = ox.add_edge_speeds(G)
    G = ox.add_edge_travel_times(G)

    # Save graph to disk if you want to reuse it
    ox.save_graphml(G, graph_area.split(',')[0]+".graphml")

    # Load the graph
    G = ox.load_graphml(graph_area.split(',')[0]+".graphml")

    print("Plotting the graph.")
    # fig, ax = ox.plot_graph(G, figsize=(10, 10), node_size=0, edge_color='y', edge_linewidth=0.2)

    # In the graph, get the nodes closest to the points
    origin_node = ox.get_nearest_node(G, origin_coordinates)
    destination_node = ox.get_nearest_node(G, destination_coordinates)

    print("Getting the shortest routes by distance.")
    shortest_routes_by_distance = list(ox.k_shortest_paths(G, origin_node, destination_node, amount_of_paths))

    routes_lengths = []
    routes_times = []
    print("Counting routes lengths and times.")
    for route in shortest_routes_by_distance:
        route_length = 0
        route_time = 0
        for j in range(len(route)-2):
            for i in list(G.edges(data=True)):
                if (i[0] == route[j]) and (i[1] == route[j+1]):
                    edge = i[2]
                    route_length += edge['length']
                    travel_time = edge['travel_time']
                    # multiplier (1.5) means, that average speed is 33.33 kph, (5) means 10 kph
                    route_time += travel_time*1.5 if 'name' not in edge or \
                                                     edge['name'] not in traffic_jam else travel_time*5
        routes_lengths.append(route_length)
        routes_times.append(route_time)

    return routes_lengths, routes_times, shortest_routes_by_distance, G
