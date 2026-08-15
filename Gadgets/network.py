#!/usr/bin/env python3
"""
Network Gadget - Real implementation
"""

import socket
import platform
import subprocess
import urllib.request
from typing import Dict, Any


class NetworkGadgets:
    """Network utility functions"""
    
    def get_ip_info(self) -> Dict[str, Any]:
        """Get real IP information"""
        result = {
            'hostname': '',
            'local_ip': '',
            'public_ip': '',
            'interfaces': [],
            'error': None
        }
        
        try:
            # Get hostname and local IP
            hostname = socket.gethostname()
            result['hostname'] = hostname
            result['local_ip'] = socket.gethostbyname(hostname)
            
            # Get public IP
            try:
                public_ip = urllib.request.urlopen(
                    'https://api.ipify.org', timeout=5
                ).read().decode('utf8')
                result['public_ip'] = public_ip
            except:
                result['public_ip'] = 'Could not retrieve'
            
            # Get network interfaces (Windows)
            if platform.system() == 'Windows':
                try:
                    output = subprocess.run(['ipconfig'], capture_output=True, text=True)
                    lines = output.stdout.split('\n')
                    interfaces = []
                    for line in lines:
                        if 'IPv4' in line or 'IPv6' in line or 'Description' in line:
                            interfaces.append(line.strip())
                    result['interfaces'] = interfaces
                except:
                    pass
                    
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def ping_host(self, host: str, count: int = 4) -> Dict[str, Any]:
        """Ping a host"""
        result = {
            'success': False,
            'output': '',
            'error': None
        }
        
        try:
            param = '-n' if platform.system() == 'Windows' else '-c'
            output = subprocess.run(
                ['ping', param, str(count), host],
                capture_output=True, text=True,
                timeout=10
            )
            result['output'] = output.stdout
            result['success'] = True
        except Exception as e:
            result['error'] = str(e)
        
        return result