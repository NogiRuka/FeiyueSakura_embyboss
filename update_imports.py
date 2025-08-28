#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量更新导入语句脚本
将所有 fix_bottons 的导入改为 aiogram_buttons
"""

import os
import re

def update_file(file_path):
    """更新单个文件的导入语句"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换导入语句
        old_import = 'from bot.func_helper.fix_bottons import'
        new_import = 'from bot.func_helper.aiogram_buttons import'
        
        if old_import in content:
            content = content.replace(old_import, new_import)
            print(f"✅ 已更新: {file_path}")
            
            # 写回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        else:
            print(f"⏭️ 无需更新: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ 更新失败 {file_path}: {e}")
        return False

def main():
    """主函数"""
    print("🔄 开始批量更新导入语句...")
    
    # 需要更新的文件列表
    files_to_update = [
        "bot/modules/panel/admin_panel.py",
        "bot/modules/panel/server_panel.py",
        "bot/modules/panel/sched_panel.py",
        "bot/modules/panel/member_panel.py",
        "bot/modules/panel/kk.py",
        "bot/modules/panel/config_panel.py",
        "bot/modules/commands/exchange.py",
        "bot/modules/commands/score_coins.py",
        "bot/modules/commands/view_user.py",
        "bot/modules/callback/leave_unauth_group.py",
        "bot/scheduler/userplays_rank.py",
        "bot/modules/extra/create.py",
        "bot/modules/extra/red_envelope.py"
    ]
    
    updated_count = 0
    for file_path in files_to_update:
        if os.path.exists(file_path):
            if update_file(file_path):
                updated_count += 1
        else:
            print(f"⚠️ 文件不存在: {file_path}")
    
    print(f"\n🎉 批量更新完成！")
    print(f"📊 总计更新文件: {updated_count}/{len(files_to_update)}")

if __name__ == "__main__":
    main()
