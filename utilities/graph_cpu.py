from ST7735Control import ST7735Control 
import json
import sys
import os
from datetime import datetime
from datetime import timedelta
import config

pad = 5

# TFT is 160 x 128
def graphFrame(mydisplay, start_tuple, height, border = True):
    """
    """
    topLeft = (pad+start_tuple[0], start_tuple[1])
    bottomRight = (160-pad-1, start_tuple[1]+height)
    borderTuple = (topLeft[0], topLeft[1], bottomRight[0], bottomRight[1])
    interiorTuple = (topLeft[0]+1, topLeft[1]+1, bottomRight[0]-1, bottomRight[1]-1)
    ###########################
    # Draw the graph edging/background
    # Gray Box
    mydisplay.drawShape("rectangle", borderTuple, (128,128,128))
    if border:
        # Black Fill
        mydisplay.drawShape("rectangle", interiorTuple, (0,0,0))

def lineGraph(mydisplay, data, scaleMax, graphTuple, justify = "Top", 
              graph_type = "line bezier", color_tuple = (0,0,0)):
    """
    """
    y_offset = graphTuple[1]
    maxHeight = graphTuple[3] - graphTuple[1]
    ###########################
    # Normalize the data
    if justify == "Top":
        data = [(((thisData)*maxHeight/scaleMax)+y_offset) for thisData in data]
    else:
        data = [(((scaleMax-thisData)*maxHeight/scaleMax)+y_offset) for thisData in data]
    ###########################
    # Draw the graph data
    mydisplay.drawShape(graph_type, graphTuple, color_tuple, data)

def graph_data():
    thisFontSize = 12

    offlineColor = (64,64,64)

    # Create a new control object
    try:
        # With no arguments, default to hardware mode
        if len(sys.argv) > 1 and sys.argv[1] == "test":
            mydisplay = ST7735Control(thisTestMode=True, thisFontSize=thisFontSize)
        else:
            mydisplay = ST7735Control(thisTestMode=False, thisFontSize=thisFontSize)
    except:
        # Fail to test mode...
        mydisplay = ST7735Control(thisTestMode=True, thisFontSize=thisFontSize)
        
    for thisCluster in range(4):
        path = os.path.expanduser("~/data/stats_data_%s-%d.local.json"%(config.basename, thisCluster))

        graph_height = 12
        print_y_offset = 5*thisCluster + graph_height*thisCluster + (thisFontSize+3)*thisCluster
        graph_y_offset = 5*thisCluster + graph_height*thisCluster + (thisFontSize+3)*(thisCluster + 1)
        
        # Read in the JSON Data
        with open(path, "r") as json_data:
            data = json.load(json_data)

        # Check the last sample update time, if it is older than 15 minutes, the node is considered offline...
        offline_limit_time = datetime.fromisoformat(data["update_time"]) + timedelta(minutes=15)

        if datetime.now() > offline_limit_time:
            node_offline = True
            node_name_color = offlineColor
            node_temp_color = offlineColor
            node_state_color = (60,60,170)
            node_state = "Down"
            node_state_x = 125
            node_cpu_color = offlineColor
            node_mem_color = offlineColor
        else:
            node_offline = False
            node_name_color = (170,170,170)
            node_temp_color = (190,40,190)
            node_state_color = (60,170,60)
            node_state = "Up"
            node_state_x = 140
            node_cpu_color = (35,115,170)
            node_mem_color = (170,45,35)

        # Print info
        mydisplay.printText(( pad, print_y_offset), "Node-%d.local"%(thisCluster), node_name_color)
        mydisplay.printText((  90, print_y_offset), "%.1f"%(data["cpu_temp"]), node_temp_color)
        mydisplay.printText(( node_state_x, print_y_offset), "%s"%(node_state), node_state_color)

        # Draw the Graph Frame
        #graphFrame(mydisplay, (0,graph_y_offset), graph_height)

        # Draw the CPU Utilizatin
        if len(data["cpu_samples"]) > 150-2:
            data_cpu_samples_trimmed = data["cpu_samples"][(len(data["cpu_samples"]) - (150-2)):]
        else:
            data_cpu_samples_trimmed = data["cpu_samples"]
        lineGraph(mydisplay,
            data_cpu_samples_trimmed, 
            100, 
            (5, graph_y_offset, 155, graph_y_offset+graph_height),
            "Bottom",
            "filled bezier",
            node_cpu_color
        )
        
        # Overlay the Memory Utilizatin
        if len(data["mem_samples"]) > 150-2:
            data_mem_samples_trimmed = data["mem_samples"][(len(data["mem_samples"]) - (150-2)):]
        else:
            data_mem_samples_trimmed = data["mem_samples"]
        lineGraph(mydisplay, 
            data_mem_samples_trimmed,
            data["mem_total"],
            (5, graph_y_offset, 155, graph_y_offset+graph_height),
            "Bottom",
            "line bezier",
            node_mem_color
        )
        
    # Push it to the display...
    mydisplay.update()

if __name__ == "__main__":
    graph_data()
