## This is a simple connection API. normally we would have an encrypted list of firewalls with username/password to use.


import json
import netmiko

class Connection():
    def __init__(self):
        pass
    def MultiConnect(connection_parameters = []):
        while True:
            def params():
                connection_parameters.clear()
                conn = input("Please enter a list of lists for  of connection parameters: device_type,  firewall IP addresses, username, pass" + "\n example:  ['paloalto_panos', '10.1.x.x', 'username', 'password']")
                res = json.loads(conn)
                [connection_parameters.append(i) for i in res]
                print(connection_parameters)
            conn = params()
            res = input("is the list formatted properly:  Type Y|N")
            if res.lower() == "y":
                break
    def SingleConnect(connection_parameters = []):
        while True:
            connection_parameters.clear()
            conn = input("Please enter a single list of parameters for a single connection instance")
            if conn == "":
                continue
            try:
                conn = json.loads(conn)
            except:
                print("enter a properly fomatted list")
                continue
            print("Here is your list:    " + str(conn))
            res = input("is the list formatted properly:  Type Y|N")
            if res.lower() == "y":
                connection_parameters.append(conn)
                return connection_parameters
            if len(connection_parameters)  > 0:
                break

