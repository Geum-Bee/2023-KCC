import numpy as np
import csv
# from tkinter import *


# 지도 그리기
def draw_map(city, region) :

    # master = Tk()

    count = 0
    cut   = 64550

    picx = 34
    picy = 127
    delta_x= 2
    delta_y= 3
    cropx=[ picx,  picx+ delta_x  ]
    cropy=[ picy,  picy+ delta_y  ]

    vxy = {}

    vertex_file = 'csvs/PNU_' + city+ "_" + region + '_vertex.csv'
    edge_file   = 'csvs/PNU_' + city+ "_" + region + '_edge.csv'

    with open(vertex_file, newline='', encoding='cp949') as vfile:
        count += 1
        vertex = list(csv.reader( vfile))

    vname = vertex[0]
    #print("Vertex File Field:", vname )

    maxx = 0
    minx = 1000
    maxy = 0
    miny = 1000
    for (i,w) in enumerate(vertex[1:]) :
        if i > cut : break
        w[0] = int(w[0])  # ID
        w[1] = int(w[1])
        w[3] = float(w[3])
        w[4] = float(w[4])
        vxy[ w[0]] = ( w[3], w[4] )     # 위치 (x,y)를 dict에 해슁
        #print(i, w )
        if w[3] > maxx : maxx = w[3]
        if w[3] < minx : minx = w[3]
        if w[4] > maxy : maxy = w[4]
        if w[4] < miny : miny = w[4]

    xgap = maxx - minx
    ygap = maxy - miny

    # print( f' x의 범위{minx,maxx},  \n y의 범위{miny,maxy}')
    # print( f' xgap {xgap:10.4f},  ygap {ygap:10.4f}')
    vfile.close()

    #print("\n\n# edge file을 읽습니다\n")

    exy={}

    with open(edge_file, newline='',encoding='cp949') as efile:
        count += 1
        edge = list(csv.reader( efile ))

    ename = edge[0]
    #print("Edge File Field:", ename )

    for (i,w) in enumerate( edge[1:]) :
        if i > cut : break
        w[0] = int(w[0])
        w[1] = int(w[1])
        w[2] = int(w[2])  # 3이 없음
        w[4] = float(w[4])
        exy[ w[0]] = ( w[1], w[2] )  # edge (x,y)
        #print(i, w )

    efile.close()


    # wx = 1000                                 # tk 사이즈 조절
    # wy = 600
    # gap = 10
    # # w = Canvas(master, width=wx, height=wy )
    # Myfont =  ( "맑은 고딕", 20)

    # def vmap( point, minv, maxv, tline, gap ) :
    #     rpoint = int( (point-minv)/(maxv-minv)*( tline - gap))
    #     return( rpoint)


    # for my in vxy :
    #     cx = vxy[ my ][0]
    #     cy = vxy[ my ][1]
    #     x = vmap ( cx, minx, maxx, wx, 10 )
    #     y = vmap ( cy, miny, maxy, wy, 10 )
    #     w.create_rectangle( x-1, y-1, x+1, y+1, fill="blue", )

    notv = 0
    for (inum,my) in enumerate(exy) :
        u = exy[ my ][0]
        v = exy[ my ][1]
        if u in vxy.keys() and v in vxy.keys() :
            px = vxy[u][0]
            py = vxy[u][1]
            qx = vxy[v][0]
            qy = vxy[v][1]
            #print(px, py, qx, qy)
            # ux =  vmap ( px, minx, maxx, wx, 10 )
            # uy =  vmap ( py, miny, maxy, wy, 10 )
            # vx =  vmap ( qx, minx, maxx, wx, 10 )
            # vy =  vmap ( qy, miny, maxy, wy, 10 )
            #print( f' Draw ({ux,uy}), ({vx,vy})')
            #if inum % 500 == 0 :
            #xval= f'{px:4.3f}' ; yval=f'{py:4.3f}'
            #vlabel=str(xval)+","+str(yval)
            #w.create_text( ux, uy, text= vlabel, fill='black' )
            # w.create_line( ux, uy, vx, vy, fill="orange", width=1)              # width 2에서 1로 변경함
        else :
            if u not in vxy.keys() :
                notv += 1
                #print( u, "가 edge에는 있지만 vertex에는 없음" )
            if v not in vxy.keys() :
                notv += 1
                #print( v, "가 edge에는 있지만 vertex에는 없음" )
        #print( u, v)


    # print(" Total vertices = ", len(vxy) )
    # print(" Total Edges = ", len(exy) )
    # print(" edge에는 있지만 vertex에 없는 정점 수 =", notv)
    # w.pack()
    # mainloop()                                                            # 안보이게

    return vertex_file, edge_file, len(exy)


# ID 1부터 오름차순으로 변경
def make_id(vertex_file, edge_file):
    vtx = open(vertex_file, 'r', encoding='cp949')
    read_vtx = csv.reader(vtx)
    next(read_vtx)  # 첫째 줄 스킵

    v_dict = {}
    cnt = 1
    for line in read_vtx:  # v_dict에 ID 값 1부터 오름차순으로 할당
        v_dict[line[0]] = cnt
        cnt += 1

    vtx.close()
    # =================================================================================

    vertex = open(vertex_file, 'r', encoding='cp949')  # 좌표값 넣어주기
    read_vertex = csv.reader(vertex)
    next(read_vertex)

    loc_dict = {}

    for line in read_vertex:
        loc_dict[v_dict[line[0]]] = (float(line[3]), float(line[4]))

    vertex.close()

    # =================================================================================
    ege = open(edge_file, 'r', encoding='cp949')
    read_ege = csv.reader(ege)
    next(read_ege)  # 첫째 줄 스킵

    e_info = {}  # key 값은 (frontid, endid) value는 거리(m)
    for line in read_ege:
        e_info[(v_dict[line[1]], v_dict[line[2]])] = float(line[4])

    temp_dict = {}  # 양방향 통행 만들기 위해서 만듦.
    temp_lst = []

    for key in e_info.keys():
        swapped_key = tuple(reversed(key))
        if swapped_key not in e_info:
            temp_dict[swapped_key] = e_info[key]
    temp_lst.append(temp_dict)

    for dct in temp_lst:
        e_info.update(dct)

    ege.close()

    return v_dict, e_info, loc_dict


# vertex들의 degree를 리스트에 저장
def save_degree(v_dict, e_info) :
    node_num = len(v_dict)

    adj = np.zeros((node_num+1, node_num+1))                         # 1번째 행과 열(index가 0)은 무시해야함

    for i in e_info.keys() :
        adj[i[0]][i[1]] = 1

    degree_num = []

    for i in range(0, node_num+1) :                                  # 인덱스 계산 용이하기 위해 0부터 시작함
        degree_num.append(np.count_nonzero(adj[:, i]))

    degree_num = np.array(degree_num)

    return degree_num


# graph 만들기
def make_graph(e_info) :
    temp_nodes = list(e_info.keys())
    temp_times = list(e_info.values())

    graph_lst = []

    for node, dist in zip(temp_nodes, temp_times) :
        graph_value = {node[1] : dist}
        graph_lst.append(graph_value)

    graph = {}

    for tup, dic in zip(temp_nodes, graph_lst) :
        if tup[0] in graph :
            graph[tup[0]].update(dic)
        else :
            graph[tup[0]] = dic

    graph = dict(sorted(graph.items()))

    return graph


def set_data(city, region) :
    vertex_file, edge_file, tot_edge = draw_map(city, region)
    v_dict, e_info, loc_dict         = make_id(vertex_file, edge_file)
    degree_num                       = save_degree(v_dict, e_info)
    graph                            = make_graph(e_info)

    return loc_dict, degree_num, graph, tot_edge