#!/usr/bin/env python3
"""
Gadget Toolkit - Main GUI Application
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import sys
import os
import platform

# Import both gadgets from Gadgets package
from Gadgets import WelcomeGadget, NetworkGadgets


class GadgetToolkitGUI:
    """Main GUI Application Class"""
    
    def __init__(self, root):
        """Initialize the application"""
        self.root = root
        self.root.title("Gadget Toolkit")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Initialize gadgets (business logic)
        self.welcome = WelcomeGadget()
        self.network = NetworkGadgets()
        
        # Setup GUI
        self.setup_styles()
        self.create_menu()
        self.create_sidebar()
        self.create_main_area()

        

        # Handle close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_styles(self):
        """Configure colors and fonts"""
        self.colors = {
            'bg': '#f0f0f0',
            'sidebar': '#2c3e50',
            'sidebar_fg': 'white',
            'sidebar_hover': '#34495e',
            'success': '#27ae60',
            'error': '#e74c3c',
            'warning': '#f39c12',
            'info': '#3498db'
        }
        self.root.configure(bg=self.colors['bg'])
        
        if platform.system() == 'Windows':
            self.fonts = {
                'default': ('Segoe UI', 10),
                'title': ('Segoe UI', 16, 'bold'),
                'mono': ('Consolas', 10)
            }
        else:
            self.fonts = {
                'default': ('Helvetica', 10),
                'title': ('Helvetica', 16, 'bold'),
                'mono': ('Monospace', 10)
            }
    
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Output", command=self.save_output, accelerator="Ctrl+S")
        file_menu.add_command(label="Clear Output", command=self.clear_output, accelerator="Ctrl+C")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing, accelerator="Ctrl+Q")
        
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Network Tools", command=self.show_network, accelerator="Ctrl+N")

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_sidebar(self):
        """Create sidebar"""
        self.sidebar = tk.Frame(self.root, bg=self.colors['sidebar'], width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        tk.Label(self.sidebar, text="🔧 Gadget\nToolkit",
                bg=self.colors['sidebar'], fg=self.colors['sidebar_fg'],
                font=self.fonts['title'], justify=tk.CENTER).pack(pady=20)
        
        ttk.Separator(self.sidebar, orient='horizontal').pack(fill=tk.X, padx=10, pady=10)
        
        buttons = [
            ("🏠 Welcome", self.show_welcome),
            ("🌐 Network", self.show_network),
        ]
        
        for text, command in buttons:
            btn = tk.Button(self.sidebar, text=text,
                          bg=self.colors['sidebar'], fg=self.colors['sidebar_fg'],
                          font=self.fonts['default'], bd=0, anchor='w',
                          padx=20, pady=10, relief='flat', command=command)
            btn.pack(fill=tk.X)
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg=self.colors['sidebar_hover']))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg=self.colors['sidebar']))
        
        tk.Label(self.sidebar, text=f"v1.0 | {platform.system()}",
                bg=self.colors['sidebar'], fg='#7f8c8d',
                font=('Segoe UI', 9)).pack(side=tk.BOTTOM, pady=10)
    
    def create_main_area(self):
        """Create main content"""
        self.main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.welcome_tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(self.welcome_tab, text="🏠 Welcome")
        
        self.output_tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(self.output_tab, text="📝 Output")
        
        self.output_text = scrolledtext.ScrolledText(
            self.output_tab, wrap=tk.WORD, font=self.fonts['mono'],
            bg='white', fg='#2c3e50'
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.output_text.tag_configure('success', foreground=self.colors['success'])
        self.output_text.tag_configure('error', foreground=self.colors['error'])
        self.output_text.tag_configure('warning', foreground=self.colors['warning'])
        self.output_text.tag_configure('info', foreground=self.colors['info'])
        self.output_text.tag_configure('header', foreground='#2c3e50',
                                      font=(self.fonts['mono'][0], 12, 'bold'))
        self.output_text.config(state=tk.DISABLED)
    


    # ============ DISPLAY METHODS ============
    def show_welcome(self):
        """
        DISPLAY: Welcome screen
        ✅ Gets DATA from Gadgets/welcome.py
        ✅ DISPLAYS it with UI formatting
        """
        # FIX: Don't clear output - just show the welcome tab
        self.notebook.select(self.welcome_tab)
        
        
        # Get welcome text from business logic
        welcome_text = self.welcome.get_welcome_text()
        
        # Create a text widget in the welcome tab if it doesn't exist
        if not hasattr(self, 'welcome_text_widget'):
            self.welcome_text_widget = scrolledtext.ScrolledText(
                self.welcome_tab, 
                wrap=tk.WORD, 
                font=self.fonts['mono'],
                bg='white', 
                fg='#2c3e50'
            )
            self.welcome_text_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Display welcome text
        self.welcome_text_widget.config(state=tk.NORMAL)
        self.welcome_text_widget.delete(1.0, tk.END)
        self.welcome_text_widget.insert(tk.END, welcome_text)
        self.welcome_text_widget.config(state=tk.DISABLED)
    
    def show_network(self):
        """
        DISPLAY: Network information
        ✅ Gets DATA from Gadgets/network.py
        ✅ DISPLAYS it with UI formatting
        """
        self.clear_output()
        self.notebook.select(self.output_tab)
        
        
        # Get data from business logic
        info = self.network.get_ip_info()
        
        # Display the results
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, "🌐 NETWORK INFORMATION\n", 'header')
        self.output_text.insert(tk.END, "=" * 60 + "\n\n")
        
        if info.get('error'):
            self.output_text.insert(tk.END, f"❌ Error: {info['error']}\n", 'error')
        else:
            # Display hostname
            self.output_text.insert(tk.END, "🖥️  HOSTNAME\n", 'header')
            self.output_text.insert(tk.END, f"   {info['hostname']}\n\n", 'info')
            
            # Display local IP
            self.output_text.insert(tk.END, "📡 LOCAL IP\n", 'header')
            self.output_text.insert(tk.END, f"   {info['local_ip']}\n\n", 'info')
            
            # Display public IP
            self.output_text.insert(tk.END, "🌍 PUBLIC IP\n", 'header')
            if info['public_ip'] and info['public_ip'] != 'Could not retrieve':
                self.output_text.insert(tk.END, f"   {info['public_ip']}\n\n", 'success')
            else:
                self.output_text.insert(tk.END, "   ⚠️ Could not retrieve public IP\n\n", 'warning')
            
            # Display network interfaces (if available)
            if info.get('interfaces'):
                self.output_text.insert(tk.END, "📋 NETWORK INTERFACES\n", 'header')
                self.output_text.insert(tk.END, "-" * 40 + "\n")
                for iface in info['interfaces']:
                    self.output_text.insert(tk.END, f"   {iface}\n")
        
        self.output_text.insert(tk.END, "\n" + "=" * 60 + "\n")
        self.output_text.insert(tk.END, "✅ Network information loaded successfully\n", 'success')
        
        self.output_text.config(state=tk.DISABLED)
        
    
 
    # ============ UTILITY METHODS ============
    
    def clear_output(self):
        """Clear output"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
        
    
    def save_output(self):
        """Save output"""
        content = self.output_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("No Content", "Nothing to save!")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                messagebox.showinfo("Success", f"Saved: {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed: {e}")
    
    def update_status(self, message):
        """Update status"""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def show_about(self):
        """Show about"""
        messagebox.showinfo("About", """
🔧 Gadget Toolkit v1.0

A collection of Python utility tools
with a modern GUI interface.

Created with Python and Tkinter.
        """)
    
    def on_closing(self):
        """Handle close"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            sys.exit(0)


def main():
    """Main entry point"""
    try:
        root = tk.Tk()
        app = GadgetToolkitGUI(root)
        root.mainloop()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()