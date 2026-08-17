#!/usr/bin/env python3
"""
CopyPasta Gadget - Manage and quickly copy text snippets
"""

import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime


class CopyPastaGadget:
    """
    Manage text snippets for quick copying and pasting.
    Each snippet has: id, name, content, created_at, updated_at
    """
    
    def __init__(self, storage_file: Optional[str] = None):
        """Initialize CopyPasta gadget with persistent storage"""
        
        # 数据结构: 使用字典存储，每个条目有唯一ID
        # {
        #     "snippet_id": {
        #         "id": "snippet_id",
        #         "name": "问候语",
        #         "content": "你好！很高兴认识你",
        #         "created_at": "2026-01-15 10:30:00",
        #         "updated_at": "2026-01-15 10:30:00"
        #     }
        # }
        
        self.snippets: Dict[str, Dict[str, Any]] = {}
        self.next_id = 1  # 用于生成唯一ID
        
        # 设置存储文件
        if storage_file is None:
            home_dir = os.path.expanduser("~")
            storage_dir = os.path.join(home_dir, ".gadget_toolkit")
            os.makedirs(storage_dir, exist_ok=True)
            self.storage_file = os.path.join(storage_dir, "copypasta_snippets.json")
        else:
            self.storage_file = storage_file
        
        # 加载已保存的数据
        self.load_snippets()
    
    # ============ 核心数据操作方法 ============
    
    def load_snippets(self) -> None:
        """从存储文件加载数据"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        self.snippets = data
                        # 更新 next_id
                        if self.snippets:
                            ids = [int(k) for k in self.snippets.keys() if k.isdigit()]
                            self.next_id = max(ids) + 1 if ids else 1
                        return
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading snippets: {e}")
        
        # 如果没有数据，添加一些示例
        self.add_default_snippets()
    
    def save_snippets(self) -> bool:
        """保存数据到存储文件"""
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(self.snippets, f, ensure_ascii=False, indent=2)
            return True
        except IOError as e:
            print(f"Error saving snippets: {e}")
            return False
    
    def add_default_snippets(self) -> None:
        """添加默认示例数据"""
        defaults = [
            ("问候语", "你好！很高兴认识你。今天过得怎么样？"),
            ("感谢", "非常感谢你的帮助！这对我的工作很有帮助。🙏"),
            ("确认", "好的，我明白了。我会按照你的要求去执行。"),
            ("等待", "请稍等片刻，我正在处理这个问题... ⏳"),
            ("结束", "好的，这次就到这里。谢谢！我们下次再聊。"),
        ]
        for name, content in defaults:
            self.add_snippet(name, content)
        self.save_snippets()
    
    # ============ CRUD 操作 ============
    
    def add_snippet(self, name: str, content: str) -> Dict[str, Any]:
        """
        添加新的片段
        
        Args:
            name: 片段名称（用于显示）
            content: 片段内容
        
        Returns:
            创建的片段字典
        """
        snippet_id = str(self.next_id)
        self.next_id += 1
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        snippet = {
            "id": snippet_id,
            "name": name.strip(),
            "content": content.strip(),
            "created_at": now,
            "updated_at": now
        }
        
        self.snippets[snippet_id] = snippet
        self.save_snippets()
        return snippet
    
    def get_all_snippets(self) -> List[Dict[str, Any]]:
        """
        获取所有片段（按创建时间排序）
        
        Returns:
            片段列表，按ID排序
        """
        # 按ID排序（数字排序）
        sorted_items = sorted(
            self.snippets.items(),
            key=lambda x: int(x[0])
        )
        return [item[1] for item in sorted_items]
    
    def get_snippet(self, snippet_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取片段"""
        return self.snippets.get(snippet_id)
    
    def update_snippet(self, snippet_id: str, name: str, content: str) -> Optional[Dict[str, Any]]:
        """
        更新片段
        
        Returns:
            更新后的片段，如果不存在返回None
        """
        if snippet_id not in self.snippets:
            return None
        
        self.snippets[snippet_id]["name"] = name.strip()
        self.snippets[snippet_id]["content"] = content.strip()
        self.snippets[snippet_id]["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.save_snippets()
        return self.snippets[snippet_id]
    
    def delete_snippet(self, snippet_id: str) -> bool:
        """删除片段"""
        if snippet_id in self.snippets:
            del self.snippets[snippet_id]
            self.save_snippets()
            return True
        return False
    
    def delete_all_snippets(self) -> None:
        """删除所有片段"""
        self.snippets.clear()
        self.save_snippets()
    
    def get_snippet_count(self) -> int:
        """获取片段数量"""
        return len(self.snippets)
    
    def search_snippets(self, query: str) -> List[Dict[str, Any]]:
        """搜索片段（按名称或内容）"""
        if not query:
            return self.get_all_snippets()
        
        query = query.lower()
        results = []
        for snippet in self.snippets.values():
            if query in snippet["name"].lower() or query in snippet["content"].lower():
                results.append(snippet)
        return results
    
    # ============ 导入导出 ============
    
    def export_to_json(self, filepath: str) -> bool:
        """导出到JSON文件"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.snippets, f, ensure_ascii=False, indent=2)
            return True
        except IOError:
            return False
    
    def import_from_json(self, filepath: str, merge: bool = True) -> bool:
        """从JSON文件导入"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                imported = json.load(f)
            
            if not isinstance(imported, dict):
                return False
            
            if merge:
                # 合并导入，更新next_id
                self.snippets.update(imported)
                if imported:
                    ids = [int(k) for k in imported.keys() if k.isdigit()]
                    if ids:
                        self.next_id = max(self.next_id, max(ids) + 1)
            else:
                # 替换所有数据
                self.snippets = imported
                if imported:
                    ids = [int(k) for k in imported.keys() if k.isdigit()]
                    self.next_id = max(ids) + 1 if ids else 1
            
            self.save_snippets()
            return True
        except (json.JSONDecodeError, IOError):
            return False