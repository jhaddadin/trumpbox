import machine
import ssd1306
import writer
import inconsolata14
import freesans20

class Hardware:

    # Constructor initializes all the hardware objects

    def __init__(self):
        self.i2c = machine.I2C(-1, machine.Pin(5), machine.Pin(4))
        self.oled = ssd1306.SSD1306_I2C(128,64,self.i2c)
        self.inc14 = writer.Writer(self.oled, inconsolata14)
        self.free20 = writer.Writer(self.oled, freesans20)
        self.inc14.set_clip(True,True)
    
