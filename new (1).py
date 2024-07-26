from RPiMCP23S17.MCP23S17 import MCP23S17
from bitstring import BitArray
import time
import RPi.GPIO as GPIO
from flask import Flask, render_template
from logger import logger
import threading

app = Flask(__name__)

# Set the GPIO mode and warning suppression
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Define the GPIO pins
#pins = [31, 29, 11]



prev_m1_status = 4
prev_m2_status = 4
prev_m3_status = 4
prev_m4_status = 4
prev_m5_status = 4
prev_m6_status = 4

print(" I need to run only once")

m1_duration = 0
m2_duration = 0
m3_duration = 0
m4_duration = 0
m5_duration = 0
m6_duration = 0

m1_changed = time.time()
m2_changed = time.time()
m3_changed = time.time()
m4_changed = time.time()
m5_changed = time.time()
m6_changed = time.time()

m1_bw1 = False
m1_bw2 = False
m1_buzz = False

m2_bw1 = False
m2_bw2 = False
m2_buzz = False


m3_bw1 = False
m3_bw2 = False
m3_buzz = False

m4_bw1 = False
m4_bw2 = False
m4_buzz = False

m5_bw1 = False
m5_bw2 = False
m5_buzz = False

m6_bw1 = False
m6_bw2 = False
m6_buzz = False

values = [False,False,False]

m1_status = 4
m2_status = 4
m3_status = 4
m4_status = 4
m5_status = 4
m6_status = 4

prev_m1_status = 4
prev_m2_status = 4 
prev_m3_status = 4
prev_m4_status = 4
prev_m5_status = 4 
prev_m6_status = 4


m1_buzz_high_ts = 0
m1_buzz_low_ts = 0


m2_buzz_high_ts = 0
m2_buzz_low_ts=0

m3_buzz_high_ts=0
m3_buzz_low_ts=0

m4_buzz_high_ts=0
m4_buzz_low_ts=0

m5_buzz_high_ts=0
m5_buzz_low_ts=0

m6_buzz_high_ts=0
m6_buzz_low_ts=0

#global m1_buzz_high_ts,m2_buzz_high_ts,m3_buzz_high_ts,m4_buzz_high_ts,m5_buzz_high_ts,m6_buzz_high_ts
#global m1_buzz_low_ts,m2_buzz_low_ts,m3_buzz_low_ts,m4_buzz_low_ts,m5_buzz_low_ts,m5_buzz_low_ts,m6_buzz_low_ts


m6_bw1_pin = 31
m6_bw2_pin = 29
m6_buzz_pin = 11


# Setup the GPIO pins as inputs with pull-down resistors
#for pin in pins:
#   GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
GPIO.setup(m6_bw1_pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(m6_bw2_pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)    
GPIO.setup(m6_buzz_pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)    
    

mcp = MCP23S17(bus=0x00, pin_cs=0x00, device_id=0x00)
#mcp.open()
#mcp._writeRegister(0x0C, 0x00)
#mcp._writeRegister(0x0D, 0x00)

#for x in range(0, 16):
    #mcp.setDirection(x, mcp.DIR_INPUT)
    # Set pull-down mode for the pin


def ZeroPad(array):
    for x in range(array.len, 8):
        array.prepend('0b0')
    return array

def mcp_init():
    global mcp
    mcp.close()
    time.sleep(1)
    mcp = MCP23S17(bus=0x00, pin_cs=0x00, device_id=0x00)
    time.sleep(1)
    mcp.open()
    mcp._writeRegister(0x0C, 0x00)
    mcp._writeRegister(0x0D, 0x00)
    for x in range(0,16):
        mcp.setDirection(x,mcp.DIR_INPUT)


    try:
        BankA = ZeroPad(BitArray(bin(mcp._readRegister(0x12))))
    except Exception as e:
        print("An error occurred while reading BankA register:", e)
        #mcp_init()
    # You can add more specific error handling here if needed

    try:
        BankB = ZeroPad(BitArray(bin(mcp._readRegister(0x13))))
    except Exception as e:
        print("An error occurred while reading BankB register:", e)
        #mcp_init()
    
mcp_init()

def ReadGPIO():
    
    global m1_bw1,m1_bw2,m1_buzz
    global m2_bw1,m2_bw2,m2_buzz
    global m3_bw1,m3_bw2,m3_buzz
    global m4_bw1,m4_bw2,m4_buzz
    global m5_bw1,m5_bw2,m5_buzz
    global m6_bw1,m6_bw2,m6_buzz
    global values
    BankA = ZeroPad(BitArray(bin(mcp._readRegister(0x12))))
    BankB = ZeroPad(BitArray(bin(mcp._readRegister(0x13))))


    # You can add more specific error handling here if needed


    print("BankA")
    print(BankA.bin)  # show read pins for GPA0 until GPA7

    print("BankB")
    print(BankB.bin)  # show read pins for GPB0 until GPB7
    # bit_positions = range(8)

    if((str(BankA.bin) == "00000000") and (str(BankB.bin) == "00000000")):
         print("MCP ERROR READING ALL ZEROS")
         mcp_init()
    
    bitstring1 = BitArray(BankA).bin
    bitstring2 = BitArray(BankB).bin
        
    m1_bw1 = bool(bitstring1[7] == "1")
    m1_bw2 = bool(bitstring1[6] == "1") 
    #m1_buzz=bool(bitstring1[5]=="1")
    
    if(bool(bitstring1[5]=="1")):
        m1_buzz = True
        global m1_buzz_high_ts
        m1_buzz_high_ts = round(time.time())
    else:
        global m1_buzz_low_ts
        m1_buzz_low_ts = round(time.time())
        if(round(time.time())-m1_buzz_high_ts>12):
            m1_buzz = False
        else:
            m1_buzz = True
            
    
    print("m1 RAW")

    m2_bw1 = bool(bitstring1[4] == "1")
    m2_bw2 = bool(bitstring1[3] == "1")
    #m2_buzz = bool(bitstring1[2] == "1")
    
    if(bool(bitstring1[2]=="1")):
        global m2_buzz_high_ts
        m2_buzz_high_ts = round(time.time())
        m2_buzz = True
    else: 
        global m2_buzz_low_ts
        m2_buzz_low_ts = round(time.time())
        if(round(time.time())-m2_buzz_high_ts>12):
            m2_buzz = False
        else:
            m2_buzz = True
        
        
    m3_bw1 = bool(bitstring1[1] == "1")
    m3_bw2 = bool(bitstring1[0] == "1")
    #m3_buzz = bool(bitstring2[7] == "1")

    if(bool(bitstring2[7]=="1")):
        global m3_buzz_high_ts
        m3_buzz_high_ts = round(time.time())
        m3_buzz = True
    else:
        global m3_buzz_low_ts
        m3_buzz_low_ts = round(time.time())
        if(round(time.time())-m3_buzz_high_ts>12):
            m3_buzz = False
        else:
            m3_buzz = True

    
        
        
    m4_bw1 = bool(bitstring2[6] == "1")
    m4_bw2 = bool(bitstring2[5] == "1")
    #m4_buzz = bool(bitstring2[4] == "1")
    
    if(bool(bitstring2[4]=="1")):
        global m4_buzz_high_ts
        m4_buzz_high_ts = round(time.time())
        m4_buzz = True
    else:
        global m4_buzz_low_ts
        m4_buzz_low_ts = round(time.time())
        if(round(time.time())-m4_buzz_high_ts>12):
            m4_buzz = False
        else:
            m4_buzz = True
        
    m5_bw1 = bool(bitstring2[3] == "1")
    m5_bw2 = bool(bitstring2[2] == "1")
    #m5_buzz = bool(bitstring2[1] == "1")

    if(bool(bitstring2[1]=="1")):
        global m5_buzz_high_ts
        m5_buzz_high_ts = round(time.time())
        m5_buzz = True
    else:
        global m5_buzz_low_ts
        m5_buzz_low_ts = round(time.time())
        if(round(time.time())-m5_buzz_high_ts>12):
            m5_buzz = False
        else:
            m5_buzz = True
    
        
    m6_bw1 = bool(GPIO.input(m6_bw1_pin)==1)
    m6_bw2 = bool(GPIO.input(m6_bw2_pin)==1)
    #m6_buzz = bool(GPIO.input(m6_buzz_pin)==1)
    
    if(bool(GPIO.input(m6_buzz_pin)==1)):
        global m6_buzz_high_ts
        m6_buzz_high_ts = round(time.time())
        m6_buzz = True
    else:
        global m6_buzz_low_ts
        m6_buzz_low_ts = round(time.time())
        if(round(time.time())-m6_buzz_high_ts>12):
            m6_buzz = False
        else:
            m6_buzz = True
    
 
    
    print(m1_bw1,m1_bw2,m1_buzz)
    global m1_status
    if (m1_bw1 == False) and (m1_bw2 == False) and (m1_buzz == True):
        m1_status = 1
        print("m1_status = 1")
    elif (m1_bw1 == True) and (m1_bw2 == True) and (m1_buzz == True):
        m1_status = 2
        print("m1_status = 2")
    elif (m1_bw1 == False) and (m1_bw2 == True) and (m1_buzz == True): 
        m1_status = 3
        print("m1_status = 3")    
    elif (m1_bw1 == True) and (m1_bw2 == False) and (m1_buzz == True):
        m1_status = 4
        print("m1_status = 4")
    elif (m1_bw1 == False) and (m1_bw2 == True) and (m1_buzz == False):
        m1_status = 5
        print("m1_status = 5")
    elif (m1_bw1 == False) and (m1_bw2 == False) and (m1_buzz == False):
        m1_status = 6
        print("m1_status = 6")
    else:
        m1_status = 7
        print("m1_status = 7")
    
    print(m2_bw1,m2_bw2,m2_buzz)
    global m2_status
    if (m2_bw1 == False) and (m2_bw2 == False) and (m2_buzz == True):
        m2_status = 1
        print("m2_status = 1")
    elif (m2_bw1 == True) and (m2_bw2 == True) and (m2_buzz == True):
        m2_status = 2
        print("m2_status = 2")
    elif (m2_bw1 == False) and (m2_bw2 == True) and (m2_buzz == True):
        m2_status = 3
        print("m2_status = 3")
    elif (m2_bw1 == True) and (m2_bw2 == False) and (m2_buzz == True):
        m2_status = 4
        print("m2_status = 4")
    elif (m2_bw1 == False) and (m2_bw2 == True) and (m2_buzz == False):
        m2_status = 5
        print("m2_status = 5")
    elif (m2_bw1 == False) and (m2_bw2 == False) and (m2_buzz == False):
        m2_status = 6
        print("m2_status = 6")
    else:
        m2_status = 7
        print("m2_status = 7")
    
    print(m3_bw1,m3_bw2,m3_buzz)
    global m3_status
    if (m3_bw1 == False) and (m3_bw2 == False) and (m3_buzz == True):
        m3_status = 1
        print("m3_status = 1")
    elif (m3_bw1 == True) and (m3_bw2 == True) and (m3_buzz == True):
        m3_status = 2
        print("m3_status = 2")
    elif (m3_bw1 == False) and (m3_bw2 == True) and (m3_buzz == True):
        m3_status = 3
        print("m3_status = 3")
    elif (m3_bw1 == True) and (m3_bw2 == False) and (m3_buzz == True):
        m3_status = 4
        print("m3_status = 4")
    elif (m3_bw1 == False) and (m3_bw2 == True) and (m3_buzz == False):
        m3_status = 5
        print("m5_status = 5")
    elif (m3_bw1 == False) and (m3_bw2 == False) and (m3_buzz == False):
        m3_status = 6
        print("m3_status = 6")
    else:
        m6_status = 7
        print("m6_status = 7")
    
    print(m4_bw1,m4_bw2,m4_buzz)
    global m4_status
    if (m4_bw1 == False) and (m4_bw2 == False) and (m4_buzz == True):
        m4_status = 1
        print("m4_status = 1")
    elif (m4_bw1 == True) and (m4_bw2 == True) and (m4_buzz == True):
        m4_status = 2
        print("m4_status = 2")
    elif (m4_bw1 == False) and (m4_bw2 == True) and (m4_buzz == True):
        m4_status = 3
        print("m4_status = 3")
    elif (m4_bw1 == True) and (m4_bw2 == False) and (m4_buzz == True):
        m4_status = 4
        print("m4_status = 4")
    elif (m4_bw1 == False) and (m4_bw2 == True) and (m4_buzz == False):
        m4_status = 5
        print("m4_status = 5") 
    elif (m4_bw1 == False) and (m4_bw2 == False) and (m4_buzz == False):
        m4_status = 6
        print("m4_status = 6")
    else:
        m4_status = 7
        print("m4_status = 7")
    
    print(m5_bw1,m5_bw2,m5_buzz)
    global m5_status
    if (m5_bw1 == False) and (m5_bw2 == False) and (m5_buzz == True):
        m5_status = 1
        print("m5_status = 1")
    elif (m5_bw1 == True) and (m5_bw2 == True) and (m5_buzz == True):
        m5_status = 2
        print("m5_status = 2")
    elif (m5_bw1 == False) and (m5_bw2 == True) and (m5_buzz == True):
        m5_status = 3
        print("m5_status = 3")
    elif (m5_bw1 == True) and (m5_bw2 == False) and (m5_buzz == True):
        m5_status = 4
        print("m5_status = 4")
    elif (m5_bw1 == False) and (m5_bw2 == True) and (m5_buzz == False):
        m5_status = 5
        print("m5_status = 5")
    elif (m5_bw1 == False) and (m5_bw2 == False) and (m5_buzz == False):
        m5_status = 6
        print("m5_status = 6")
    else:
        m5_status = 7
        print("m5_status = 7")
    
    print(m6_bw1,m6_bw2,m6_buzz)
    if (m6_bw1 == False) and (m6_bw2 == False) and (m6_buzz == True):
        m6_status = 1
        print("m6_status = 1")
    elif (m6_bw1 == True) and (m6_bw2 == True) and (m6_buzz == True):
        m6_status = 2
        print("m6_status = 2")
    elif (m6_bw1 == False) and (m6_bw2 == True) and (m6_buzz == True):
        m6_status = 3
        print("m6_status = 3")
    elif (m6_bw1 == True) and (m6_bw2 == False) and (m6_buzz == True):
        m6_status = 4
        print("m6_status = 4")
    elif (m6_bw1 == False) and (m6_bw2 == True) and (m6_buzz == False):
        m6_status = 5
        print("m6_status = 5")
    elif (m6_bw1 == False) and (m6_bw2 == False) and (m6_buzz == False):
        m6_status = 6
        print("m6_status = 6")
    else:
        m6_status = 7
        print("m6_status = 7")
    
    global prev_m1_status
    global m1_changed
    if(m1_status != prev_m1_status):
        m1_changed  = time.time()
        prev_m1_status = m1_status
    global prev_m2_status
    global m2_changed
    if(m2_status != prev_m2_status):
        m2_changed  = time.time()   
        prev_m2_status = m2_status
    global prev_m3_status
    global m3_changed
    if(m3_status != prev_m3_status):
        m3_changed  = time.time()   
        prev_m3_status = m3_status
    global prev_m4_status
    global m4_changed
    if(m4_status != prev_m4_status):
        m4_changed  = time.time()   
        prev_m4_status = m4_status
    global prev_m5_status
    global m5_changed
    if(m5_status != prev_m5_status):
        m5_changed  = time.time()   
        prev_m5_status = m5_status
    global prev_m6_status
    global m6_changed
    if(m6_status != prev_m6_status):
        m6_changed  = time.time()
        prev_m6_status = m6_status
        
    global m1_duration
    m1_duration = int((time.time() - m1_changed)/60)
    global m2_duration
    m2_duration = int((time.time() - m2_changed)/60)
    global m3_duration
    m3_duration = int((time.time() - m3_changed)/60)
    global m4_duration
    m4_duration = int((time.time() - m4_changed)/60)
    global m5_duration
    m5_duration = int((time.time() - m5_changed)/60)
    global m6_duration
    m6_duration = int((time.time() - m6_changed)/60)
    
    print(m1_duration,m2_duration,m3_duration,m4_duration,m5_duration,m6_duration)
    
    return m1_status, m2_status, m3_status, m4_status, m5_status, m6_status, m1_duration, m2_duration, m3_duration, m4_duration, m5_duration, m6_duration



@app.route("/")
def index():
    m1_status, m2_status, m3_status, m4_status, m5_status, m6_status,m1_duration,m2_duration,m3_duration,m4_duration,m5_duration,m6_duration = ReadGPIO()
    return render_template("new.html", m1_status=m1_status, m2_status=m2_status, m3_status=m3_status,
                           m4_status=m4_status, m5_status=m5_status, m6_status=m6_status,
                           m1_duration=m1_duration,m2_duration=m2_duration,m3_duration=m3_duration,m4_duration=m4_duration,m5_duration=m5_duration,m6_duration=m6_duration)

def gpio_thread_function():
    while True:
        try:
            ReadGPIO()
            time.sleep(5)
            assert time.sleep(5)
        except KeyboardInterrupt:
            GPIO.cleanup()
      # Adjust the delay as needed
    
# Create a thread for the GPIO function and start it
gpio_thread = threading.Thread(target=gpio_thread_function)
gpio_thread.start()



if __name__ == "__main__":
    app.run(host='172.27.203.154', port=6001,debug=True)
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    #while True:
        #try:
           # ReadGPIO()
        #print("Pin values:", values)
            #time.sleep(2)
       # except KeyboardInterrupt:
    # Clean up GPIO on program exit 
    