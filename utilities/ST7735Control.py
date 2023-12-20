import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7735

BACKGROUND=(0,0,0)
FOREGROUND=(255,255,255)
FONTSIZE = 10
BAUDRATE = 24000000

##########################################
### Class Stuff Down Here
class ST7735Control:
    def __init__(self):
        # Create a board object...
        self.spi = board.SPI()
        
        # Display configuration for the 1.8" TFT Display
        self.disp = st7735.ST7735R(
            self.spi, 
            rotation=270,
            cs=digitalio.DigitalInOut(board.CE0),
            dc=digitalio.DigitalInOut(board.D25),
            rst=digitalio.DigitalInOut(board.D22),
            baudrate=BAUDRATE,
        )
        
        # Reverse the Width/Height if the display is rotated
        if self.disp.rotation % 180 == 90:
            self.height = self.disp.width
            self.width = self.disp.height
        else:
            self.height = self.disp.height
            self.width = self.disp.width
        
        # Create a new image handle
        self.image = Image.new("RGB", (self.width, self.height))
        
        # Get the drawing object from the image handle
        self.draw = ImageDraw.Draw(self.image)
        
        # Load a Font
        self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE)

        # Clear the Display
        self.clearDisplay()

        # Enable the Backlight
        self.enableBacklight()
    
    def getDimensions(self):
        return (self.width, self.height)

    def clearDisplay(self):
        # Clear the display with the Background color...
        self.draw.rectangle((0, 0, self.width, self.height), fill=BACKGROUND) 
    
    def enableBacklight(self):
        self.tft_bl = digitalio.DigitalInOut(board.D24)
        # Configure the Backlight as an output...
        self.tft_bl.direction = digitalio.Direction.OUTPUT
        # Enable the Backlight by Default...
        self.tft_bl.value = True

    def printText(self, originTuple, text, color):
        # Draw some Text
        self.draw.text(
            originTuple,
            text,
            font=self.font,
            fill=color,
        )

    def drawShape(self, shape, size_tuple, color_tuple):
        """
            The LCD Origin is in the top-left of the display when it is oriented in landscape mode.
        """
        if shape == "rectangle":
            # Start X, Start Y, End X, End Y
            self.draw.rectangle(size_tuple, fill=color_tuple)

    def update(self):
        self.disp.image(self.image)

