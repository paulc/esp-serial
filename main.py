import network,socket,os,select,machine,time

@micropython.native
def loop(port,baudrate=9600,debug=False,buflen=32,rxbuf=32):
    try:
        uart = machine.UART(0,rxbuf=rxbuf)
        uart.init(baudrate=baudrate)
        os.dupterm(None, 1) 
        s = socket.socket()
        s.bind(('0.0.0.0',port))
        s.listen(0)
        buf = bytearray(buflen)
        mbuf = memoryview(buf)
        while True:
            try:
                if debug:
                    print('[+] Listening:', port)
                client,addr = s.accept()
                if debug:
                    print('[+] Connection:', addr)
                p = select.poll()
                p.register(uart,select.POLLIN)
                p.register(client,select.POLLIN)
                closed = False
                while not closed:
                    for (device,_) in p.ipoll():
                        if device == client:
                            data = client.recv(64)
                            if len(data) == 0:
                                if debug:
                                    print('[-] Client disconnected')
                                client.close()
                                closed = True
                            else:
                                uart.write(data)
                        if device == uart:
                            buflen = uart.readinto(mbuf)
                            if debug:
                                print(">>",buf[:buflen])
                            client.write(mbuf[:buflen])
            except Exception as e:
                if debug:
                    print(str(e))
                pass
    finally:
        os.dupterm(uart, 1) 
        s.close()

for i in range(5,0,-1):
    print('Disabling REPL ({} secs)\r'.format(i),end='')
    time.sleep(1)

os.dupterm(None, 1) # disable REPL on UART(0)

loop(port=1234,baudrate=19200)
