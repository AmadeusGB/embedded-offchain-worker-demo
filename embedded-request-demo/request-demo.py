import RPi.GPIO as GPIO
import LCD1602    # LCD1602液晶显示屏库
import time
import json
import substrateinterface
from scalecodec.type_registry import load_type_registry_file

colors1 = [0x0000FF, 0xFF00FF]
makerobo_BtnPin = 12
makerobo_R = 15
makerobo_G = 16
makerobo_B = 18


def makerobo_setup(Rpin, Gpin, Bpin):
    global pins
    global p_R, p_G, p_B
    pins = {'pin_R':Rpin, 'pin_G':Gpin, 'pin_B':Bpin}
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    for i in pins:
        GPIO.setup(pins[i], GPIO.OUT)
        GPIO.output(pins[i], GPIO.LOW)

    p_R = GPIO.PWM(pins['pin_R'], 2000)
    p_G = GPIO.PWM(pins['pin_G'], 1999)
    p_B = GPIO.PWM(pins['pin_B'], 5000)

    GPIO.setup(makerobo_BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(makerobo_BtnPin, GPIO.BOTH, callback=makerobo_detect, bouncetime=200)

    p_R.start(0)
    p_G.start(0)
    p_B.start(0)

    LCD1602.makerobo_init(0x27, 1)
    #LCD1602.makerobo_write(0, 0, 'Hello!!!')
    #LCD1602.makerobo_write(0, 1, 'Raspberry')

def set_colorLED(x):
    if x == 0:
        while True:
            makerobo_set_Color(0x00FFFF)

def makerobo_pwm_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def makerobo_detect(chn):
    set_colorLED(GPIO.input(makerobo_BtnPin))

def makerobo_set_Color(col):
    R_val = (col & 0xff0000) >> 16
    G_val = (col & 0x00ff00) >> 8
    B_val = (col & 0x0000ff) >> 0

    R_val = makerobo_pwm_map(R_val, 0, 255, 0, 100)
    G_val = makerobo_pwm_map(G_val, 0, 255, 0, 100)
    B_val = makerobo_pwm_map(B_val, 0, 255, 0, 100)

    p_R.ChangeDutyCycle(100-R_val)
    p_G.ChangeDutyCycle(100-G_val)
    p_B.ChangeDutyCycle(100-B_val)

def makerobo_loop():
    substrate = substrateinterface.SubstrateInterface(
    url="http://127.0.0.1:9933",
    address_type=42,
    type_registry=load_type_registry_file("/home/ubuntu/project/raspberrydemo/lcd3/customSpec.json"),
)

    currentblock = 0
    while True:  
        blockinfo = substrate.get_runtime_block()
        data1 = json.dumps(blockinfo)
        data2 = json.loads(data1)
        blocknumber = data2['block']['header']['number']
        if blocknumber == currentblock:
            makerobo_set_Color(0xFF00FF)
        else:
            makerobo_set_Color(0x0000FF)

        blocknumberstr = str(blocknumber)
        blockshow = 'block:' + blocknumberstr
        LCD1602.makerobo_write(0,0,blockshow)
        now = time.strftime('%m/%d %H:%M:%S', time.localtime(time.time()))
        LCD1602.makerobo_write(0, 1, now)
        time.sleep(0.2)
        currentblock = blocknumber
        #LCD1602.makerobo_clear()

def makerobo_off():
    GPIO.setmode(GPIO.BOARD)
    for i in pins:
        GPIO.setup(pins[i], GPIO.OUT)
        GPIO.output(pins[i], GPIO.LOW)

def makerobo_destroy():
    p_G.stop()
    p_R.stop()
    p_B.stop()
    makerobo_off()
    GPIO.cleanup()
    pass	

if __name__ == "__main__":
    try:
        makerobo_setup(makerobo_R, makerobo_G, makerobo_B)
        makerobo_loop()
	#makerobo_loop()
    except KeyboardInterrupt:
        makerobo_destroy()
