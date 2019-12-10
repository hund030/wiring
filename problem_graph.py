import pandas as pd


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
        ll_bpy_list = [2.4, 14.8, 74.4, 86.8]
        dy = 0
        dy = dy + ll_bpy_list[ll_list.index(x.L) % 4]
        if x.L in ll_list[:4]:
            dy = dy + mm_list.index(x.M) * mt_gap
            if mm_list.index(x.M) >= 4:
                dy = dy + 0.4
            dy = dy + (NumPerOutput/2 + 0.5 - x.LN) * (line_width + line_dist)
        else:
            dy = dy + (len(mm_list) - 1 - mm_list.index(x.M)) * mt_gap
            if mm_list.index(x.M) < 4:
                dy = dy + 0.4
            dy = dy + (x.LN - NumPerOutput/2 + 0.5) * (line_width + line_dist)
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
    df_sc['sy']=df_sc.apply(lambda x: BeginPointY+29.7 if x.MT in mt_list[:4] else BeginPointY+70.3, axis=1)

    df_l = data["Port2"].str.split('-', expand=True)
    df_l[0] = pd.to_numeric(df_l[0].str[1:])
    df_l[1] = pd.to_numeric(df_l[1].str[1:])
    df_l[2] = pd.to_numeric(df_l[2])
    df_l.columns = ['L', 'M', 'LN']
    df_l['lx'] = df_l.apply(lambda x: BeginPointX+0 if x.L in ll_list[:4] else BeginPointX+130,  axis=1)
    df_l['ly']=df_l.apply(lambda x: ll_mm_ln_posy(x), axis=1)

    df=pd.concat([data, df_sc, df_l], axis=1)
    df.to_excel(save_folder +"fiberBoard896data.xlsx")

    return df
