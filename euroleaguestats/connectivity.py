import socket


from jnius import autoclass


def resolve_connectivity():

    available_net = check_network_availability()

    if available_net:
        available_site = is_connected('www.euroleague.net')

        if available_site:
            return True
        else:
            message = 'euroleague.net could not be reached. Please, check your network connection.'
            return message

    else:
        message = 'Could not detect any network. Please, connect to a network first.'
        return message


def check_network_availability():

    Context = autoclass('android.content.Context')
    NetworkCapabilities = autoclass('android.net.NetworkCapabilities')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    activity = PythonActivity.mActivity

    '''Create an instance of :cls: ConnectivityManager'''
    con_mgr = activity.getSystemService(Context.CONNECTIVITY_SERVICE)

    '''Return the Network object corresponding to the currently active default data network.'''
    network = con_mgr.getActiveNetwork()

    '''Call the NetworkCapabilities java class for our current Network object.'''
    capabilities = con_mgr.getNetworkCapabilities(network)

    '''Check if the Network object is not null and verify the type of available network.'''
    if capabilities is not None and (
            capabilities.hasTransport(NetworkCapabilities.TRANSPORT_WIFI) or capabilities.hasTransport(
            NetworkCapabilities.TRANSPORT_CELLULAR)):
        return True
    return False


def is_connected(hostname):

    """Called by :cls: 'Standings' - main.py."""

    try:
        '''see if we can resolve the host name -- tells us if there is
        a DNS listening
        '''
        host = socket.gethostbyname(hostname)

        '''connect to the host -- tells us if the host is actually
        reachable -- Port: 80 = HTTP, 53 = DNS, 10 sec = timeout
        :meth: gethostbyname returns an IPv4 address (numeric)
        '''
        s = socket.create_connection((host, 80), 10)
        '''2 = SHUT_RDWR'''
        s.shutdown(2)
        s.close()
        return True

    except OSError:
        pass
    return False
