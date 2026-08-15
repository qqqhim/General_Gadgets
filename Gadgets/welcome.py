#!/usr/bin/env python3
"""
Welcome Gadget - Business Logic
Provides welcome message and app information
"""

import platform
import sys
from typing import Dict, Any


class WelcomeGadget:
    """Welcome gadget - returns welcome data"""
    
    def get_welcome_data(self) -> Dict[str, Any]:
        """
        Get welcome information
        Returns: Dict with app info, system info, available gadgets
        """
        return {
            'app_name': 'Gadget Toolkit',
            'app_version': '1.0.0',
            'app_description': 'A collection of useful Python utility tools',
            'system': {
                'os': platform.system(),
                'release': platform.release(),
                'python': sys.version.split()[0],
                'architecture': platform.architecture()[0]
            },
            'available_gadgets': [
                {
                    'name': 'Network',
                    'icon': '🌐',
                    'description': 'Display IP addresses, hostname, network interfaces'
                }
            ],
            'coming_soon': [
                {'name': 'Text Tools', 'icon': '📝', 'description': 'Word count, text analysis, password generator'},
                {'name': 'System Info', 'icon': '💻', 'description': 'CPU, memory, disk usage monitoring'},
                {'name': 'File Operations', 'icon': '📁', 'description': 'File management and organization'},
            ],
            'shortcuts': [
                {'key': 'Ctrl+N', 'action': 'Open Network Gadget'},
                {'key': 'Ctrl+S', 'action': 'Save output to file'},
                {'key': 'Ctrl+C', 'action': 'Clear output'},
                {'key': 'Ctrl+Q', 'action': 'Exit application'},
            ],
            'tip': 'All gadgets are modular - more tools will be added!'
        }
    
    def get_welcome_text(self) -> str:
        """
        Get formatted welcome text
        Returns: Formatted welcome message as string
        """
        data = self.get_welcome_data()
        
        # Build welcome text
        text = f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              🔧  WELCOME TO {data['app_name'].upper()}                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

📋 ABOUT THIS APPLICATION
───────────────────────────────────────────────────────────────
{data['app_description']}

💻 SYSTEM INFORMATION
───────────────────────────────────────────────────────────────
• Operating System: {data['system']['os']} {data['system']['release']}
• Python Version: {data['system']['python']}
• Architecture: {data['system']['architecture']}

🎯 AVAILABLE GADGETS
───────────────────────────────────────────────────────────────
"""
        
        # Add available gadgets
        for gadget in data['available_gadgets']:
            text += f"{gadget['icon']} {gadget['name']}\n"
            text += f"   • {gadget['description']}\n"
        
        # Add coming soon
        if data['coming_soon']:
            text += """
🚀 COMING SOON
───────────────────────────────────────────────────────────────
"""
            for gadget in data['coming_soon']:
                text += f"{gadget['icon']} {gadget['name']}\n"
                text += f"   • {gadget['description']}\n"
        
        # Add shortcuts
        text += """
💡 HOW TO USE
───────────────────────────────────────────────────────────────
1. Click a gadget button on the LEFT SIDEBAR
2. Results will appear in this OUTPUT tab
3. Use File menu to Save (Ctrl+S) or Clear (Ctrl+C) output

⌨️  KEYBOARD SHORTCUTS
───────────────────────────────────────────────────────────────
"""
        for shortcut in data['shortcuts']:
            text += f"• {shortcut['key']}  - {shortcut['action']}\n"
        
        text += f"""
📌 TIP: {data['tip']}

╔══════════════════════════════════════════════════════════════╗
║              Ready to get started? 🚀                       ║
║         Click "Network" on the sidebar to begin!           ║
╚══════════════════════════════════════════════════════════════╝
"""
        return text