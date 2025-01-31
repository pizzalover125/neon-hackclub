import requests
import time
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio
from adafruit_display_text import label

class LEDMatrixDisplay:
    def __init__(self):
        displayio.release_displays()
        self.setup_matrix()
        self.setup_display()
        self.setup_logo()
        
    def setup_matrix(self):
        self.matrix = rgbmatrix.RGBMatrix(
            width=64, height=32, bit_depth=1,
            rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
            addr_pins=[board.A5, board.A4, board.A3, board.A2],
            clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1
        )
        
    def setup_display(self):
        self.display = framebufferio.FramebufferDisplay(self.matrix, auto_refresh=False)
        self.main_group = displayio.Group()
        self.display.root_group = self.main_group
        
    def setup_logo(self):
        LOGO_BITMAP = displayio.Bitmap(12, 12, 3)
        LOGO_PALETTE = displayio.Palette(3)
        LOGO_PALETTE[0] = 0x000000  
        LOGO_PALETTE[1] = 0xFF0000  
        LOGO_PALETTE[2] = 0xFFFFFF  
        logo_pattern = [
            "111111111111",
            "111111111111",
            "111111111111",
            "111221111111",
            "111221111111",
            "111222221111",
            "111221122111",
            "111221122111",
            "111221122111",
            "111221122111",
            "111111111111",
            "111111111111"
        ]
        
        for y in range(len(logo_pattern)):
            for x in range(len(logo_pattern[y])):
                if logo_pattern[y][x] == "1":
                    LOGO_BITMAP[x, y] = 1
                elif logo_pattern[y][x] == "2":
                    LOGO_BITMAP[x, y] = 2
                    
        self.logo_grid = displayio.TileGrid(LOGO_BITMAP, pixel_shader=LOGO_PALETTE)
        self.logo_grid.x = 4
        self.logo_grid.y = (self.display.height - 12) // 2
        
    def display_number(self, number):
        while len(self.main_group) > 0:
            self.main_group.pop()
        
        self.main_group.append(self.logo_grid)
        
        text = str(number)
        text_area = label.Label(
            terminalio.FONT,
            text=text,
            color=0xFFFFFF
        )
        
        text_area.anchor_point = (0.5, 0.5)
        text_area.anchored_position = (
            (self.display.width * 3) // 5, 
            self.display.height // 2       
        )
        self.main_group.append(text_area)
        self.display.auto_refresh = True

def get_total_members():
    response = requests.get("https://hackclub.com/api/slack/").json()
    return response["total_members_count"]

def main():
    display = LEDMatrixDisplay()
    last_count = None
    
    while True:
        try:
            count = get_total_members()
            if count is not None:
                if count != last_count:  
                    display.display_number(count)
                    last_count = count
                    
            time.sleep(300)

if __name__ == "__main__":
    main()