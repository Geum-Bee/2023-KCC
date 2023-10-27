
def run(graph, degree_num, v):
    # start = 1
    # end   = 100

    start = int(input("Enter start point : "))
    end   = int(input("Enter end point   : "))

    spd, sp = calculate.shortest_path_dists(graph, start, end)
    spt     = calculate.shortest_path_times(graph, start, end, degree_num, v)

    spd = round(spd, 2)
    spt = round(spt, 2)

    print()
    print("shortest-path-distance : " + str(spd) + "m")
    print("shortest-path          :", sp)
    print("shortest-path-time     : " + str(spt) + " minutes")


    qpd, qp = calculate.quickest_path_dist(graph, start, end, degree_num, v)
    tup2    = calculate.quickest_path_times(graph, start, end, degree_num, v)
    qpt     = tup2[0]

    qpd = round(qpd, 2)
    qpt = round(qpt, 2)

    print()
    print("quickest-path-distance : " + str(qpd) + "m")
    print("quickest-path          :", qp)
    print("quickest-path-time     : " + str(qpt) + " minutes")
    print()
    print("==================================================================================")

    if sp == qp :
        print()
        print("resonable-path         :", sp)
    else :
        calculate.resonable_path(graph, start, end, spd, qpd, spt, qpt, degree_num)



def main():
    # select1 = int(input("short(1), mid(2), long(3) ? : "))
    # select2 = int(input("속도를 설정하세요. (km/h) : "))
    select2 = 30
    # select3 = int(input("shortest-path time(1) or quickest-path time(2) or turn-shortest-path(3) or shortest-path dist(4)? or " \
    #                     "Resonable-path(5)? : "))

    with open("txts/sample.txt", "r", encoding="UTF-8") as file:
        data = file.readlines()


    line = data[0].strip().split(",")

    city     = line[1]
    region   = line[2]
    velocity = int(line[3]) + select2

    loc_dict, degree_num, graph, tot_edge = setup.set_data(city, region)


    run(graph, degree_num, velocity)


if __name__ == '__main__':
    import setup
    import calculate

    main()