# 命令模块初始化文件
# 从Pyrogram框架改为aiogram框架

from .emby_libs import extraembylibs_blockall, extraembylibs_unblockall, embylibs_blockall, embylibs_unblockall
from .pro_rev import pro_admin, pro_user, rev_user, del_admin
from .renew import renew_user
from .renewall import renew_all
from .rmemby import rmemby_user
from .score_coins import score_user, coins_user
from .start import router as start_router  # 导入start模块的路由器
from .syncs import sync_emby_group, sync_emby_unbound, bindall_id, reload_admins
from .view_user import list_whitelist, whitelist_page, list_normaluser, normaluser_page

# 导入所有路由器
routers = [
    start_router,  # start命令路由器
    # 其他模块的路由器将在后续更新中添加
]

# 导出所有路由器列表，供主程序注册使用
__all__ = ['routers']