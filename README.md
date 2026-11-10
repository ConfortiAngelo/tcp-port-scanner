# tcp-port-scanner

[![tests](https://github.com/ConfortiAngelo/tcp-port-scanner/actions/workflows/tests.yml/badge.svg)](https://github.com/ConfortiAngelo/tcp-port-scanner/actions/workflows/tests.yml)

An asynchronous TCP connect scanner in Python, written from scratch to understand what tools like Nmap do under the hood and what a scan looks like from the defender's side.

> **Authorized use only.** Scan only hosts you own or have written permission to test. Examples and tests here target `127.0.0.1` only.

## Demo

```text
$ python -m app.main -t 127.0.0.1 -p 8080 [8081,8083]
╭─────────────────────────╮
│ PORT SCAN INIT V1.0     │
│ Target(s) : 127.0.0.1   │
│ Scan Type : TCP Connect │
╰─────────────────────────╯
┏━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┓
┃ PORTS    ┃ STATE  ┃ SERVICE    ┃
┡━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━┩
│ 8080/tcp │ OPEN   │ http-proxy │
│ 8081/tcp │ CLOSED │ http-alt   │
│ 8082/tcp │ CLOSED │            │
│ 8083/tcp │ CLOSED │            │
└──────────┴────────┴────────────┘
[✔] Open ports : 1
[-] Closed ports : 3
[!] Filtered ports : 0
```

(`8080` was a local `python -m http.server` started for the demo.)

## Features

- Targets: single IPs, several IPs, or CIDR ranges (`192.0.2.0/29`), validated with `ipaddress`.
- Ports: list and ranges (`-p 22 80 [8000,8100]`), or a default list of 814 common ports.
- **Async I/O** with `asyncio` + a semaphore (100 concurrent connections), one `TaskGroup` per host.
- States: `OPEN` (handshake completed), `CLOSED` (RST / refused), `FILTERED` (timeout).
- Service detection: banner regexes first (SSH, FTP, SMTP, HTTP, Redis, VNC…), then the well-known port table.
- Structured logging to `app/logs/logs.log` (per-connection debug lines).

## Architecture

```
app/main.py            CLI (argparse), input errors → exit code 2
core/
  ports.py             parse and validate ports / ranges
  scanner.py           entry point: runs the async executor
  services.py          banner regexes + port → service table
  models.py            PortScanResult / HostScanResult dataclasses, PortStatus enum
infrastructure/
  async_executor.py    semaphore + TaskGroup per host
  socket_client.py     one TCP connect: open → read banner → classify
utils/                 validators, output (rich), logger, exceptions
```

The core layer knows nothing about sockets; `infrastructure/` is the only layer that touches the network. That split is what makes the parsing and classification testable without a network.

## How to run

```bash
pip install -r requirements-dev.txt
python -m pytest                                   # 15 passed (integration tests use 127.0.0.1 only)
python -m app.main -t 127.0.0.1 -p 22 80 [8000,8100]
```

Requires **Python 3.12+** (uses PEP 701 f-strings).

## Blue-team view: what this scan leaves behind

A TCP connect scan completes the full three-way handshake, so it is the **noisiest** scan type:

- The target's application logs record each connection (e.g. sshd: `Connection closed by <ip> port <p> [preauth]`).
- Host firewalls log a burst of SYNs from one source to many destination ports, which is exactly what the `port_scan` rule in my [log-threat-detection](https://github.com/ConfortiAngelo/log-threat-detection) project detects (T1046).

## Design decisions and limitations

- **TCP connect instead of SYN scan:** needs no root and no raw sockets, at the cost of being louder and slower.
- **Filtered = timeout (2 s):** a slow host can be misclassified as filtered.
- **Banner grabbing waits for the server to speak first**, so services that wait for the client (HTTP) take the full timeout and fall back to the port table.
- IPv4 and IPv6 literals are accepted, but hostnames are not resolved. No UDP. CLI messages are still in Spanish.

## Changelog (repository cleanup)

- Removed a committed `venv/` (2,825 files) and `__pycache__/` from the whole history (repo went from 15 MB to 224 KB).
- Removed a committed runtime log that contained scan attempts against non-lab addresses. New examples use `127.0.0.1` and documentation ranges only.
- Fixed: `UnboundLocalError` when the event loop failed; logger crashed if `app/logs/` did not exist; invalid ports raised a traceback instead of an error message; test file imported a function that did not exist; duplicate port in the default list; unused `scapy` dependency.

## With more time

- SYN scan with raw sockets (and a comparison of the logs each scan type leaves).
- Send protocol probes (e.g. `HEAD / HTTP/1.0`) to identify services that do not speak first.
- JSON output for SIEM ingestion; hostname resolution; per-host rate limiting.

## License

[MIT](LICENSE)
