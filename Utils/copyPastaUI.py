#!/usr/bin/env python3
"""
CopyPasta UI Helper Functions
负责：添加/编辑/删除片段的对话框
"""

import tkinter as tk
from tkinter import messagebox


class CopyPastaUI:
    """
    CopyPasta 的 UI 辅助类
    负责：添加/编辑/删除片段的对话框
    """
    
    def __init__(self, parent):
        """
        初始化 UI 辅助类
        
        Args:
            parent: GadgetToolkitGUI 的实例（主窗口）
        """
        self.parent = parent
        self.root = parent.root
        self.colors = parent.colors
        self.fonts = parent.fonts
    
    # ============ 添加片段对话框 ============
    
    def add_snippet_dialog(self):
        """弹出对话框添加新片段"""
        dialog = tk.Toplevel(self.root)
        dialog.title("添加新片段")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f"400x200+{x}+{y}")
        
        main_frame = tk.Frame(dialog, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text="名称:", font=self.fonts['default']).pack(anchor='w')
        name_entry = tk.Entry(main_frame, font=self.fonts['default'])
        name_entry.pack(fill=tk.X, pady=(0, 10))
        name_entry.focus()
        
        tk.Label(main_frame, text="内容:", font=self.fonts['default']).pack(anchor='w')
        content_entry = tk.Entry(main_frame, font=self.fonts['default'])
        content_entry.pack(fill=tk.X, pady=(0, 15))
        
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)
        
        def confirm():
            name = name_entry.get().strip()
            content = content_entry.get().strip()
            if name and content:
                self.parent.copyPasta.add_snippet(name, content)
                dialog.destroy()
                self.parent.show_copyPasta()
                messagebox.showinfo("成功", f"✅ 已添加片段: {name}")
            else:
                messagebox.showwarning("警告", "名称和内容都不能为空！")
        
        tk.Button(btn_frame, text="✅ 添加", command=confirm,
                  bg='#27ae60', fg='white', padx=20).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="❌ 取消", command=dialog.destroy,
                  bg='#95a5a6', fg='white', padx=20).pack(side=tk.LEFT, padx=5)
        
        content_entry.bind('<Return>', lambda e: confirm())
    
    # ============ 删除片段对话框（列表选择） ============
    
    def delete_snippet_dialog(self):
        """弹出对话框删除片段（从列表选择）"""
        snippets = self.parent.copyPasta.get_all_snippets()
        if not snippets:
            messagebox.showinfo("提示", "没有片段可以删除！")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("删除片段")
        dialog.geometry("300x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="选择要删除的片段:", font=self.fonts['default']).pack(pady=10)
        
        listbox = tk.Listbox(dialog, font=self.fonts['default'])
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        for snippet in snippets:
            listbox.insert(tk.END, f"{snippet['id']}: {snippet['name']}")
        
        def confirm_delete():
            selection = listbox.curselection()
            if selection:
                snippet = snippets[selection[0]]
                if messagebox.askyesno("确认", f"删除「{snippet['name']}」？"):
                    self.parent.copyPasta.delete_snippet(snippet['id'])
                    dialog.destroy()
                    self.parent.show_copyPasta()
                    messagebox.showinfo("成功", "✅ 已删除！")
        
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="🗑️ 删除", command=confirm_delete,
                  bg='#e74c3c', fg='white', padx=20).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="❌ 取消", command=dialog.destroy,
                  bg='#95a5a6', fg='white', padx=20).pack(side=tk.LEFT, padx=5)
    
    # ============ 删除片段（直接删除，带确认） ============
    
    def delete_snippet_by_id(self, snippet_id: str):
        """
        根据ID删除片段（带确认对话框）
        用于表格中的删除按钮
        
        Args:
            snippet_id: 片段ID
        """
        snippet = self.parent.copyPasta.get_snippet(snippet_id)
        if snippet:
            if messagebox.askyesno("确认删除", f"删除「{snippet['name']}」？"):
                self.parent.copyPasta.delete_snippet(snippet_id)
                self.parent.show_copyPasta()
                messagebox.showinfo("成功", "✅ 已删除！")
    
    # ============ 编辑片段对话框 ============
    
    def edit_snippet_dialog(self, snippet_id: str):
        """弹出对话框编辑片段"""
        snippet = self.parent.copyPasta.get_snippet(snippet_id)
        if not snippet:
            messagebox.showerror("错误", "片段不存在！")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("编辑片段")
        dialog.geometry("450x280")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (280 // 2)
        dialog.geometry(f"450x280+{x}+{y}")
        
        # 主框架
        main_frame = tk.Frame(dialog, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text=f"编辑片段 #{snippet_id}", 
                font=('Segoe UI', 14, 'bold')).pack(pady=(0, 15))
        
        # 名称输入（预填当前值）
        tk.Label(main_frame, text="名称:", font=self.fonts['default'], anchor='w').pack(fill=tk.X)
        name_entry = tk.Entry(main_frame, font=self.fonts['default'])
        name_entry.insert(0, snippet.get('name', ''))
        name_entry.pack(fill=tk.X, pady=(0, 10))
        name_entry.focus()
        name_entry.select_range(0, tk.END)
        
        # 内容输入（预填当前值）
        tk.Label(main_frame, text="内容:", font=self.fonts['default'], anchor='w').pack(fill=tk.X)
        content_entry = tk.Entry(main_frame, font=self.fonts['default'])
        content_entry.insert(0, snippet.get('content', ''))
        content_entry.pack(fill=tk.X, pady=(0, 15))
        
        # 按钮
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)
        
        def confirm_update():
            name = name_entry.get().strip()
            content = content_entry.get().strip()
            
            if not name or not content:
                messagebox.showwarning("警告", "名称和内容都不能为空！")
                return
            
            updated = self.parent.copyPasta.update_snippet(snippet_id, name, content)
            if updated:
                dialog.destroy()
                self.parent.show_copyPasta()
                messagebox.showinfo("成功", f"✅ 已更新片段: {name}")
        
        tk.Button(
            btn_frame,
            text="✅ 确认更新",
            command=confirm_update,
            bg='#27ae60',
            fg='white',
            font=self.fonts['default'],
            padx=20,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="❌ 取消",
            command=dialog.destroy,
            bg='#95a5a6',
            fg='white',
            font=self.fonts['default'],
            padx=20,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        # 绑定回车键
        content_entry.bind('<Return>', lambda e: confirm_update())