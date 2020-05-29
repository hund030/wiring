import pandas as pd
from problem_graph import create_sim_space, read_sim_space
from wiring_rect_826 import plotter_rect, svg2dwgscr_rect
from wiring_bend_826 import plotter_bend, svg2gds_bend
from waveguide_calculator import calc_index, draw_chart
# Demands
# channels count
N = 256
# save folder
SaveFolder = "./results/"
Src = "./fiberBoard" + str(N) + ".xlsx"
SimSpace = SaveFolder + "fiberBoard" +str(N) + "rect.xlsx"
# the width of the fibers, unit: mm
Line_Width = 0.05
# the minimal Distance between parallel lines, unit: mm
Dist = 0.250
# minimal bend radius, unit: mm
Bend_Radius = 10
# bend.svg accuracy, unit: mm
Delta_Arc = 0.001
# mm
height = 150
width = 150

def main() -> None:
    print("******* Start! ********")
    print("******* Routing the waveguides without bend... ********")
    df = create_sim_space(Src, SaveFolder, Line_Width, Dist, height=height, N=N)
    df_rect = plotter_rect(df, Line_Width, Dist+Line_Width, SaveFolder, height=height, N=N, r=Bend_Radius)
    # svg2dwgscr_rect(df_rect, "fiberBoard"+str(N)+"rect.scr", SaveFolder)
    print("******* Adding bend to the routed plain... ********")
    df_bend = plotter_bend(df_rect, Line_Width, Dist + Line_Width, Bend_Radius, Delta_Arc, SaveFolder, "fiberBoard"+str(N)+"bend")
    # print("******* Converting the data to gds file... ********")
    svg2gds_bend(df_bend, Line_Width, Bend_Radius, "fiberBoard"+str(N)+"bend.gds", SaveFolder)
    print("******* Calculating various index for each waveguide... ********")
    loss = pd.read_excel('crossloss.xlsx')
    df_bend = pd.read_excel(SaveFolder + "fiberBoard"+str(N)+"bend.xlsx")
    del df_bend["Unnamed: 0"]
    df_calc = calc_index(df_bend, loss, Line_Width, Bend_Radius, height, width, "fiberBoard"+str(N)+"calc.xlsx")
    print("******* draw graph ********")
    data = pd.read_excel("fiberBoard"+str(N)+"calc.xlsx")
    draw_chart(data, str(N))
    print("******* All done! ********")

if __name__ == "__main__":
    main()
