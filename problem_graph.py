import pandas as pd
import numpy as np
from itertools import tee
import sys

def create_sim_space(file_name: str = "./fiberBoard896.xls", save_folder: str = './results/', line_width: float = 0.125, line_dist: float = 0.2) -> pd.DataFrame:
    data = pd.read_excel(file_name)

    # In this case, we set the left-bottom point as the BeginPoint with changeable coordinate
    # i.e. the intersection point of vertical magenta line and horizontal green line in ./Demands/*.dwg file
    BeginPointX = 0
    BeginPointY = 0
    BeginPointZ = 0
    NumPerOutput = 16
    # OutputDist = 3
    OutputDist = 0.6
    # mt_gap = 7
    mt_gap = (NumPerOutput * (line_width + line_dist) + OutputDist)
    # the number of connectors
    mm_list = [2, 4, 6, 8, 7, 5, 3, 1]
    ll_list = [9, 10, 15, 16, 17, 18, 23, 24]
    sc_list = [1, 2, 3, 4, 5, 6, 7]
    mt_list = [16, 15, 10, 9, 17, 18, 23, 24]

    def ll_mm_ln_posy(x):
        # the k-element is the relative position for Lk-M*-* with minimal distance in y-axis refer to BeginPoint
        ll_bpy_list = [10.5, 23.8, 64.4, 77.7]
        dy = 0
        dy = dy + ll_bpy_list[ll_list.index(x.L) % 4]
        if x.L in ll_list[:4]:
            dy = dy + mm_list.index(x.M) * mt_gap
            if mm_list.index(x.M) >= 4:
                dy = dy + 0.4
            dy = dy + (NumPerOutput/2 - x.LN) * (line_width + line_dist)
        else:
            dy = dy + (len(mm_list) - 1 - mm_list.index(x.M)) * mt_gap
            if mm_list.index(x.M) < 4:
                dy = dy + 0.4
            dy = dy + (x.LN - NumPerOutput/2) * (line_width + line_dist)
        return BeginPointY + dy

    def sc_mt_sn_posx(x):
        # the k-element is the relative position for SCk-MT*-* with minimal distance in x-axis refer to BeginPoint
        sc_bpx_list = [42.8 + i * 6 for i in range(7)]
        dx = 0
        dx = dx + sc_bpx_list[sc_list.index(x.SC)] + (mt_list.index(x.MT) % 4) * mt_gap
        if mt_list.index(x.MT) < 4:
            dx = dx + (x.SN - NumPerOutput/2 + 0.5) * (line_width + line_dist)
        else:
            dx = dx + (NumPerOutput/2 + 0.5 - x.SN) * (line_width + line_dist)
        return BeginPointX + dx

    df_sc = data["Port1"].str.split('-', expand=True)
    df_sc[0] = pd.to_numeric(df_sc[0].str[2:])
    df_sc[1] = pd.to_numeric(df_sc[1].str[2:])
    df_sc[2] = pd.to_numeric(df_sc[2])
    df_sc.columns = ['SC', 'MT', 'SN']
    df_sc['sx'] = df_sc.apply(lambda x: sc_mt_sn_posx(x), axis=1)
    df_sc['sy']=df_sc.apply(lambda x: BeginPointY+5 if x.MT in mt_list[:4] else BeginPointY+95, axis=1)

    df_l = data["Port2"].str.split('-', expand=True)
    df_l[0] = pd.to_numeric(df_l[0].str[1:])
    df_l[1] = pd.to_numeric(df_l[1].str[1:])
    df_l[2] = pd.to_numeric(df_l[2])
    df_l.columns = ['L', 'M', 'LN']
    df_l['lx'] = df_l.apply(lambda x: BeginPointX+0 if x.L in ll_list[:4] else BeginPointX+130,  axis=1)
    df_l['ly']=df_l.apply(lambda x: ll_mm_ln_posy(x), axis=1)

    df=pd.concat([data, df_sc, df_l], axis=1)
    # df.to_excel(save_folder +"fiberBoard896data.xlsx")

    return df


def create_sim_space_826(file_name: str = "./fiberBoard826.xls", save_folder: str = './results/', line_width: float = 0.05, line_dist: float = 0.25, channel_num: int = 12, height: int = 150) -> pd.DataFrame:
    data = pd.read_excel(file_name)

    BeginPointX = 0
    BeginPointY = 0
    BeginPointZ = 0

    # serial number for each port 
    '''
    above_list = [29, 26, 21, 20, 24, 17, 10, 16, 18, 19, 2, 13, 12, 14, 9, 8]
    below_list = [53, 54, 56, 57, 58, 48, 47, 49, 51, 41, 33, 11, 38, 39, 1, 6]
    '''
    above_list = [21, 116, 29, 114, 26, 113, 20, 117, 24, 118, 18, 107, 19, 108, 16, 109, 17, 101, 10, 111, 2, 12, 13, 98, 71, 99, 14, 93, 8, 61, 9, 66]
    below_list = [53, 89, 54, 80, 56, 81, 57, 86, 58, 84, 47, 79, 48, 78, 49, 76, 51, 77, 41, 70, 11, 62, 38, 74, 39, 72, 1, 73, 33, 68, 6, 69]
    # distance to the previous port
    '''
    above_dist = [6.5] + [9] * (len(above_list)-1)
    below_dist = [2] + [9] * (len(below_list)-1)
    '''
    above_dist = [4] + [4.5] * (len(above_list)-1)
    below_dist = [2] + [4.5] * (len(below_list)-1)
    above_dist = np.cumsum(above_dist)
    below_dist = np.cumsum(below_dist)

    def find_next(value: int, l: list, reverse: bool) -> int:
        length = len(l)
        for i in range(length):
            i = length - i - 1 if reverse else i
            if l[i] == value:
                return i
        # didn't find the value
        print("didn't find the value %d, in "%(value), l)
        return -1

    def sn_posx(x):
        idx = find_next(x.index2, PORTS[int(x.index1)], False)
        PORTS[int(x.index1)][idx] = -1
        base_x = above_dist[above_list.index(x.Port1)] if x.Port1 in above_list else below_dist[below_list.index(x.Port1)]
        return base_x + idx * (line_dist + line_width)

    def ln_posx(x):
        idx = find_next(x.index1, PORTS[int(x.index2)], x.sy==x.ly)
        PORTS[int(x.index2)][idx] = -1
        base_x = above_dist[above_list.index(x.Port2)] if x.Port2 in above_list else below_dist[below_list.index(x.Port2)]
        return base_x + idx * (line_dist + line_width)

    PORTS = [[] for j in range(len(below_list)+len(above_list))]
    def calc_sn_ln(x):
        PORTS[int(x.index1)].append(x.index2)
        PORTS[int(x.index2)].append(x.index1)
        return None

    def coarse_sort(PORTS):
        for i, l in enumerate(PORTS):
            left = []
            center = []
            right = []
            if i < len(above_list):
                for it in l:
                    if it < i:
                        left.append(it)
                    elif it > i and it < len(above_list):
                        right.append(it)
                    elif it >= len(above_list) and it < len(above_list) + len(below_list):
                        center.append(it)
                    else:
                        # TODO:: throw exception
                        print("Port error")
            else:
                for it in l:
                    if it < len(above_list):
                        center.append(it)
                    elif it < i:
                        left.append(it)
                    elif it > i and it < len(above_list) + len(below_list):
                        right.append(it)
                    else:
                        # TODO:: throw exception
                        print("Port error")
            PORTS[i] = np.sort(left)[::-1].tolist() + np.sort(center).tolist() + np.sort(right)[::-1].tolist()
        return PORTS

    
    # data["Port1"] = pd.to_numeric(data["Port1"].str.split(':', expand=True)[0].str[1:])
    # data["Port2"] = pd.to_numeric(data["Port2"].str.split(':', expand=True)[0].str[1:])
    data["Port1"] = pd.to_numeric(data["Port1"])
    data["Port2"] = pd.to_numeric(data["Port2"])
    idx = (data["Port1"] > data["Port2"])
    data.loc[idx, ["Port1", "Port2"]] = data.loc[idx, ["Port2", "Port1"]].values

    data["index1"] = data.apply(lambda x: above_list.index(x.Port1) if x.Port1 in above_list else below_list.index(x.Port1) + len(above_list), axis=1)
    data["index2"] = data.apply(lambda x: above_list.index(x.Port2) if x.Port2 in above_list else below_list.index(x.Port2) + len(above_list), axis=1)
    data["sy"] = data.apply(lambda x: BeginPointY+height if x.Port1 in above_list else BeginPointY, axis=1)
    data["ly"] = data.apply(lambda x: BeginPointY+height if x.Port2 in above_list else BeginPointY, axis=1)
    data["dz"] = data.apply(lambda x: 0, axis=1)

    data.apply(lambda x: calc_sn_ln(x), axis=1)
    PORTS = coarse_sort(PORTS)

    data["sx"] = data.apply(lambda x: sn_posx(x), axis=1)
    data["lx"] = data.apply(lambda x: ln_posx(x), axis=1)
    data["dx"] = data.apply(lambda x: np.abs(x.sx - x.lx), axis=1)
    # switch port1 and port2 if port2 is at the right of port1.
    idx = (data["sx"] < data["lx"])
    data.loc[idx, ["Port1", "Port2","index1", "index2", "sy", "ly", "sx", "lx"]] = data.loc[idx, ["Port2", "Port1", "index2", "index1", "ly", "sy", "lx", "sx"]].values
    
    data = data.sort_values(by="sx", ascending=True)

    data.to_excel("./fiberBoard0data.xlsx")

    return data
