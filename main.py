#!/usr/bin/env python3
"""
Gadget Toolkit - Main GUI Application
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import sys
import os
import platform

# Import gadgets from Gadgets package
from Gadgets import WelcomeGadget, NetworkGadgets, CopyPastaGadget
from Utils import CopyPastaUI


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
        self.copyPasta = CopyPastaGadget()

        # Setup GUI
        self.setup_styles()
        self.cp_ui = CopyPastaUI(self)

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
        tools_menu.add_command(label="CopyPasta", command=self.show_copyPasta, accelerator="Ctrl+P")
        tools_menu.add_separator()
        tools_menu.add_command(label="添加片段", command=self.cp_ui.add_snippet_dialog, accelerator="Ctrl+A")
        tools_menu.add_command(label="删除片段", command=self.cp_ui.delete_snippet_dialog, accelerator="Ctrl+D")
        
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
            ("📋 CopyPasta", self.show_copyPasta),
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
        """Display Welcome screen"""
        self.notebook.select(self.welcome_tab)
        
        welcome_text = self.welcome.get_welcome_text()
        
        if not hasattr(self, 'welcome_text_widget'):
            self.welcome_text_widget = scrolledtext.ScrolledText(
                self.welcome_tab, 
                wrap=tk.WORD, 
                font=self.fonts['mono'],
                bg='white', 
                fg='#2c3e50'
            )
            self.welcome_text_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.welcome_text_widget.config(state=tk.NORMAL)
        self.welcome_text_widget.delete(1.0, tk.END)
        self.welcome_text_widget.insert(tk.END, welcome_text)
        self.welcome_text_widget.config(state=tk.DISABLED)
    
    def show_network(self):
        """Display Network information"""
        self.clear_output()
        self.notebook.select(self.output_tab)
        
        info = self.network.get_ip_info()
        
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, "🌐 NETWORK INFORMATION\n", 'header')
        self.output_text.insert(tk.END, "=" * 60 + "\n\n")
        
        if info.get('error'):
            self.output_text.insert(tk.END, f"❌ Error: {info['error']}\n", 'error')
        else:
            self.output_text.insert(tk.END, "🖥️  HOSTNAME\n", 'header')
            self.output_text.insert(tk.END, f"   {info['hostname']}\n\n", 'info')
            
            self.output_text.insert(tk.END, "📡 LOCAL IP\n", 'header')
            self.output_text.insert(tk.END, f"   {info['local_ip']}\n\n", 'info')
            
            self.output_text.insert(tk.END, "🌍 PUBLIC IP\n", 'header')
            if info['public_ip'] and info['public_ip'] != 'Could not retrieve':
                self.output_text.insert(tk.END, f"   {info['public_ip']}\n\n", 'success')
            else:
                self.output_text.insert(tk.END, "   ⚠️ Could not retrieve public IP\n\n", 'warning')
            
            if info.get('interfaces'):
                self.output_text.insert(tk.END, "📋 NETWORK INTERFACES\n", 'header')
                self.output_text.insert(tk.END, "-" * 40 + "\n")
                for iface in info['interfaces']:
                    self.output_text.insert(tk.END, f"   {iface}\n")
        
        self.output_text.insert(tk.END, "\n" + "=" * 60 + "\n")
        self.output_text.insert(tk.END, "✅ Network information loaded successfully\n", 'success')
        self.output_text.config(state=tk.DISABLED)

    def show_copyPasta(self):
        """显示 CopyPasta 列表（表格样式，每行带操作按钮）"""
        self.clear_output()
        self.notebook.select(self.output_tab)
        
        snippets = self.copyPasta.get_all_snippets()
        
        # 清空 output_text
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        
        # 显示标题（在文本区域）
        self.output_text.insert(tk.END, "📋 COPYPASTA - 快速复制片段\n", 'header')
        self.output_text.insert(tk.END, "=" * 60 + "\n")
        self.output_text.insert(tk.END, "💡 点击行任意位置复制 | 点击按钮操作\n\n", 'info')
        
        # 创建主容器 - 使用 PanedWindow 或 Frame 来完全控制大小
        # 先插入一个占位，然后替换为 Frame
        self.output_text.insert(tk.END, "\n")
        text_end = self.output_text.index(tk.END)
        
        # 创建主容器 Frame (使用高一点的行高)
        container = tk.Frame(self.output_text, bg='white', height=400)
        self.output_text.window_create(text_end, window=container, stretch=True)
        
        # 使用 Canvas 支持滚动
        canvas = tk.Canvas(container, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 内部 Frame - 用来放置所有行
        list_frame = tk.Frame(canvas, bg='white')
        canvas.create_window((0, 0), window=list_frame, anchor='nw', width=canvas.winfo_width())
        
        # 表头 - 增加高度
        header_frame = tk.Frame(list_frame, bg='#2c3e50', height=35)
        header_frame.pack(fill=tk.X, pady=(0, 3))
        header_frame.pack_propagate(False)
        
        # 表头列 - 调整宽度比例
        tk.Label(header_frame, text="#", bg='#2c3e50', fg='white', 
                 font=('Segoe UI', 11, 'bold'), width=5, anchor='center').pack(side=tk.LEFT, padx=3)
        tk.Label(header_frame, text="名称", bg='#2c3e50', fg='white',
                 font=('Segoe UI', 11, 'bold'), width=15, anchor='w').pack(side=tk.LEFT, padx=5)
        # 内容预览列 - 使用 expand 填满剩余空间
        tk.Label(header_frame, text="内容预览", bg='#2c3e50', fg='white',
                 font=('Segoe UI', 11, 'bold'), anchor='w').pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        tk.Label(header_frame, text="操作", bg='#2c3e50', fg='white',
                 font=('Segoe UI', 11, 'bold'), width=18, anchor='center').pack(side=tk.LEFT, padx=5)
        
        # 存储 snippets 供后续刷新使用
        list_frame.snippets = snippets
        
        # 如果没有片段
        if not snippets:
            empty_label = tk.Label(list_frame, text="📭 还没有任何片段，请添加", 
                                bg='white', fg='#7f8c8d', font=('Segoe UI', 12), pady=40)
            empty_label.pack(fill=tk.X)
        else:
            # 填充数据行 - 行高增加
            for idx, snippet in enumerate(snippets, 1):
                row_frame = tk.Frame(list_frame, bg='white', height=45)
                row_frame.pack(fill=tk.X, pady=2)
                row_frame.pack_propagate(False)
                
                # 鼠标悬停效果
                def on_enter(e, f=row_frame):
                    f.config(bg='#ecf0f1')
                    for child in f.winfo_children():
                        if isinstance(child, (tk.Label, tk.Frame)):
                            child.config(bg='#ecf0f1')
                            for subchild in child.winfo_children():
                                if isinstance(subchild, tk.Label):
                                    subchild.config(bg='#ecf0f1')
                                elif isinstance(subchild, tk.Frame):
                                    subchild.config(bg='#ecf0f1')
                                    for subsub in subchild.winfo_children():
                                        if isinstance(subsub, tk.Label):
                                            subsub.config(bg='#ecf0f1')
                def on_leave(e, f=row_frame):
                    f.config(bg='white')
                    for child in f.winfo_children():
                        if isinstance(child, (tk.Label, tk.Frame)):
                            child.config(bg='white')
                            for subchild in child.winfo_children():
                                if isinstance(subchild, tk.Label):
                                    subchild.config(bg='white')
                                elif isinstance(subchild, tk.Frame):
                                    subchild.config(bg='white')
                                    for subsub in subchild.winfo_children():
                                        if isinstance(subsub, tk.Label):
                                            subsub.config(bg='white')
                
                row_frame.bind('<Enter>', on_enter)
                row_frame.bind('<Leave>', on_leave)
                
                # 整行点击复制
                content = snippet.get('content', '')
                def row_click(e, c=content):
                    self.copy_to_clipboard(c)
                row_frame.bind('<Button-1>', row_click)
                
                # 序号
                idx_label = tk.Label(row_frame, text=f"{idx:2d}", bg='white', fg='#7f8c8d',
                                    font=('Segoe UI', 10), width=5, anchor='center')
                idx_label.pack(side=tk.LEFT, padx=3)
                idx_label.bind('<Button-1>', row_click)
                
                # 名称
                name = snippet.get('name', '未命名')
                name_label = tk.Label(row_frame, text=name, bg='white', fg='#2c3e50',
                                     font=('Segoe UI', 10), width=15, anchor='w')
                name_label.pack(side=tk.LEFT, padx=5)
                name_label.bind('<Button-1>', row_click)
                
                # 内容预览
                preview = content[:50] + "..." if len(content) > 50 else content
                preview_label = tk.Label(row_frame, text=preview, bg='white', fg='#34495e',
                                        font=('Segoe UI', 10), anchor='w')
                preview_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
                preview_label.bind('<Button-1>', row_click)
                
                # 操作按钮容器
                btn_frame = tk.Frame(row_frame, bg='white')
                btn_frame.pack(side=tk.LEFT, padx=5)
                # 阻止事件传播到 row_frame，但不阻止按钮点击
                
                # 复制按钮 - 使用更大的按钮
                copy_btn = tk.Button(
                    btn_frame,
                    text="📋 复制",
                    font=('Segoe UI', 9, 'bold'),
                    bg='#3498db',
                    fg='white',
                    padx=10,
                    pady=2,
                    cursor='hand2',
                    relief='raised',
                    bd=2,
                    command=lambda c=content: self.copy_to_clipboard(c)
                )
                copy_btn.pack(side=tk.LEFT, padx=3)
                # 阻止按钮点击事件冒泡
                copy_btn.bind('<Button-1>', lambda e: "break", add=True)
                
                # 编辑按钮
                edit_btn = tk.Button(
                    btn_frame,
                    text="✏️ 编辑",
                    font=('Segoe UI', 9, 'bold'),
                    bg='#f39c12',
                    fg='white',
                    padx=10,
                    pady=2,
                    cursor='hand2',
                    relief='raised',
                    bd=2,
                    command=lambda sid=snippet['id']: self.cp_ui.edit_snippet_dialog(sid)
                )
                edit_btn.pack(side=tk.LEFT, padx=3)
                edit_btn.bind('<Button-1>', lambda e: "break", add=True)
                
                # 删除按钮
                delete_btn = tk.Button(
                    btn_frame,
                    text="🗑️ 删除",
                    font=('Segoe UI', 9, 'bold'),
                    bg='#e74c3c',
                    fg='white',
                    padx=10,
                    pady=2,
                    cursor='hand2',
                    relief='raised',
                    bd=2,
                    command=lambda sid=snippet['id']: self.cp_ui.delete_snippet_by_id(sid)
                )
                delete_btn.pack(side=tk.LEFT, padx=3)
                delete_btn.bind('<Button-1>', lambda e: "break", add=True)
        
        # 更新 Canvas 滚动区域
        def update_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox('all'))
        list_frame.bind('<Configure>', update_scroll_region)
        
        # 配置 Canvas 宽度 - 让内容填满
        def configure_canvas_width(event):
            canvas_width = event.width
            canvas.itemconfig(1, width=canvas_width)
        canvas.bind('<Configure>', configure_canvas_width)
        
        # 在列表下方显示统计信息
        self.output_text.insert(tk.END, "\n" + "=" * 60 + "\n")
        self.output_text.insert(tk.END, f"✅ 共 {len(snippets)} 个片段\n", 'success')
        self.output_text.insert(tk.END, "💡 点击行任意位置复制 | 点击按钮操作\n", 'info')
        
        # 阻止键盘编辑
        def block_edit(event):
            return "break"
        self.output_text.bind('<Key>', block_edit)
    
    # ============ UTILITY METHODS ============
    
    def copy_to_clipboard(self, content: str):
        """复制到剪贴板并显示提示"""
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        self.root.update()
        
        preview = content[:100] + "..." if len(content) > 100 else content
        messagebox.showinfo("✅ 复制成功", f"已复制到剪贴板！\n\n{preview}")
    
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