"""
Autor: Max Kohnen
Klasse: ETS23
Datum: 05.12.2023
Funktionsbeschreibung:
Das Programm zeigt die Temperatur und die Luftfeuchtigkeit auf einem Display an.
Die Steuerung muss vorher über den Taster eingeschaltet werden.
Die Steuerung lässt sich durch den Taster an und aus schalten.
Version: 0.2; 05.12.2023
Hardware: ESP32 USB-C; AHT10 - Sensor; LCD - Display 240 x 280; 1x LED - rot; 1x LED - gruen; 1x 5.1KOhm Widerstand; 2x 330Ohm Widerstand

Anschlüsse: Display:
            GND: GND
            VCC: 3.3V
            SCL:  13
            SDA:  11
            RES:   5
            DC:    4
            CS:
            BLK: 3.3V
            
            AHT10:
            VCC: 3.3V
            GND: GND
            SCL:   9
            SDA:   8
            
            Taster:
            1. Pin: 3.3V
            2. Pin: 7 / 5.1KOhm auf GND(Pulldown)
            
            LED rot:
            GND
            6 / 330 Ohm
            
            LED gruen:
            GND
            21 / 330 Ohm
            
            

Bibliotheken: AHTx0: https://github.com/targetblank/micropython_ahtx0
              st7789: https://github.com/russhughes/st7789_mpy
"""

import uos
import machine
import st7789py as st7789
import vga1_16x32 as font
import utime
from machine import Pin, I2C
import ahtx0

# Pin-Definitionen für das ST7789-Display und Initialisierung
st7789_res = 5
st7789_dc = 4
#blk_pwm = 6 # PWM Pin
pin_st7789_res = machine.Pin(st7789_res, machine.Pin.OUT)
pin_st7789_dc = machine.Pin(st7789_dc, machine.Pin.OUT)
pin_rot_led = machine.Pin(6, machine.Pin.OUT)
pin_gruen_led = machine.Pin(21, machine.Pin.OUT)
taster = machine.Pin(7, machine.Pin.IN)
letzter_taster_status = taster.value() # Status Variable des letzten Tasterzustands
power_an = False # power on Status Variable

#pin_blk_pwm = machine.PWM(blk_pwm)

# Display-Abmessungen
disp_width = 240
disp_height = 280
CENTER_Y = int(disp_width / 2)
CENTER_X = int(disp_height / 2)

# SPI-Konfiguration
pin_spi2_sck = machine.Pin(13, machine.Pin.OUT)
pin_spi2_mosi = machine.Pin(11, machine.Pin.OUT)
pin_spi2_miso = machine.Pin(19, machine.Pin.IN)
spi2 = machine.SPI(2, sck=pin_spi2_sck, mosi=pin_spi2_mosi, miso=pin_spi2_miso,
                   baudrate=40000000, polarity=1, phase=0, bits=8)

# Display- und Temperatursensor-Initialisierung
display = st7789.ST7789(spi2, disp_width, disp_width,
                         reset=pin_st7789_res,
                         dc=pin_st7789_dc,
                         xstart=0, ystart=0, rotation=3)

i2c = I2C(scl=Pin(9), sda=Pin(8))
sensor = ahtx0.AHT10(i2c)
#bh1750 = BH1750(0x23, i2c)

#__________________________________________________________________________________
# Display löschen
display.fill(st7789.BLACK)
# display.text(font, "Temperatur:", 10, 20)
# display.text(font, "Luftfeuchtigkeit:", 10, 90)
#___________________________________________________________________________________

# Hauptprogramm
while True:
    
    temperatur = sensor.temperature
    luftfeuchtigkeit = sensor.relative_humidity
    
    aktueller_taster_status = taster.value() # der aktuelle Taster Zustand wird in die aktueller_taster_status Variable geschrieben
    utime.sleep(0.2) # Zeit zum entprellen des Tasters 
    if aktueller_taster_status and not letzter_taster_status: # Es wird verglichen, ob der aktuelle_taster_status dem letzten_taster_status entspricht. Wenn nicht dann geht es weiter
        power_an = not power_an
    
        if temperatur >= 25 or luftfeuchtigkeit >= 60:
            display.text(font, "Temperatur:", 10, 20)
            display.text(font, "Luftfeuchtigkeit:", 10, 90)
        elif temperatur < 25 or luftfeuchtigkeit < 60:
            display.text(font, "Temperatur:", 10, 20)
            display.text(font, "Luftfeuchtigkeit:", 10, 90)
            
    if power_an == True:  # Funktionen werden nur ausgeführt, wenn power_an True ist
        
        # Temperatur und Luftfeuchtigkeit anzeigen
        display.text(font, "%.2f °C" % temperatur, 10, 50)
        display.text(font, "%.2f %%" % luftfeuchtigkeit, 10, 120)
        
        if temperatur >= 25 or luftfeuchtigkeit >= 60: # rote LED einschalten, gruene LED ausschalten wenn temp >= 25 Grad Celsius und luftf. >= 60 %
            pin_gruen_led.off()
            pin_rot_led.on()
            utime.sleep(0.1)
            pin_rot_led.off()
        elif temperatur < 25 or luftfeuchtigkeit < 60: # gruene LED einschalten, rote LED ausschalten wenn temp < 25 Grad Celsius und luftf. < 60 %
            pin_rot_led.off()
            pin_gruen_led.on()
            
    elif power_an == False: # Wenn die Steuerung über den Taster ausgeschaltet wurde, dann ...
        
        # Display löschen
        display.fill(st7789.BLACK)
        
        # leds ausschalten
        pin_rot_led.off()
        pin_gruen_led.off()
        
    letzter_taster_status = aktueller_taster_status # der letzte Taster Status wird auf den aktuellen Taster Zustand gesetzt
    utime.sleep(0.1) # kurze Pause um die CPU zu entlasten