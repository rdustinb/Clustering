from ST7735Control import ST7735Control 
import json
import sys

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
    # Create a new control object
    mydisplay = ST7735Control(thisTestMode=True)
        
    for thisCluster in range(4):
        data_file = "data.json"

        graph_height = 18
        print_y_offset = graph_height*thisCluster + 12*thisCluster + thisCluster
        graph_y_offset = graph_height*thisCluster + 12*(thisCluster + 1) + thisCluster
        
        # Read in the JSON Data
        with open(data_file, "r") as json_data:
            data = json.load(json_data)

        # Print info
        mydisplay.printText(( pad, print_y_offset), "Node %d"%(thisCluster), (255,255,255))
        mydisplay.printText(( 80,  print_y_offset), "Up", (0,255,0))

        # Draw the Graph Frame
        #graphFrame(mydisplay, (0,graph_y_offset), graph_height)

        # Draw the CPU Utilizatin
        lineGraph(mydisplay, data["cpu_samples"], 100, (5, graph_y_offset, 155, graph_y_offset+graph_height), "Bottom", "filled bezier", (128,128,255))
        
        # Overlay the Memory Utilizatin
        lineGraph(mydisplay, data["mem_samples"], data["mem_total"], (5, graph_y_offset, 155, graph_y_offset+graph_height), "Bottom", "line bezier", (255,128,128))
        
    # Push it to the display...
    mydisplay.update()

if __name__ == "__main__":
    graph_data()
