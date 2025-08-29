#! /usr/bin/python3
# -*- coding:utf-8 -*-
"""
emby 的 API 封装
"""
from datetime import datetime, timedelta, timezone

import requests as r
from bot import emby_url, emby_api, emby_block, extra_emby_libs, LOGGER
from bot.sql_helper.sql_emby import sql_update_emby, Emby
from bot.sql_helper.sql_emby2 import sql_delete_emby2
from bot.common.utils import pwd_create, convert_runtime, cache


def create_policy(admin: bool = False, disable: bool = False, limit: int = 2, block: list | None = None):
    if block is None:
        block = ['播放列表'] + extra_emby_libs
    return {
        "IsAdministrator": admin,
        "IsHidden": True,
        "IsHiddenRemotely": True,
        "IsDisabled": disable,
        "EnableRemoteControlOfOtherUsers": False,
        "EnableSharedDeviceControl": False,
        "EnableRemoteAccess": True,
        "EnableLiveTvManagement": False,
        "EnableLiveTvAccess": True,
        "EnableMediaPlayback": True,
        "EnableAudioPlaybackTranscoding": False,
        "EnableVideoPlaybackTranscoding": False,
        "EnablePlaybackRemuxing": False,
        "EnableContentDeletion": False,
        "EnableContentDownloading": False,
        "EnableSubtitleDownloading": False,
        "EnableSubtitleManagement": False,
        "EnableSyncTranscoding": False,
        "EnableMediaConversion": False,
        "EnableAllDevices": True,
        "SimultaneousStreamLimit": limit,
        "BlockedMediaFolders": block,
        "AllowCameraUpload": False,
    }


def pwd_policy(embyid: str, stats: bool = False, new: str | None = None):
    if new is None:
        return {"Id": f"{embyid}", "ResetPassword": stats}
    return {"Id": f"{embyid}", "NewPw": f"{new}"}


class Embyservice:
    def __init__(self, url: str, api_key: str):
        self.url = url
        self.api_key = api_key
        self.headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'X-Emby-Token': self.api_key,
            'X-Emby-Client': 'Sakura BOT',
            'X-Emby-Device-Name': 'Sakura BOT',
            'X-Emby-Client-Version': '1.0.0',
            'User-Agent': 'Mozilla/5.0',
        }

    async def emby_create(self, name: str, us: int):
        ex = (datetime.now() + timedelta(days=us))
        res = r.post(f'{self.url}/emby/Users/New', headers=self.headers, json={"Name": name})
        if res.status_code == 200 or 204:
            try:
                user_id = res.json()["Id"]
                pwd = await pwd_create(8)
                r.post(f'{self.url}/emby/Users/{user_id}/Password', headers=self.headers, json=pwd_policy(user_id, new=pwd))
            except Exception:
                return False
            pr = r.post(f'{self.url}/emby/Users/{user_id}/Policy', headers=self.headers, json=create_policy(False, False))
            return (user_id, pwd, ex) if (pr.status_code == 200 or 204) else False
        return False

    async def emby_del(self, id: str, stats=None):
        res = r.delete(f'{self.url}/emby/Users/{id}', headers=self.headers)
        if res.status_code == 200 or 204:
            if stats is None:
                return bool(sql_update_emby(Emby.embyid == id, embyid=None, name=None, pwd=None, pwd2=None, lv='d', cr=None, ex=None))
            return bool(sql_delete_emby2(embyid=id))
        return False

    async def emby_reset(self, id: str, new: str | None = None):
        pr = r.post(f'{self.url}/emby/Users/{id}/Password', headers=self.headers, json=pwd_policy(embyid=id, stats=True))
        if pr.status_code == 200 or 204:
            if new is None:
                return bool(sql_update_emby(Emby.embyid == id, pwd=None))
            pr2 = r.post(f'{self.url}/emby/Users/{id}/Password', headers=self.headers, json=pwd_policy(id, new=new))
            if pr2.status_code == 200 or 204:
                return bool(sql_update_emby(Emby.embyid == id, pwd=new))
        return False

    async def emby_block(self, id: str, stats: int = 0, block=emby_block):
        policy = create_policy(False, False, block=block) if stats == 0 else create_policy(False, False)
        pr = r.post(f'{self.url}/emby/Users/{id}/Policy', headers=self.headers, json=policy)
        return True if (pr.status_code == 200 or 204) else False

    async def get_emby_libs(self) -> list | None:
        rp = r.get(f"{self.url}/emby/Library/VirtualFolders?api_key={self.api_key}", headers=self.headers)
        if rp.status_code == 200:
            return [lib['Name'] for lib in rp.json()]
        return None

    @cache.memoize(ttl=120)
    def get_current_playing_count(self) -> int:
        sessions = r.get(f"{self.url}/emby/Sessions", headers=self.headers).json()
        count = 0
        for s in sessions:
            try:
                if s.get("NowPlayingItem"):
                    count += 1
            except KeyError:
                pass
        return count

    async def emby_change_policy(self, id: str, admin: bool = False, method: bool = False):
        pr = r.post(self.url + f'/emby/Users/{id}/Policy', headers=self.headers, json=create_policy(admin=admin, disable=method))
        return True if (pr.status_code == 200 or 204) else False

    async def authority_account(self, tg: int, username: str, password: str | None = None):
        data = {"Username": username} if password == 'None' else {"Username": username, "Pw": password}
        res = r.post(self.url + '/emby/Users/AuthenticateByName', headers=self.headers, json=data)
        if res.status_code == 200:
            return True, res.json()["User"]["Id"]
        return False, 0

    async def emby_cust_commit(self, user_id: str | None = None, days: int = 7, method: str | None = None):
        _url = f'{self.url}/emby/user_usage_stats/submit_custom_query'
        sub_time = datetime.now(timezone(timedelta(hours=8)))
        start_time = (sub_time - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
        end_time = sub_time.strftime("%Y-%m-%d %H:%M:%S")
        sql = ''
        if method == 'sp':
            sql += "SELECT UserId, SUM(PlayDuration - PauseDuration) AS WatchTime FROM PlaybackActivity "
            sql += f"WHERE DateCreated >= '{start_time}' AND DateCreated < '{end_time}' GROUP BY UserId ORDER BY WatchTime DESC"
        elif user_id != 'None':
            sql += "SELECT MAX(DateCreated) AS LastLogin,SUM(PlayDuration - PauseDuration) / 60 AS WatchTime FROM PlaybackActivity "
            sql += f"WHERE UserId = '{user_id}' AND DateCreated >= '{start_time}' AND DateCreated < '{end_time}' GROUP BY UserId"
        resp = r.post(_url, headers=self.headers, json={"CustomQueryString": sql, "ReplaceUserId": True}, timeout=30)
        if resp.status_code == 200:
            return resp.json().get("results")
        return None

    async def users(self):
        try:
            resp = r.get(f"{self.url}/emby/Users", headers=self.headers)
            if resp.status_code != 204 and resp.status_code != 200:
                return False, {'error': "🤕Emby 服务器连接失败!"}
            return True, resp.json()
        except Exception as e:
            return False, {'error': e}

    def user(self, embyid: str):
        try:
            resp = r.get(f"{self.url}/emby/Users/{embyid}", headers=self.headers)
            if resp.status_code != 204 and resp.status_code != 200:
                return False, {'error': "🤕Emby 服务器连接失败!"}
            return True, resp.json()
        except Exception as e:
            return False, {'error': e}

    async def add_favotire_items(self, user_id: str, item_id: str):
        try:
            resp = r.post(f"{self.url}/emby/Users/{user_id}/FavoriteItems/{item_id}", headers=self.headers)
            return True if (resp.status_code == 204 or resp.status_code == 200) else False
        except Exception as e:
            LOGGER.error(f'添加收藏失败 {e}')
            return False

    async def item_id_namme(self, user_id: str, item_id: str):
        try:
            reqs = r.get(f"{self.url}/emby/Users/{user_id}/Items/{item_id}", headers=self.headers, timeout=3)
            if reqs.status_code != 204 and reqs.status_code != 200:
                return ''
            return reqs.json().get("Name", '')
        except Exception as e:
            LOGGER.error(f'获取title失败 {e}')
            return ''

    async def primary(self, item_id: str, width: int = 200, height: int = 300, quality: int = 90):
        try:
            resp = r.get(f"{self.url}/emby/Items/{item_id}/Images/Primary?maxHeight={height}&maxWidth={width}&quality={quality}", headers=self.headers)
            if resp.status_code != 204 and resp.status_code != 200:
                return False, {'error': "🤕Emby 服务器连接失败!"}
            return True, resp.content
        except Exception as e:
            return False, {'error': e}

    async def backdrop(self, item_id: str, width: int = 300, quality: int = 90):
        try:
            resp = r.get(f"{self.url}/emby/Items/{item_id}/Images/Backdrop?maxWidth={width}&quality={quality}", headers=self.headers)
            if resp.status_code != 204 and resp.status_code != 200:
                return False, {'error': "🤕Emby 服务器连接失败!"}
            return True, resp.content
        except Exception as e:
            return False, {'error': e}

    async def items(self, user_id: str, item_id: str):
        try:
            resp = r.get(f"{self.url}/emby/Users/{user_id}/Items/{item_id}", headers=self.headers)
            if resp.status_code != 204 and resp.status_code != 200:
                return False, {'error': "🤕Emby 服务器连接失败!"}
            return True, resp.json()
        except Exception as e:
            return False, {'error': e}

    async def get_emby_report(self, types: str = 'Movie', user_id: str | None = None, days: int = 7, end_date=None, limit: int = 10):
        try:
            if not end_date:
                end_date = datetime.now(timezone(timedelta(hours=8)))
            start_time = (end_date - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
            end_time = end_date.strftime('%Y-%m-%d %H:%M:%S')
            sql = "SELECT UserId, ItemId, ItemType, "
            if types == 'Episode':
                sql += " substr(ItemName,0, instr(ItemName, ' - ')) AS name, "
            else:
                sql += "ItemName AS name, "
            sql += "COUNT(1) AS play_count, "
            sql += "SUM(PlayDuration - PauseDuration) AS total_duarion "
            sql += "FROM PlaybackActivity "
            sql += f"WHERE ItemType = '{types}' "
            sql += f"AND DateCreated >= '{start_time}' AND DateCreated <= '{end_time}' "
            sql += "AND UserId not IN (select UserId from UserList) "
            if user_id:
                sql += f"AND UserId = '{user_id}' "
            sql += "GROUP BY name "
            sql += "ORDER BY total_duarion DESC "
            sql += "LIMIT " + str(limit)
            resp = r.post(f'{self.url}/emby/user_usage_stats/submit_custom_query', headers=self.headers, json={"CustomQueryString": sql, "ReplaceUserId": False})
            if resp.status_code != 204 and resp.status_code != 200:
                return False, {'error': "🤕Emby 服务器连接失败!"}
            ret = resp.json()
            if len(ret.get("colums", [])) == 0:
                return False, ret.get("message")
            return True, ret.get("results")
        except Exception as e:
            return False, {'error': e}

    async def get_emby_userip(self, user_id: str):
        sql = f"SELECT DISTINCT RemoteAddress,DeviceName FROM PlaybackActivity WHERE RemoteAddress NOT IN ('127.0.0.1', '172.17.0.1') and UserId = '{user_id}'"
        data = {"CustomQueryString": sql, "ReplaceUserId": True}
        resp = r.post(f'{self.url}/emby/user_usage_stats/submit_custom_query?api_key={emby_api}', json=data)
        if resp.status_code != 204 and resp.status_code != 200:
            return False, {'error': "🤕Emby 服务器连接失败!"}
        ret = resp.json()
        if len(ret.get("colums", [])) == 0:
            return False, ret.get("message")
        return True, ret.get("results")


emby = Embyservice(emby_url, emby_api)
