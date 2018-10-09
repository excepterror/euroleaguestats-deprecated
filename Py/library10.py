import socket


def is_connected(hostname):
    # Called by :cls: 'Standings' - main.py.
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(hostname)
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 80), 2)
        s.shutdown(2)
        s.close()
        return True
    except:
        pass
    return False
