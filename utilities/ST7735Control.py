# Optional Libraries if running in TestMode
try:
    import digitalio
    import board
    from adafruit_rgb_display import st7735
except:
    print("Some libraries weren't loaded.")
    print("Please make sure to install digitalio, board, and adafruit_rgb_display if running this in non-test mode.")

# Required Libraries for all modes
from PIL import Image, ImageDraw, ImageFont

BACKGROUND=(0,0,0)
FOREGROUND=(255,255,255)
ROTATION=270
FONTSIZE=10
BAUDRATE=24000000

##########################################
### Class Stuff Down Here
class ST7735Control:
    def __init__(self, thisTestMode):
        # When creating the object, define it in TestMode or not
        self.TestMode = thisTestMode
        # Test mode will render a bitmap instead of trying to write to the display.
        # Useful for debugging graphics code.
        if self.TestMode:
            # Reverse the Width/Height if the display is rotated
            if ROTATION % 180 == 90:
                self.height = 128
                self.width = 160
            else:
                self.height = 160
                self.width = 128

        # Only initialize the display if not in test mode
        else:
            # Create a board object...
            self.spi = board.SPI()
            
            # Display configuration for the 1.8" TFT Display
            self.disp = st7735.ST7735R(
                self.spi, 
                rotation=ROTATION,
                cs=digitalio.DigitalInOut(board.CE0),
                dc=digitalio.DigitalInOut(board.D25),
                rst=digitalio.DigitalInOut(board.D22),
                baudrate=BAUDRATE,
            )
            
            # Reverse the Width/Height if the display is rotated
            if ROTATION % 180 == 90:
                self.height = self.disp.width
                self.width = self.disp.height
            else:
                self.height = self.disp.height
                self.width = self.disp.width
            
            # Enable the Backlight
            self.enableBacklight()

        # Create a new image handle
        self.image = Image.new("RGB", (self.width, self.height))

        # Get a Pixel Map Object
        self.pixels = self.image.load()
        
        # Get the drawing object from the image handle
        self.draw = ImageDraw.Draw(self.image)
        
        # Load a Font
        self.font = ImageFont.truetype("SFNS.ttf", FONTSIZE)

        # Clear the Display
        self.clearDisplay()

    
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
        # Draw to local OS
        if self.TestMode:
            self.draw.text(
                originTuple,
                text,
                font=self.font,
                fill=color[::-1],
            )
        # Draw to TFT display over SPI
        else:
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
            # Draw to local OS
            if self.TestMode:
                # The Pixels color Tuple is (R,G,B)
                self.draw.rectangle(size_tuple, fill=color_tuple[::-1])
            # Draw to TFT display over SPI
            else:
                # The TFT Library color Tuple is (B,G,R)
                self.draw.rectangle(size_tuple, fill=color_tuple)

    def update(self):
        if self.TestMode:
            # Draw to local OS
            self.image.show()
        else:
            # Draw to TFT display over SPI
            self.disp.image(self.image)

