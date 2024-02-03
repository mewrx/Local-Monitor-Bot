from platform import system
from socket import *
from subprocess import check_output
import os
import subprocess
import scapy.all as sc


def local_ipv4():
    """Getting local IP address from ARP scan"""
    st = socket(AF_INET, SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        ip_l = st.getsockname()[0]
    except Exception:
        ip_l = '127.0.0.1'
    finally:
        st.close()
    return ip_l


def get_gateway_win():
    """Getting local gateway. Code for Windows"""
    com = f'route PRINT 0* | findstr {local_ipv4()}'.split()
    return check_output(com, shell=True).decode('cp866').split()[2]


def get_gateway_linx():
    """Getting local gateway. Code for linux"""
    com = 'route -n'.split()
    ip_route = str(subprocess.check_output(com, shell=True)).split("\\n")[2].split()[1].strip()
    if ip_route.isdigit():
        return ip_route
    else:
        sock = gethostbyname(ip_route)
        return sock


def get_ip_mac_network(ip):
    """ARP scanning on local network. Return dict of MAC and IP address."""
    answered_list = sc.srp(sc.Ether(dst='ff:ff:ff:ff:ff:ff') / sc.ARP(pdst=ip), timeout=1, verbose=False)[0]
    clients_list = []
    for element in answered_list:
        clients_list.append({'ip': element[1].psrc, 'mac': element[1].hwsrc})
    return clients_list


def print_ip_mac(mac_ip_list):
    print(f"\nMachine in Network:\n\nIP\t\t\tMAC-address\n{'-' * 41}")
    for client in mac_ip_list:
        print(f'{client["ip"]}\t\t{client["mac"]}')


def main():
    local_ip = local_ipv4()

    if system() == "Windows":
        gateway = get_gateway_win()
    elif system() == 'Linux':
        if not os.getuid() == 0:
            print('\n[+] run with sudo!\n')
            return
        gateway = get_gateway_linx()

    ip_mac_network = get_ip_mac_network(
        f'{local_ip.split(".")[0]}.{local_ip.split(".")[1]}.{local_ip.split(".")[2]}.1/24')
    print(f'\n[+] Local IP: {local_ip}\n[+] Local Gateway: {gateway}')
    print_ip_mac(ip_mac_network)


if __name__ == "__main__":
    main()
