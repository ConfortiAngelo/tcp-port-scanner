import re
def _detected_from_banner(banner):
    for pattern , service in BANNER_PATTERNS:
        if pattern.search(banner):
            return service
    return None

def get_service(port : str, banner : str | None) -> tuple[str:bool]:
    if banner:
        detected = _detected_from_banner(banner)
        if detected:
            return detected,True

    if port in COMMON_PORTS:
        return COMMON_PORTS[port],False
    return 'unknown', False

#PORTS
COMMON_PORTS = {
    #Infraestructura básica
    20: "ftp-data",
    21: "ftp",
    22: "ssh",
    23: "telnet",
    25: "smtp",
    53: "dns",
    67: "dhcp",
    68: "dhcp",
    69: "tftp",
    70: "gopher",
    79: "finger",
    111: "rpcbind",

    #Web
    80: "http",
    81: "http-alt",
    82: "http-alt",
    83: "http-alt",
    88: "kerberos",
    443: "https",
    444: "https-alt",
    591: "http-alt",
    8000: "http-alt",
    8008: "http-alt",
    8080: "http-proxy",
    8081: "http-alt",
    8088: "http-alt",
    8443: "https-alt",
    8888: "http-alt",

    #Correo
    109: "pop2",
    110: "pop3",
    143: "imap",
    465: "smtps",
    587: "smtp-submission",
    993: "imaps",
    995: "pop3s",

    #Directorio / autenticación
    135: "rpc",
    137: "netbios-ns",
    138: "netbios-dgm",
    139: "netbios-ssn",
    389: "ldap",
    445: "smb",
    464: "kerberos-change",
    593: "rpc-over-http",
    636: "ldaps",
    3268: "ldap-global",
    3269: "ldaps-global",

    #Bases de datos
    1433: "mssql",
    1434: "mssql-monitor",
    1521: "oracle",
    2049: "nfs",
    2082: "cpanel",
    2083: "cpanel-ssl",
    2181: "zookeeper",
    2375: "docker",
    2376: "docker-ssl",
    2483: "oracle-ssl",
    2484: "oracle-ssl",
    27017: "mongodb",
    27018: "mongodb",
    27019: "mongodb",
    28017: "mongodb-web",
    3306: "mysql",
    5432: "postgresql",
    6379: "redis",
    6380: "redis-ssl",
    7001: "weblogic",
    9042: "cassandra",
    9200: "elasticsearch",

    #Acceso remoto
    3389: "rdp",
    5900: "vnc",
    5901: "vnc",
    5902: "vnc",

    #Dev / control de versiones
    3690: "svn",
    9418: "git",

    #Proxy / tunneling
    1080: "socks",
    3128: "proxy",

    #Monitoreo / logs
    161: "snmp",
    162: "snmptrap",
    514: "syslog",
    9100: "printer",

    #VPN / comunicaciones
    989: "ftps-data",
    990: "ftps",
    1194: "openvpn",
    1701: "l2tp",
    1723: "pptp",
    1812: "radius",
    1813: "radius-accounting",

    #Otros
    515: "printer-lpd",
    548: "afp",
    873: "rsync",
    1900: "upnp",
    5060: "sip",
    5061: "sips",
    5222: "xmpp",
    5269: "xmpp-server",
    6667: "irc",

    #Juegos
    25565: "minecraft",
    19132: "minecraft-bedrock"
}

                                                                                                                                                                 
BANNER_PATTERNS: list[tuple[re.Pattern, str]] = [
    # 🔸 Infraestructura básica
    (re.compile(r"^SSH-\d+\.\d+-",                  re.IGNORECASE), "ssh"),
    (re.compile(r"^220[-\s].*FTP|FileZilla|ProFTPD|vsftpd|Pure-FTPd", re.IGNORECASE), "ftp"),
    (re.compile(r"^220[-\s].*ftps",                 re.IGNORECASE), "ftps"),
    (re.compile(r"^220[-\s]",                        re.IGNORECASE), "smtp"),   # fallback 220
    (re.compile(r"^220[-\s].*(ESMTP|Postfix|Exim|Sendmail|Exchange)", re.IGNORECASE), "smtp"),
    (re.compile(r"^\xff\xfb|^\xff\xfd",             re.IGNORECASE), "telnet"),  # IAC WILL / IAC DO
    (re.compile(r"^@RSYNCD",                         re.IGNORECASE), "rsync"),

    #Web
    (re.compile(r"^HTTP/\d\.\d\s+\d{3}",            re.IGNORECASE), "http"),
    (re.compile(r"^HTTP/\d\.\d\s+\d{3}.*https",     re.IGNORECASE), "https"),

    #Correo
    (re.compile(r"^\+OK",                            re.IGNORECASE), "pop3"),
    (re.compile(r"^\* OK.*IMAP",                     re.IGNORECASE), "imap"),

    #Bases de datos
    (re.compile(r"^\d+\.\d+\.\d+.*MySQL|MariaDB",   re.IGNORECASE), "mysql"),
    (re.compile(r"^.*PostgreSQL",                    re.IGNORECASE), "postgresql"),
    (re.compile(r"^\-ERR|\+PONG|\+OK",              re.IGNORECASE), "redis"),
    (re.compile(r"^.*MongoDB",                       re.IGNORECASE), "mongodb"),
    (re.compile(r"^\{.*\"version\".*\"elastic\"",    re.IGNORECASE), "elasticsearch"),
    (re.compile(r"^.*Zookeeper",                     re.IGNORECASE), "zookeeper"),

    #Acceso remoto
    (re.compile(r"^RFB \d+\.\d+",                   re.IGNORECASE), "vnc"),

    #Proxy / tunneling
    (re.compile(r"^HTTP/\d\.\d\s+407",              re.IGNORECASE), "proxy"),

    #Dev / control de versiones
    (re.compile(r"^\( success",                      re.IGNORECASE), "svn"),
    (re.compile(r"^git",                             re.IGNORECASE), "git"),

    #Comunicaciones
    (re.compile(r"^SIP/\d\.\d",                     re.IGNORECASE), "sip"),
    (re.compile(r"^<\?xml.*jabber|xmpp",            re.IGNORECASE), "xmpp"),
    (re.compile(r"^:\S+\s+NOTICE|^\S+\s+001\s",    re.IGNORECASE), "irc"),

    #Infraestructura Docker
    (re.compile(r"^HTTP.*Docker",                    re.IGNORECASE), "docker"),
]