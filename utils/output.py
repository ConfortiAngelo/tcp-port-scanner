from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from core.services import get_service
console = Console()



def render_header(target) -> None:
    console.print(Panel(f'[magenta]PORT SCAN INIT V1.0[/magenta]\n'
    f'Target(s) : {target.ip}\n'
    f'Scan Type : TCP Connect',
    expand=False))
        
def render_scan_info(hosts) -> None:
    console.print(f'[+] Resolving targets...\n'
        f'[✔] {hosts} hosts identified')
    console.print(f'[~] Starting scan')


def render_status(hostscanresult) -> None:
    # mostrar si el host esta prendido (si es posible la conexion) o apagado (no es posible la conexion)
    pass
def render_ports_table(target) -> None:
    table = Table()
    table.add_column('PORTS')
    table.add_column('STATE')
    table.add_column('SERVICE')

    for result in target.port_result:
        service, detected = get_service(result.port, result.banner)

        state_color = {
            "OPEN": "green",
            "CLOSED": "red",
            "FILTERED": "yellow"
        }.get(result.status.name, "white")

        table.add_row(
            f"{result.port}/tcp",
            f"[{state_color}]{result.status.name}[/{state_color}]",
            f"{service}{' (banner)' if detected else ''}"
        )

    console.print(table)

def host_summary(target) -> None:
    console.print(f'[✔] Open ports : {target.summary()['open']}')
    console.print(f'[-] Closed ports : {target.summary()['closed']}')
    console.print(f'[!] Filtered ports : {target.summary()['filtered']}')

def final_host_summary(target,hosts) -> None:
    console.print('[bold underline yellow]Final Summary[/bold underline yellow]')
    console.print(f'Hosts scanned : {hosts}\n'
    f'Total open ports : {target.summary()['open']}\n'
    f'Scan duration : {target.total_duration_ms}\n'
    f'[✔] Scan completed successfully')

def render_host_result(hostscanresult) -> None:
    
    
    for target in (hostscanresult):
        console.rule()
        hosts = len(hostscanresult)
        render_header(target)
        render_scan_info(hosts)
        render_ports_table(target)
        host_summary(target)
        final_host_summary(target,hosts)
