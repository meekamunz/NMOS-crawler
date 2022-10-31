from utils import isGoodIPv4, rest_get, wait, clear
from time import sleep

# registry address
def set_registry_address(ip, port):
    conn=f'http://{ip}:{port}/'
    return conn

# user inputs for connection
# user sets valid IPv4
def connection_inputs():
    ip_loop=True
    while ip_loop:
        ip_add=input('Set IP address of NMOS registry: ')
        if isGoodIPv4(ip_add)==True:
            ip_loop = False
        else:
            print('Invalid IP')
            wait()
            
    # user sets valid port
    port_loop=True
    while port_loop:
        try:
            port=int(input('Enter the port number for the NMOS registry: '))
            port_loop=False
        except ValueError:
            print('Invalid port')
            wait()
        
    conn = set_registry_address(ip_add, port)
    return conn

# take choices, make next connection
def next_api_access(conn, options):
    choice_loop=True
    data={'reponse':'empty', 'close':False}
    if data['close']==False:
        while choice_loop:
            clear()
            print(conn)
            print()
            i=1
            print('API Response: ')
            for item in options:
                print(f' [{i}] {item}')
                i+=1
                
            print(' [.]')
            print(' [0] Return this data')
            print()
            
            try:
                opt = int(input('Select an option: '))
                if opt==0:
                    clear()
                    data={'response':options, 'close':True}
                    choice_loop=False
                else:
                    choice=options[opt-1]
                    new_conn = f'{conn}{choice}'
                    next_option = rest_get(new_conn)
                    data = {'response':next_api_access(new_conn, next_option), 'close':False}
                    return data['response']
            except ValueError:
                print('Invalid option')
                sleep(1)
    
    return(data['response'])

if __name__ == "__main__":
    conn = connection_inputs()
    
    # access top layer of api
    top_options = rest_get(conn)
    # need test for NMOS connection
    d = next_api_access(conn, top_options)