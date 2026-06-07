#!/usr/bin/env python3
# ============================================================
#   ██╗  ██╗ █████╗ ██╗    ██╗██╗  ██╗███╗   ███╗ █████╗ ██████╗ ██████╗ ███████╗██████╗
#   ██║  ██║██╔══██╗██║    ██║██║ ██╔╝████╗ ████║██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
#   ███████║███████║██║ █╗ ██║█████╔╝ ██╔████╔██║███████║██████╔╝██████╔╝█████╗  ██████╔╝
#   ██╔══██║██╔══██║██║███╗██║██╔═██╗ ██║╚██╔╝██║██╔══██║██╔═══╝ ██╔═══╝ ██╔══╝  ██╔══██╗
#   ██║  ██║██║  ██║╚███╔███╔╝██║  ██╗██║ ╚═╝ ██║██║  ██║██║     ██║     ███████╗██║  ██║
#   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═╝
#
#   Advanced Network Reconnaissance Suite
#   Made by   : Harshit Negi
#   GitHub    : github.com/harshithnegi
#   Tool Name : Hawkmapper v1.0
#   Purpose   : Penetration Testing / CTF / Network Recon
#   Platform  : Kali Linux / Any Linux with nmap
# ============================================================

import os
import sys
import subprocess
import datetime
import shutil
import xml.etree.ElementTree as ET

# ── ANSI Colors ──────────────────────────────────────────────
R  = "\033[0m"          # reset
G  = "\033[92m"         # green
C  = "\033[96m"         # cyan
Y  = "\033[93m"         # yellow
RE = "\033[91m"         # red
B  = "\033[94m"         # blue
W  = "\033[97m"         # white
DM = "\033[2m"          # dim
BO = "\033[1m"          # bold

# ── Banner ────────────────────────────────────────────────────
def banner():
    os.system("clear")
    print(G + BO + """
  ██╗  ██╗ █████╗ ██╗    ██╗██╗  ██╗███╗   ███╗ █████╗ ██████╗ ██████╗ ███████╗██████╗
  ██║  ██║██╔══██╗██║    ██║██║ ██╔╝████╗ ████║██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
  ███████║███████║██║ █╗ ██║█████╔╝ ██╔████╔██║███████║██████╔╝██████╔╝█████╗  ██████╔╝
  ██╔══██║██╔══██║██║███╗██║██╔═██╗ ██║╚██╔╝██║██╔══██║██╔═══╝ ██╔═══╝ ██╔══╝  ██╔══██╗
  ██║  ██║██║  ██║╚███╔███╔╝██║  ██╗██║ ╚═╝ ██║██║  ██║██║     ██║     ███████╗██║  ██║
  ╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═╝
""" + R)
    print(C + "  " + "─"*80 + R)
    print(W + "    Advanced Network Reconnaissance Suite" + DM + "  |  Made by: " + G + BO + "Harshit Negi" + R)
    print(C + "  " + "─"*80 + R)
    print()

# ── Nmap check ───────────────────────────────────────────────
def check_nmap():
    if shutil.which("nmap") is None:
        print(RE + "\n  [!] nmap not found. Install it: sudo apt install nmap\n" + R)
        sys.exit(1)

# ── Main Menu ─────────────────────────────────────────────────
def main_menu():
    print(Y + BO + "  [ SELECT SCAN MODULE ]\n" + R)
    options = [
        ("01", "Host Discovery",             "Ping sweeps, ICMP, ARP, UDP probes"),
        ("02", "Port & Service Discovery",   "TCP, SYN, XMAS, ACK, SCTP scans"),
        ("03", "OS Detection",               "OS fingerprinting & SMB discovery"),
        ("04", "IDS / Firewall Evasion",     "Fragmentation, decoys, spoof port"),
        ("05", "Report Generation",          "Save scan output as XML file"),
        ("06", "Exit",                       ""),
    ]
    for num, label, desc in options:
        if num == "06":
            print(RE + f"  [{num}] " + W + f"{label}" + R)
        else:
            print(G + f"  [{num}] " + W + BO + f"{label:<30}" + R + DM + f"  {desc}" + R)
    print()

# ── Sub-menu helper ───────────────────────────────────────────
def sub_menu(title, scans):
    banner()
    print(Y + BO + f"  [ {title.upper()} ]\n" + R)
    for i, (name, desc, _) in enumerate(scans, 1):
        print(G + f"  [{i:02d}] " + W + BO + f"{name:<35}" + R + DM + f"  {desc}" + R)
    print(RE + f"\n  [00] " + W + "Back to Main Menu" + R)
    print()

# ── Get target ────────────────────────────────────────────────
def get_target(prompt="  [»] Enter Target IP / Range / Hostname : "):
    target = input(C + prompt + G).strip()
    print(R, end="")
    if not target:
        print(RE + "\n  [!] No target entered. Going back.\n" + R)
        return None
    return target

# ── Run nmap ─────────────────────────────────────────────────
def run_nmap(cmd):
    print()
    print(C + "  " + "─"*60 + R)
    print(G + f"  [»] Running : " + Y + cmd + R)
    print(C + "  " + "─"*60 + R)
    print(DM + "  [i] Press Ctrl+C to abort scan\n" + R)
    try:
        subprocess.run(cmd, shell=True)
    except KeyboardInterrupt:
        print(RE + "\n\n  [!] Scan aborted by user.\n" + R)
    print()
    input(G + "  [»] Press Enter to return to menu..." + R)

# ── Module 1 — Host Discovery ─────────────────────────────────
def host_discovery():
    scans = [
        ("UDP Ping Sweep",          "Sends UDP to discover hosts when ICMP is blocked",      "nmap -sn -PU {t}"),
        ("ICMP Echo Ping Sweep",    "Classic ping sweep via ICMP echo requests",              "nmap -sn -PE {t}"),
        ("ICMP Echo Range Sweep",   "ICMP echo across a host range (e.g. 10.10.1.1-25)",     "nmap -sn -PE {t}"),
        ("ICMP Timestamp Ping",     "Timestamp requests; bypasses firewalls blocking echo",  "nmap -sn -PP {t}"),
        ("ICMP Netmask Ping",       "Sends ICMP address mask requests to find live hosts",   "nmap -sn -PM {t}"),
        ("TCP SYN Ping",            "SYN to port 80; host responds if alive (no handshake)", "nmap -sn -PS {t}"),
        ("TCP ACK Ping",            "ACK packets; evades stateless firewall rules",           "nmap -sn -PA {t}"),
        ("IP Protocol Ping",        "Raw IP packets with multiple protocols to find hosts",   "nmap -sn -PO {t}"),
    ]
    while True:
        banner()
        sub_menu("Host Discovery", scans)
        choice = input(C + "  [»] Select scan : " + G).strip()
        print(R, end="")
        if choice == "0" or choice == "00":
            break
        if not choice.isdigit() or not (1 <= int(choice) <= len(scans)):
            print(RE + "\n  [!] Invalid choice.\n" + R)
            input(G + "  [»] Press Enter..." + R)
            continue
        idx = int(choice) - 1
        name, desc, cmd_t = scans[idx]
        print(G + f"\n  [+] Selected : " + W + BO + name + R)
        print(DM + f"  [i] {desc}\n" + R)
        target = get_target()
        if target:
            cmd = cmd_t.replace("{t}", target)
            run_nmap(cmd)

# ── Module 2 — Port & Service Discovery ──────────────────────
def port_discovery():
    scans = [
        ("TCP Connect Scan",         "Full TCP handshake; no root needed, easily logged",     "nmap -sT -v {t}"),
        ("SYN Stealth Scan",         "Half-open SYN; faster, stealthier (needs root)",        "nmap -sS -v {t}"),
        ("XMAS Scan",                "Sets FIN+PSH+URG; bypasses some stateless firewalls",   "nmap -sX -v {t}"),
        ("Maimon Scan",              "FIN/ACK probe; many BSD systems reveal filtered ports",  "nmap -sM -v {t}"),
        ("ACK Scan",                 "Maps firewall rulesets; finds filtered vs unfiltered",   "nmap -sA -v {t}"),
        ("SCTP INIT Scan",           "SCTP equivalent of SYN scan; maps SCTP services",       "nmap -sY -v {t}"),
        ("Idle / Zombie Scan",       "Stealthy via zombie host; your IP never hits target",   "nmap -sI -v {t}"),
        ("SCTP COOKIE-ECHO Scan",    "Advanced SCTP; open ports silently drop chunks",        "nmap -sZ -v {t}"),
        ("Aggressive Full Scan",     "OS + version + scripts + traceroute in one sweep",      "nmap -A {t}"),
    ]
    while True:
        banner()
        sub_menu("Port & Service Discovery", scans)
        choice = input(C + "  [»] Select scan : " + G).strip()
        print(R, end="")
        if choice == "0" or choice == "00":
            break
        if not choice.isdigit() or not (1 <= int(choice) <= len(scans)):
            print(RE + "\n  [!] Invalid choice.\n" + R)
            input(G + "  [»] Press Enter..." + R)
            continue
        idx = int(choice) - 1
        name, desc, cmd_t = scans[idx]
        print(G + f"\n  [+] Selected : " + W + BO + name + R)
        print(DM + f"  [i] {desc}\n" + R)
        target = get_target()
        if target:
            cmd = cmd_t.replace("{t}", target)
            run_nmap(cmd)

# ── Module 3 — OS Detection ───────────────────────────────────
def os_detection():
    scans = [
        ("Aggressive OS + Service Detect", "Full aggressive scan: OS, version, scripts, traceroute", "nmap -A {t}"),
        ("OS Fingerprinting",              "TCP/IP stack fingerprinting to identify the OS",          "nmap -O {t}"),
        ("SMB OS Discovery Script",        "NSE SMB script — pulls OS info via Windows file-sharing", "nmap --script=smb-os-discovery {t}"),
    ]
    while True:
        banner()
        sub_menu("OS Detection", scans)
        choice = input(C + "  [»] Select scan : " + G).strip()
        print(R, end="")
        if choice == "0" or choice == "00":
            break
        if not choice.isdigit() or not (1 <= int(choice) <= len(scans)):
            print(RE + "\n  [!] Invalid choice.\n" + R)
            input(G + "  [»] Press Enter..." + R)
            continue
        idx = int(choice) - 1
        name, desc, cmd_t = scans[idx]
        print(G + f"\n  [+] Selected : " + W + BO + name + R)
        print(DM + f"  [i] {desc}\n" + R)
        target = get_target()
        if target:
            cmd = cmd_t.replace("{t}", target)
            run_nmap(cmd)

# ── Module 4 — IDS / Firewall Evasion ────────────────────────
def ids_evasion():
    scans = [
        ("Packet Fragmentation",       "Splits TCP header; bypasses older IDS/IPS signatures",     "nmap -f {t}"),
        ("Source Port Spoof (80)",     "Source port = 80; firewalls often trust port 80 traffic",   "nmap -g 80 {t}"),
        ("Source Port Option (80)",    "Alternate --source-port flag; same effect as -g 80",        "nmap --source-port 80 {t}"),
        ("Custom MTU (8 bytes)",       "Forces 8-byte MTU fragmentation; evades DPI firewalls",     "nmap --mtu 8 {t}"),
        ("Decoy Scan (10 random IPs)", "Generates 10 ghost IPs to mask your real source address",   "nmap -D RND:10 {t}"),
    ]
    while True:
        banner()
        sub_menu("IDS / Firewall Evasion", scans)
        choice = input(C + "  [»] Select scan : " + G).strip()
        print(R, end="")
        if choice == "0" or choice == "00":
            break
        if not choice.isdigit() or not (1 <= int(choice) <= len(scans)):
            print(RE + "\n  [!] Invalid choice.\n" + R)
            input(G + "  [»] Press Enter..." + R)
            continue
        idx = int(choice) - 1
        name, desc, cmd_t = scans[idx]
        print(G + f"\n  [+] Selected : " + W + BO + name + R)
        print(DM + f"  [i] {desc}\n" + R)
        target = get_target()
        if target:
            cmd = cmd_t.replace("{t}", target)
            run_nmap(cmd)

# ── HTML Report Builder ───────────────────────────────────────
def parse_xml_to_html(xml_file, html_file, target, scan_time, analyst='Unknown'):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except Exception as e:
        return False, str(e)

    hosts_html = ""
    host_count = 0
    open_port_total = 0

    for host in root.findall("host"):
        # Status
        status_el = host.find("status")
        state = status_el.get("state", "unknown") if status_el is not None else "unknown"
        state_color = "#00ff88" if state == "up" else "#ff4455"

        # IP + hostname
        addr_el = host.find("address[@addrtype='ipv4']")
        ip = addr_el.get("addr", "N/A") if addr_el is not None else "N/A"
        hn_el = host.find("hostnames/hostname")
        hostname = hn_el.get("name", "") if hn_el is not None else ""

        # OS
        os_match = host.find("os/osmatch")
        os_name = os_match.get("name", "Unknown") if os_match is not None else "Unknown"
        os_acc  = os_match.get("accuracy", "") if os_match is not None else ""

        # Ports
        ports_rows = ""
        port_count = 0
        for port in host.findall("ports/port"):
            pid      = port.get("portid", "")
            proto    = port.get("protocol", "")
            st_el    = port.find("state")
            pstate   = st_el.get("state", "") if st_el is not None else ""
            svc_el   = port.find("service")
            svc_name = svc_el.get("name", "") if svc_el is not None else ""
            svc_prod = svc_el.get("product", "") if svc_el is not None else ""
            svc_ver  = svc_el.get("version", "") if svc_el is not None else ""
            svc_info = f"{svc_prod} {svc_ver}".strip()

            if pstate == "open":
                port_count += 1
                open_port_total += 1
                row_color = "rgba(0,255,136,0.07)"
                state_badge = f'<span style="color:#00ff88;font-weight:600">● open</span>'
            elif pstate == "filtered":
                row_color = "rgba(255,215,0,0.05)"
                state_badge = f'<span style="color:#ffd700">◐ filtered</span>'
            else:
                row_color = "transparent"
                state_badge = f'<span style="color:#4a6070">{pstate}</span>'

            ports_rows += f"""
            <tr style="background:{row_color};border-bottom:1px solid #1a2a3a">
              <td style="padding:8px 12px;color:#00d4ff;font-weight:600">{pid}</td>
              <td style="padding:8px 12px;color:#4a6070;text-transform:uppercase;font-size:11px">{proto}</td>
              <td style="padding:8px 12px">{state_badge}</td>
              <td style="padding:8px 12px;color:#c8d8e8">{svc_name}</td>
              <td style="padding:8px 12px;color:#888;font-size:12px">{svc_info}</td>
            </tr>"""

        # Scripts / NSE output
        script_rows = ""
        for script in host.findall("ports/port/script"):
            sid    = script.get("id", "")
            sout   = script.get("output", "").replace("<", "&lt;").replace(">", "&gt;")
            script_rows += f"""
            <div style="margin:6px 0;padding:10px 14px;background:#070b10;border-left:3px solid #00d4ff;border-radius:0 4px 4px 0">
              <span style="color:#00d4ff;font-size:11px;letter-spacing:1px">{sid}</span>
              <pre style="margin:6px 0 0;color:#c8d8e8;font-size:12px;white-space:pre-wrap;word-break:break-word">{sout}</pre>
            </div>"""

        host_count += 1
        hostname_line = f'<span style="color:#4a6070;font-size:13px"> / {hostname}</span>' if hostname else ""

        hosts_html += f"""
        <div style="background:#0f1520;border:1px solid #1a2a3a;border-radius:6px;margin-bottom:24px;overflow:hidden">
          <div style="background:#070b10;padding:14px 20px;border-bottom:1px solid #1a2a3a;display:flex;align-items:center;justify-content:space-between">
            <div>
              <span style="font-family:'Orbitron',monospace;font-size:16px;color:#00ff88;font-weight:700">{ip}</span>
              {hostname_line}
            </div>
            <span style="font-size:12px;padding:4px 12px;border:1px solid {state_color};color:{state_color};border-radius:3px;letter-spacing:2px">{state.upper()}</span>
          </div>
          <div style="padding:16px 20px;display:grid;grid-template-columns:1fr 1fr;gap:12px">
            <div style="background:#070b10;border-radius:4px;padding:12px 16px">
              <div style="font-size:10px;color:#4a6070;letter-spacing:2px;margin-bottom:4px">OPERATING SYSTEM</div>
              <div style="color:#c8d8e8;font-size:13px">{os_name} {'<span style="color:#4a6070;font-size:11px">('+os_acc+'% accuracy)</span>' if os_acc else ''}</div>
            </div>
            <div style="background:#070b10;border-radius:4px;padding:12px 16px">
              <div style="font-size:10px;color:#4a6070;letter-spacing:2px;margin-bottom:4px">OPEN PORTS FOUND</div>
              <div style="color:#00ff88;font-size:20px;font-weight:700;font-family:'Orbitron',monospace">{port_count}</div>
            </div>
          </div>
          {'<div style="padding:0 20px 4px"><div style="font-size:10px;color:#4a6070;letter-spacing:2px;margin-bottom:8px">PORT DETAILS</div><div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;font-family:monospace;font-size:13px"><thead><tr style="background:#070b10;border-bottom:1px solid #1a2a3a"><th style="padding:8px 12px;text-align:left;color:#4a6070;font-size:10px;letter-spacing:2px">PORT</th><th style="padding:8px 12px;text-align:left;color:#4a6070;font-size:10px;letter-spacing:2px">PROTO</th><th style="padding:8px 12px;text-align:left;color:#4a6070;font-size:10px;letter-spacing:2px">STATE</th><th style="padding:8px 12px;text-align:left;color:#4a6070;font-size:10px;letter-spacing:2px">SERVICE</th><th style="padding:8px 12px;text-align:left;color:#4a6070;font-size:10px;letter-spacing:2px">VERSION</th></tr></thead><tbody>' + ports_rows + '</tbody></table></div></div>' if ports_rows else '<div style="padding:0 20px 16px;color:#4a6070;font-size:13px">No ports detected.</div>'}
          {('<div style="padding:8px 20px 16px"><div style="font-size:10px;color:#4a6070;letter-spacing:2px;margin-bottom:8px">NSE SCRIPT OUTPUT</div>' + script_rows + '</div>') if script_rows else ''}
        </div>"""

    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Hawkmapper Report — {target}</title>
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{background:#0a0e14;color:#c8d8e8;font-family:'Share Tech Mono',monospace;min-height:100vh;padding:0 0 40px}}
  a{{color:#00d4ff;text-decoration:none}}
  pre{{font-family:'Share Tech Mono',monospace}}
  ::-webkit-scrollbar{{width:6px;height:6px}}
  ::-webkit-scrollbar-track{{background:#0a0e14}}
  ::-webkit-scrollbar-thumb{{background:#1a2a3a;border-radius:3px}}
</style>
</head>
<body>
<!-- HEADER -->
<div style="background:linear-gradient(135deg,#0a0e14,#0f1a2e,#0a0e14);border-bottom:1px solid #00ff88;padding:24px 40px;display:flex;align-items:center;justify-content:space-between">
  <div style="display:flex;align-items:center;gap:18px">
    <div style="font-size:40px;filter:drop-shadow(0 0 10px #00ff88)">🦅</div>
    <div>
      <div style="font-family:'Orbitron',monospace;font-size:26px;font-weight:900;color:#00ff88;letter-spacing:4px;text-shadow:0 0 16px rgba(0,255,136,0.4)">HAWKMAPPER</div>
      <div style="font-size:11px;color:#4a6070;letter-spacing:3px;margin-top:3px">NETWORK RECONNAISSANCE REPORT</div>
    </div>
  </div>
  <div style="text-align:right">
    <div style="font-size:11px;color:#4a6070;letter-spacing:1px">Generated by</div>
    <div style="font-size:15px;color:#00d4ff;font-weight:600;letter-spacing:1px">{analyst}</div>
    <div style="font-size:10px;color:#4a6070;margin-top:4px">{now_str}</div>
  </div>
</div>

<!-- SUMMARY CARDS -->
<div style="max-width:1100px;margin:30px auto;padding:0 24px">
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:28px">
    <div style="background:#0f1520;border:1px solid #1a2a3a;border-radius:6px;padding:16px 20px">
      <div style="font-size:10px;color:#4a6070;letter-spacing:2px;margin-bottom:6px">TARGET</div>
      <div style="font-size:14px;color:#00ff88;word-break:break-all">{target}</div>
    </div>
    <div style="background:#0f1520;border:1px solid #1a2a3a;border-radius:6px;padding:16px 20px">
      <div style="font-size:10px;color:#4a6070;letter-spacing:2px;margin-bottom:6px">SCAN TIME</div>
      <div style="font-size:13px;color:#c8d8e8">{scan_time}</div>
    </div>
    <div style="background:#0f1520;border:1px solid #00ff88;border-radius:6px;padding:16px 20px">
      <div style="font-size:10px;color:#4a6070;letter-spacing:2px;margin-bottom:6px">HOSTS FOUND</div>
      <div style="font-size:28px;color:#00ff88;font-family:'Orbitron',monospace;font-weight:700">{host_count}</div>
    </div>
    <div style="background:#0f1520;border:1px solid #00d4ff;border-radius:6px;padding:16px 20px">
      <div style="font-size:10px;color:#4a6070;letter-spacing:2px;margin-bottom:6px">OPEN PORTS</div>
      <div style="font-size:28px;color:#00d4ff;font-family:'Orbitron',monospace;font-weight:700">{open_port_total}</div>
    </div>
  </div>

  <!-- SCAN TYPE BADGE -->
  <div style="background:#0f1520;border:1px solid #1a2a3a;border-radius:6px;padding:12px 20px;margin-bottom:28px;display:flex;align-items:center;gap:12px">
    <span style="font-size:10px;color:#4a6070;letter-spacing:2px">SCAN TYPE</span>
    <span style="color:#ffd700;font-size:13px">nmap -Pn -sS -A (SYN Stealth + Aggressive Detection)</span>
    <span style="margin-left:auto;font-size:10px;padding:3px 10px;border:1px solid #00ff88;color:#00ff88;border-radius:2px;letter-spacing:2px">HAWKMAPPER v1.0</span>
  </div>

  <!-- HOST RESULTS -->
  <div style="font-size:10px;color:#4a6070;letter-spacing:3px;margin-bottom:16px;padding-bottom:10px;border-bottom:1px solid #1a2a3a">HOST RESULTS</div>
  {hosts_html if hosts_html else '<div style="color:#4a6070;padding:20px;text-align:center">No hosts found in scan results.</div>'}

  <!-- FOOTER -->
  <div style="margin-top:40px;padding:16px 20px;border:1px solid #1a2a3a;border-radius:6px;display:flex;align-items:center;justify-content:space-between;font-size:11px;color:#4a6070">
    <span>🦅 Hawkmapper v1.0 &nbsp;·&nbsp; Made by <span style="color:#00d4ff">Harshit Negi</span></span>
    <span style="color:#ff4455">For authorized penetration testing only. Use responsibly.</span>
  </div>
</div>
</body>
</html>"""

    with open(html_file, "w") as f:
        f.write(html)
    return True, ""


# ── Module 5 — Report Generation ─────────────────────────────
def report_generation():
    banner()
    print(Y + BO + "  [ REPORT GENERATION ]\n" + R)
    print(G + "  [01] " + W + BO + "Full Scan → HTML Report" + R)
    print(DM + "       No-ping SYN scan + aggressive detect; saves a browser-readable HTML report\n" + R)
    print(RE + "  [00] " + W + "Back to Main Menu\n" + R)

    choice = input(C + "  [»] Select : " + G).strip()
    print(R, end="")
    if choice == "0" or choice == "00" or choice != "1":
        return

    target = get_target()
    if not target:
        return

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    default_file = f"hawkmapper_report_{ts}"
    print(C + f"  [»] Output filename (no extension) [default: {default_file}] : " + G, end="")
    filename = input().strip() or default_file
    print(R, end="")

    print(C + "  [»] Analyst Name (report mein dikhega) : " + G, end="")
    analyst = input().strip() or "Unknown"
    print(R, end="")

    xml_tmp  = f"{filename}.xml"
    html_out = f"{filename}.html"

    # Run nmap, save XML temporarily
    cmd = f"nmap -Pn -sS -A -oX {xml_tmp} {target}"
    print()
    print(C + "  " + "─"*60 + R)
    print(G + f"  [»] Running : " + Y + cmd + R)
    print(C + "  " + "─"*60 + R)
    print(DM + "  [i] Press Ctrl+C to abort\n" + R)

    scan_start = datetime.datetime.now()
    try:
        subprocess.run(cmd, shell=True)
    except KeyboardInterrupt:
        print(RE + "\n\n  [!] Scan aborted.\n" + R)
        input(G + "  [»] Press Enter..." + R)
        return
    scan_end   = datetime.datetime.now()
    scan_time  = str(scan_end - scan_start).split(".")[0]

    # Parse XML → HTML
    print(G + "\n  [+] Building HTML report..." + R)
    ok, err = parse_xml_to_html(xml_tmp, html_out, target, scan_time, analyst)
    if ok:
        print(G + BO + f"  [✔] Report saved : " + Y + f"{html_out}" + R)
        print(DM + f"  [i] Open in browser: firefox {html_out}" + R)
    else:
        print(RE + f"  [!] HTML generation failed: {err}" + R)
        print(Y + f"  [i] Raw XML still available at: {xml_tmp}" + R)
    print()
    input(G + "  [»] Press Enter to return..." + R)

# ── Exit ──────────────────────────────────────────────────────
def exit_tool():
    banner()
    print(G + BO + "  [+] Hawkmapper closed. Stay ethical, stay legal." + R)
    print(DM + "  [i] Made by Harshit Negi  |  For authorized testing only\n" + R)
    sys.exit(0)

# ── Main Loop ─────────────────────────────────────────────────
def main():
    check_nmap()
    module_map = {
        "1": host_discovery,
        "2": port_discovery,
        "3": os_detection,
        "4": ids_evasion,
        "5": report_generation,
        "6": exit_tool,
        "01": host_discovery,
        "02": port_discovery,
        "03": os_detection,
        "04": ids_evasion,
        "05": report_generation,
        "06": exit_tool,
    }
    while True:
        banner()
        main_menu()
        choice = input(C + "  [»] Enter module number : " + G).strip()
        print(R, end="")
        if choice in module_map:
            module_map[choice]()
        else:
            print(RE + "\n  [!] Invalid option. Choose 01–06.\n" + R)
            input(G + "  [»] Press Enter..." + R)

if __name__ == "__main__":
    main()
