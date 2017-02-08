import network
import time
import hardware

def main():
    hw = hardware.Hardware()
    hw.free20.set_textpos(16,16)
    hw.free20.printstring('TrumpBox')
    for i in range(100):
        hw.oled.pixel((13+i),11,1)
        hw.oled.pixel((13+i),39,1)
        hw.oled.show()
    for i in range(255):
        hw.oled.contrast(255-i)
        time.sleep(0.005)
    hw.oled.fill(0)
    hw.oled.show()

    sta = network.WLAN(network.STA_IF)
    ap = network.WLAN(network.AP_IF)
    
    while True:
        sta.active(True)
        starting_time = time.time()
        while not sta.isconnected() and (time.time() - starting_time) < 10:
            pass
        if not sta.isconnected():
            time.sleep(5)
            import networkconfig
            networkconfig.start(hw)
            ap.active(False)
        else:
            time.sleep(5)
            import trumpbox
            trumpbox.blather(hw)


