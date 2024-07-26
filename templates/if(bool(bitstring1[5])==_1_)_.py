if(bool(bitstring1[5])=="1"):
        m1_buzz_high_ts=int(time.time())
        print(m1_buzz_high_ts)
        print("high")
    else:   
        m1_buzz_low_ts=int(time.time())
        print(m1_buzz_low_ts)
        print("low")
    if(max(m1_buzz_high_ts,m1_buzz_low_ts)-min(m1_buzz_high_ts,m1_buzz_low_ts)<11000):
        m1_buzz = True
        print("Blinking took as high")

    else:
        m1_buzz= False
        print("No Blink OFF")