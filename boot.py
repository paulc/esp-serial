import esp,gc,json,network,webrepl

def disable_ap():
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)

def enable_ap(ap_ssid,ap_pw,ap_ifconfig=None):
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(True)
    ap_if.config(essid=ap_ssid, password=ap_pw)
    if ap_ifconfig:
        ap_if.ifconfig(ap_ifconfig)
    return ap_if.ifconfig()

def disable_sta():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(False)

def enable_sta(sta_ssid,sta_pw):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(sta_ssid,sta_pw)
        while not sta_if.isconnected():
            pass
    return sta_if.ifconfig()

def save_config(config):
    with open('config.json','w') as f:
        json.dump(config,f)

def get_config():
    try:
        with open('config.json') as f:
            return json.load(f)
    except:
        config = dict()
        if input('Enable AP [y/n]: ').lower() == 'y':
            config['ap_ssid'] = input('AP SSID: ')
            config['ap_pw'] = input('AP Password: ')
        if input('Enable STA [y/n]: ').lower() == 'y':
            config['sta_ssid'] = input('STA SSID: ')
            config['sta_pw'] = input('STA Password: ')
        if input('Enable WebREPL [y/n]: ').lower() == 'y':
            config['webrepl_pw'] = input('WebREPL Password: ')
        save_config(config)
        return config

esp.osdebug(None)
config = get_config()

if 'ap_ssid' in config:
    enable_ap(config['ap_ssid'],config['ap_pw'],config.get('ap_ifconfig',None))
else:
    disable_ap()

if 'sta_ssid' in config:
    enable_sta(config['sta_ssid'],config['sta_pw'])
else:
    disable_sta()

if 'webrepl_pw' in config:
    webrepl.start(password=config['webrepl_pw'])

gc.collect()

