import algorithms
import numpy as np
import copy


def shortest_path_dists(graph, start, end):

    distances, parent = algorithms.dijkstra(graph, start)
    path              = algorithms.get_shortest_path(parent, end)
    spd               = distances[end]          # shortest path distance

    return spd, path


def shortest_path_times(graph, start, end, degree_num, v):

    v = v * 1000 / 60  # m / min

    distances, parent = algorithms.dijkstra(graph, start)
    path              = algorithms.get_shortest_path(parent, end)
    plus_time         = algorithms.add(path, degree_num)
    original_time     = distances[end] / v * 60                   # 단위 초
    spt               = original_time + plus_time
    spt               /= 60
    spt               = np.around(spt, 2)               # shortest path time

    # return spt, path
    return spt


def quickest_path_dist(graph, start, end, degree_num, v):
    graph_temp     = copy.deepcopy(graph)
    tup            = quickest_path_times(graph_temp, start, end, degree_num, v)
    path           = tup[1]
    qpd            = 0

    # print("qpd_func", graph_original)

    for i in range(len(path) - 1):
        qpd += graph[path[i]][path[i+1]]

    # print(qpd)

    return qpd, path



def quickest_path_times(graph, start, end, degree_num, v):

    graph_temp = copy.deepcopy(graph)

    v = v * 1000 / 60  # m / min

    vertices_time = algorithms.make_vertices_time(graph_temp, degree_num)

    for outer_key in graph_temp:                             # graph 거리 -> 시간(초)로 환산
        for inner_key in graph_temp[outer_key]:
            graph_temp[outer_key][inner_key] = (graph_temp[outer_key][inner_key] / v) * 60

    # print("time", graph)

    distances, parent = algorithms.find_quickest_path(graph_temp, start, vertices_time)
    path              = algorithms.get_quickest_path(parent, end)
    qpt               = distances[end]
    qpt /= 60                       # 단위 분
    qpt = np.around(qpt, 2)


    # print(graph)

    return qpt, path


def resonable_path(graph, start, end, spd, qpd, spt, qpt, degree_num) :

    v = 30
    v = v * 1000 / 60

    yen_path = algorithms.yen_algorithm(graph, start, end, 50)

    for lis in yen_path :
        dist = 0
        plus_time = algorithms.add(lis, degree_num)

        for i in range(len(lis) - 1):
            dist += graph[lis[i]][lis[i + 1]]

        original_time = dist / v * 60

        rpt = original_time + plus_time
        rpt /= 60
        # print(round(dist, 2))
        # print(rpt)


        if (spd < dist < qpd) and (qpt < rpt < spt) :
            print()
            print("resonable-path-distance: " + str(round(dist, 2)) + "m")
            print("resonable-path         :", lis)
            print("resonable-path-time    : " + str(round(rpt, 2)) + " minutes")
