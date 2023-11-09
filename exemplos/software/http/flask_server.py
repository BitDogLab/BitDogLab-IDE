import time
from flask import Flask, render_template
import ahtx0
from ssd1306 import SSD1306_I2C
from machine import Pin, SoftI2C, PWM

app = Flask(__name__)

@app.route('/index/<temp>') #website says that the variable <temp> would be passed into the index function

def index(temp): #website said I needed this so that the temp variable would be returned
    
    i2c_oled = SoftI2C(scl=Pin(15), sda=Pin(14))
    oled = SSD1306_I2C(128, 64, i2c_oled)
    
    # Configuração Sensor AHT10/AHT20
    i2c_sensor = SoftI2C(scl=Pin(3), sda=Pin(2))
    sensor = ahtx0.AHT10(i2c_sensor)

    
    while True:
        temperature = sensor.temperature
        humidity = sensor.relative_humidity
        if humidity is not None and temperature is not None:
            temperature = temperature * 1.8 +32 #convert from C to F
            print('Temp={0:0.1f}*F Humidity={1:0.1f}%'.format(temperature, humidity))
            temperature = '%.2f'%(temperature)
            humidity = '%.2f'%(humidity)
            
            tempReading = str(temperature) 
            templateData = {'temp'  : tempReading
            }
            return render_template('index.html', **templateData)
            
        else:
            print('Failed to get DHT22 Reading, trying again in seconds')
            
            time.sleep(1)

if __name__== '__main__':
    app.run(debug=True, host='127.0.0.1')
    
   