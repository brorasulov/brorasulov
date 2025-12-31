#!/usr/bin/env python3
"""
Get your local IP address for sharing the website
"""
import socket

def get_local_ip():
    try:
        # Connect to a remote server to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return None

def get_all_ips():
    """Get all local IP addresses"""
    import subprocess
    try:
        result = subprocess.run(['ifconfig'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        ips = []
        for line in lines:
            if 'inet ' in line and '127.0.0.1' not in line:
                ip = line.split('inet ')[1].split(' ')[0]
                if ip.startswith('192.168.') or ip.startswith('10.') or ip.startswith('172.'):
                    ips.append(ip)
        return ips
    except:
        return []

print("🌐 Finding your local IP address...\n")

# Try primary method
ip = get_local_ip()
if ip:
    print(f"✅ Primary IP: {ip}")
    print(f"\n🔗 Others can access at: http://{ip}:8000")
else:
    print("⚠️  Could not detect IP automatically")

# Get all IPs
all_ips = get_all_ips()
if all_ips:
    print(f"\n📋 All local IPs found:")
    for i, ip_addr in enumerate(all_ips, 1):
        print(f"   {i}. http://{ip_addr}:8000")

print("\n📝 Instructions:")
print("1. Make sure you're on the same WiFi network")
print("2. Start server with: python3 -m http.server 8000 --bind 0.0.0.0")
print("3. Share the IP address above with others")
print("4. They can open it in their browser")

