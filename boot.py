import esp,gc,os,machine,network,time,webrepl

def connect_wifi(network,password):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(network,password)
        while not sta_if.isconnected():
            pass
    ifconfig = sta_if.ifconfig()
    return ifconfig

esp.osdebug(None)

try:
    (ssid,pw,repl_pw) = [s.rstrip() for s in open('config.txt').readlines()]
except:
    ssid    = input("SSID: ")
    pw      = input("Network Password: ")
    repl_pw = input("WebREPL Password: ")
    with open('config.txt','w') as f:
        f.write('{}\n{}\n{}\n'.format(ssid,pw,repl_pw))

ifconfig = connect_wifi(ssid,pw)
webrepl.start(password=repl_pw)
gc.collect()
