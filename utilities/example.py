from ST7735Control import ST7735Control 

# Create a new control object
mydisplay = ST7735Control()

# Text to display...
mydisplay.printText((  0,  0), "Node 0", (255,255,255))
mydisplay.printText(( 80,  0), "Up", (0,255,0))
mydisplay.printText((  0, 12), "Node 1", (255,255,255))
mydisplay.printText(( 80, 12), "Up", (0,255,0))
mydisplay.printText((  0, 24), "Node 2", (255,255,255))
mydisplay.printText(( 80, 24), "Down", (0,0,255))
mydisplay.printText((  0, 36), "Node 3", (255,255,255))
mydisplay.printText(( 80, 36), "Up", (0,255,0))

# Draw some colored rectangles...
mydisplay.drawShape("rectangle", (10, 40, 20, 50), (0,0,255))
mydisplay.drawShape("rectangle", (50, 50, 60, 60), (0,255,0))
mydisplay.drawShape("rectangle", (20, 60, 30, 70), (255,0,0))

# Push it to the display...
mydisplay.update()
