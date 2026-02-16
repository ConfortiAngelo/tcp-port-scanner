import ipaddress


def generate_ip_range(ips : str):
    ips_list = []
    net = ipaddress.ip_network(ips , strict= False)
    for ip_generate in net.hosts():
        ips_list.append(ip_generate)
    return ips_list