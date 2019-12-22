import pandas as pd
import numpy as np
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


def create_sim_space_826(file_name: str = "./fiberBoard826.xls", save_folder: str = './results/', line_width: float = 0.05, line_dist: float = 0.25, channel_num: int = 12) -> pd.DataFrame:
    data = pd.read_excel(file_name)

    BeginPointX = 0
    BeginPointY = 0
    BeginPointZ = 0

    zoom_factor_x = 130.0 / 450
    # zoom_factor_y = 100.0 / 70

    above_list = [29, 26, 24, 20, 21, 18, 19, 16, 17,  2, 14, 15, 12, 13, 10, 11,  8,  9,  1,  6,  7]
    above_dist = [18, 86, 6, 6, 6, 118, 8, 8, 8, 18, 18, 8, 8, 8, 34, 8, 25, 8, 18, 18, 8]
    # switch port 41 and port 42
    below_list = [59, 53, 54, 55, 56, 57, 58, 52, 47, 48, 49, 50, 51, 43, 44, 45, 46, 42, 41, 39, 38, 33, 32, 31, 30]
    below_dist = [ 4, 18, 18, 18,  6,  6,  6, 58,  6,  6,  6,  6,  6,  6,  6,  8,  8,  8, 18, 48, 18, 18, 18, 25, 25]
    above_dist = np.cumsum(above_dist) * zoom_factor_x
    below_dist = np.cumsum(below_dist) * zoom_factor_x

    channels = [[0 for i in range(channel_num*4)] for j in range(60)]

    def find_1st_0(l, st):
        x = next((i for i, x in enumerate(l[st:]) if x == 0), None)
        if x != None:
            return x + st
        else:
            return next((i for i, x in enumerate(l[:st]) if x == 0), None) + st

    def layout_sn_ln(x):
        # find the 1st '0' in the list
        p1 = find_1st_0(channels[x.Port1], 0)
        p2 = find_1st_0(channels[x.Port2], 0)
        #TODO::maybe dead loop here, caution!!
        while int(p1/channel_num) != int(p2/channel_num):
            if int(p1/channel_num) > int(p2/channel_num):
                p2 = find_1st_0(channels[x.Port2], int(p1/channel_num)*channel_num)
            elif int(p1/channel_num) < int(p2/channel_num):
                p1 = find_1st_0(channels[x.Port1], int(p2/channel_num)*channel_num)
        channels[x.Port1][p1] = 1
        channels[x.Port2][p2] = 1
        return (p1, p2)

    def layout_sn(x):
        return x.SN_LN[0]

    def layout_ln(x):
        return x.SN_LN[1]

    def sn_posx(x):
        base_x = above_dist[above_list.index(x.Port1)] if x.Port1 in above_list else below_dist[below_list.index(x.Port1)]
        return base_x + (x.SN - channel_num / 2) * (line_dist + line_width)

    def ln_posx(x):
        base_x = above_dist[above_list.index(x.Port2)] if x.Port2 in above_list else below_dist[below_list.index(x.Port2)]
        return base_x + (x.LN - channel_num / 2) * (line_dist + line_width)

    data["Port1"] = pd.to_numeric(data["Port1"].str.split(':', expand=True)[0].str[1:])
    data["Port2"] = pd.to_numeric(data["Port2"].str.split(':', expand=True)[0].str[1:])
    data["SN_LN"] = data.apply(lambda x: layout_sn_ln(x), axis=1)
    data["SN"] = data.apply(lambda x: layout_sn(x), axis=1)
    data["LN"] = data.apply(lambda x: layout_ln(x), axis=1)

    data["sx"] = data.apply(lambda x: sn_posx(x), axis=1)
    data["lx"] = data.apply(lambda x: ln_posx(x), axis=1)
    # switch port1 and port2 if port2 is at the right of port1.
    idx = (data["sx"] < data["lx"])
    data.loc[idx, ["Port1", "Port2", "SN", "LN", "sx", "lx"]] = data.loc[idx, ["Port2", "Port1", "LN", "SN", "lx", "sx"]].values
    data["dx"] = data.apply(lambda x: x.sx - x.lx, axis=1)
    # hard code 100 height here
    data["sy"] = data.apply(lambda x: BeginPointY+100 if x.Port1 in above_list else BeginPointY, axis=1)
    data["ly"] = data.apply(lambda x: BeginPointY + 100 if x.Port2 in above_list else BeginPointY, axis=1)
    data["dz"] = data.apply(lambda x: int(x.SN / channel_num), axis=1)
    data = data.sort_values(by="dx", ascending=True)

    data.to_excel(save_folder + "fiberBoard826data.xlsx")

    return data