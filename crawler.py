import os
from utils import isGoodIPv4, rest_get, wait, clear, get_arb_value
from time import sleep

#ping
def ping(ip):
    return not os.system('ping %s -n 1 > NUL' % (ip,))

# registry address
def set_registry_address(ip, port):
    conn=f'http://{ip}:{port}/x-nmos/query/'
    return conn

# user inputs for connection
# user sets valid IPv4
def connection_inputs():
    ip_loop=True
    while ip_loop:
        ip_add=input('Set IP address of NMOS registry: ')
        if isGoodIPv4(ip_add)==True:
            if ping(ip_add)==True:
                
                ip_loop = False
            else:
                print('IP address unreachable')
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

# set version
def version(conn):
    ver_list=['v1.0', 'v1.1', 'v1.2', 'v1.3']
    ver_loop=True
    while ver_loop:
        clear()
        print(conn)
        print()
        i=0
        print('Set version:')
        for item in ver_list:
            print(f' [{i+1}] {item}')
            i+=1
        
        print(' [.]')
        print(' [0] Cancel')
        print()
        
        try:
            opt = int(input('Select an option: '))
            if opt==0: ver_loop=False
            else: return conn+ver_list[opt-1]+'/'
        except ValueError:
            print('Invalid option')
            sleep(1)

# devices
def device_list(conn):
    device_loop = True
    while device_loop:
        clear()
        print(conn+'devices/')
        print()
        i=0
        device_list=rest_get(conn+'devices/')
        for device in device_list:
            print(f' [{i+1}] {device["description"]}')
            i+=1
        
        print(' [.]')
        print(' [0] Cancel')
        print()
        
        try:
            opt = int(input('Select an option: '))
            if opt==0: device_loop=False
            else:
                device = {'id': device_list[opt-1]['id'], 'description': device_list[opt-1]['description'], 'node_id': device_list[opt-1]['node_id'], 'label': device_list[opt-1]['label']}
                return device
        except ValueError:
            print('Invalid option')
            sleep(1)

# nodes
def node(conn, node_id):
    data = rest_get(f'{conn}nodes/')
    return data

# senders
def senders(conn, node):
    senders_loop = True
    while senders_loop:
        clear()
        print(f'{conn}senders/{node}')
        print()
        i=0
        node_list=[]
        senders_list=rest_get(conn+'senders/?paging.order=update&paging.limit=10000')
        for sender in senders_list:
            if sender['node_id']==node:
                node_list.append(sender)
                tag = get_arb_value(sender["tags"])
                tag = tag[0]
                #print(f' [{i+1}] {tag}')
                i+=1
        
        node_list = sorted(node_list, key=lambda d: get_arb_value(d['tags']))
        i=0
        for j in node_list:
            tag = get_arb_value(j["tags"])
            tag = tag[0]
            print(f' [{i+1}] {tag}')
            i+=1
            
        print(' [.]')
        print(' [0] Cancel')
        print()
            
        try:
            opt = int(input('Select a sender: '))
            if opt==0: senders_loop=False
            else:
                sender = {'label': node_list[opt-1]['label'], 'description': node_list[opt-1]['description'], 'manifest_href': node_list[opt-1]['manifest_href'], 'flow_id': node_list[opt-1]['flow_id'], 'id': node_list[opt-1]['id'], 'device_id': node_list[opt-1]['device_id'], 'grouphint': get_arb_value(node_list[opt-1]['tags'])}
                return sender
        except:
            print('Invalid option')
            sleep(1)

# get sdp
def get_sdp(href):


if __name__ == "__main__":
    conn = connection_inputs()
    
    # access top layer of api
    #top_options = rest_get(conn)
    # need test for NMOS connection
    #d = next_api_access(conn, top_options)


    # select NMOS version - needs to be a top menu item
    ver=version(conn)

    # select device
    device=device_list(ver)

    node_id=device['node_id']
    #data = node(ver, node_id)

    # get sender info
    senders(ver, node_id)
