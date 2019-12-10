import pandas as pd


def create_sim_space(file_name: str = "./fiberBoard896.xls", save_folder: str = './results/') -> pd.DataFrame:
    data = pd.read_excel(file_name)

    # In this case, we set the left-bottom point as the BeginPoint with changeable coordinate
    # i.e. the intersection point of vertical magenta line and horizontal green line in ./Demands/*.dwg file
    BeginPointX = 0
    BeginPointY = 0
    BeginPointZ = 0
    # the number of connectors
    mm_list = [2, 4, 6, 8, 7, 5, 3, 1]
    ll_list = [9, 10, 15, 16, 17, 18, 23, 24]
    sc_list = [1, 2, 3, 4, 5, 6, 7]
    mt_list = [16, 15, 10, 9, 17, 18, 23, 24]

    def ll_mm_ln_posy(x):
        # the k-element is the relative position for Lk-M*-* with minimal distance in y-axis refer to BeginPoint
        ll_bpy_list = [12.0, 72.4, 364.4, 424.8]
        dy = 0
        dy = dy + ll_bpy_list[ll_list.index(x.L) % 4]
        if x.L in ll_list[:4]:
            dy = dy + mm_list.index(x.M) * 7
            if mm_list.index(x.M) >= 4:
                dy = dy + 2.2
            dy = dy - 0.125 + (9 - x.LN) * 0.25
        else:
            dy = dy + (7 - mm_list.index(x.M)) * 7
            if mm_list.index(x.M) < 4:
                dy = dy + 2.2
            dy = dy - 0.125 + (x.LN - 8) * 0.25
        return BeginPointY + dy

    def sc_mt_sn_posx(x):
        # the k-element is the relative position for SCk-MT*-* with minimal distance in x-axis refer to BeginPoint
        sc_bpx_list = [193.9 + i * 30.2 for i in range(7)]
        dx = 0
        dx = dx + sc_bpx_list[sc_list.index(x.SC)] + (mt_list.index(x.MT) % 4) * 7
        if mt_list.index(x.MT) < 4:
            dx = dx - 0.125 + (x.SN - 8) * 0.25
        else:
            dx = dx - 0.125 + (9 - x.SN) * 0.25
        return BeginPointX + dx

    df_sc = data["Port1"].str.split('-', expand=True)
    df_sc[0] = pd.to_numeric(df_sc[0].str[2:])
    df_sc[1] = pd.to_numeric(df_sc[1].str[2:])
    df_sc[2] = pd.to_numeric(df_sc[2])
    df_sc.columns = ['SC', 'MT', 'SN']
    df_sc['sx'] = df_sc.apply(lambda x: sc_mt_sn_posx(x), axis=1)
    df_sc['sy']=df_sc.apply(lambda x: BeginPointY+145.0 if x.MT in mt_list[:4] else BeginPointY+343, axis=1)

    df_l = data["Port2"].str.split('-', expand=True)
    df_l[0] = pd.to_numeric(df_l[0].str[1:])
    df_l[1] = pd.to_numeric(df_l[1].str[1:])
    df_l[2] = pd.to_numeric(df_l[2])
    df_l.columns = ['L', 'M', 'LN']
    df_l['lx'] = df_l.apply(lambda x: BeginPointX+0 if x.L in ll_list[:4] else BeginPointX+590,  axis=1)
    df_l['ly']=df_l.apply(lambda x: ll_mm_ln_posy(x), axis=1)

    df=pd.concat([data, df_sc, df_l], axis=1)
    df.to_excel(save_folder +"fiberBoard896data.xlsx")

    return df
