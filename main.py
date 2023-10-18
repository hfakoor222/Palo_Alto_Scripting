import json
import re
import netmiko
from netmiko import ConnectHandler
from ConnectionHandler import Connection
import time

profile_list = []
ip_address = []
connections = []
connection_parameters = []

while True:
    result = input("Will you be updating one or more than one device? Type:  O for one M for more")
    if result.lower() == "m":
        Connection.MultiConnect(connection_parameters)
        break
    elif result.lower() == "o":
        Connection.SingleConnect(connection_parameters)
        break
for i in connection_parameters:
    print(i)

    conn = netmiko.ConnectHandler(device_type=i[0], host = i[1], username = i[2], password = i[3])
    conn.config_mode()
    time.sleep(1)
    connections.append(conn)
    output = conn.send_command("show network profiles interface-management-profile",  delay_factor=3) #cmd_verify = False
    print(str(i[1]) + "\n" +   str(output))

print("Now we will enter permitted Ip Addresses for the interfaces")

def main_function():
    global ip_update_list
    while True:
        res = input("Please enter a profile to update")
        profile_list.append(res)
        skip = input("Continue more profiles? Y|N")
        if skip.lower() == "y":
            continue
        while True:
            res = input("Is this a list of permitted-IP addresses or a single IP address: Type  List|Single")
            if res.lower() !="single":
                if res.lower() != "list":
                    continue
            if res.lower() == "list":
                lres = ("Please enter the ip addresses in list form [ip_1, ip_2, ip_3]")
                ip_update_list = lres.strip("][").split(",")
                print("List of permitted-ip's to be updated  :" + str(ip_update_list))
                return ip_update_list #this is the list of permitted-ip addresses

            if res.lower() == "single":
                res = input('Please enter the permitted-ip address with subnets and brackets:  example:  ["100.100.100.100/24"]')
                ip_update_list = json.loads(res)
                print("List of permitted-ip's to be updated  :" + str(ip_update_list))
                print(ip_update_list)
                return ip_update_list

main_function()
for i in connections:
    for profile in profile_list:
        print(profile)
        for ip in ip_update_list:
            print(ip)
            res = i.send_command("set network profiles interface-management-profile Inside permitted-ip " + ip)

    # i.send_command("commit")
    result = i.send_command("show network profiles interface-management-profile")
    print(result)
    i.disconnect()
