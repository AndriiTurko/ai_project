from helper import *
from routes import *


def count_cost(time_of_ride, ride_distance):
    cost = BFa + ((CPMin * time_of_ride) + (CPkm * ride_distance) * SBM) + BFe
    return cost


def main():
    # The place where your 2 points are located. It will be used to create a graph from the OSM data
    # In this example, the 2 points are two addresses in Lviv, so we choose "Lviv"
    graph_area = "Lviv"

    # Two pairs of (lat,lng) coordinates
    origin_coordinates = (49.801894, 24.018080)
    destination_coordinates = (49.801880, 23.997494)

    # List of streets with traffic jams
    traffic_jam = ['Стрийська вулиця', 'Княгині Ольги вулиця']

    amount_of_paths = 9

    lengths_m, times_s, routes, graph = find_possible_distances_and_times_of_routes(graph_area, origin_coordinates,
                                                                                    destination_coordinates,
                                                                                    traffic_jam, amount_of_paths)

    lengths_km = [l / 1000 for l in lengths_m]  # from metres to kilometres
    times_m = [t / 60 for t in times_s]  # from seconds to minutes

    print("All shortest ways to get to the destination point\n\nCost: (time, distance)")
    for i in range(amount_of_paths):
        print(str(count_cost(times_m[i], lengths_km[i])) + ": (" + str(times_m[i]) + ", " + str(lengths_km[i]) + ")")
    print()
    dicti = {count_cost(times_m[i], lengths_km[i]): [times_m[i], lengths_km[i], i] for i in range(amount_of_paths)}

    first_proposal = list(dicti.keys())[0]
    first_time_and_length = dicti.pop(first_proposal)

    min_time = min_max(dicti, True)
    max_length = min_max(dicti, False)

    print("The first proposed cost:", round(first_proposal, 2), "UAH, with such (time, distance) -",
          first_time_and_length[:2])

    res_min_time = list(min_time.keys())[0]
    if res_min_time < first_proposal:
        print("Found better cost:", round(res_min_time, 2), "UAH, with such (time, distance) -",
              min_time[res_min_time][:2])
        fig, ax = ox.plot_graph_routes(graph, [routes[0], routes[min_time[res_min_time][2]]],
                                       route_colors=['r', 'b'], route_linewidth=3, node_size=0)

    res_max_length = list(max_length.keys())[0]
    if res_max_length < first_proposal:
        print("Found better cost:", round(res_max_length, 2), "UAH, with such (time, distance) -",
              max_length[res_max_length][:2])
        fig, ax = ox.plot_graph_routes(graph, [routes[0], routes[max_length[res_max_length][2]]],
                                       route_colors=['r', 'b'], route_linewidth=3, node_size=0)

    print("end")


if __name__ == "__main__":
    main()
