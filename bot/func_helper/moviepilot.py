import requests
import json
from bot import config, moviepilot_access_token, moviepilot_url, moviepilot_username, moviepilot_password,save_config
from bot import LOGGER
import aiohttp
import asyncio

TIMEOUT = 30
# aiohttp重试装饰器
def aiohttp_retry(retry_count):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            for i in range(retry_count):
                try:
                    return await func(*args, **kwargs)
                except aiohttp.ClientError:
                    await asyncio.sleep(3)  # 延迟 3 秒后进行重试
            return None

        return wrapper

    return decorator
@aiohttp_retry(3)
async def do_request(request):
    async with aiohttp.ClientSession() as session:
        async with session.request(method=request['method'], url=request['url'], headers=request['headers'], data=request.get('data')) as response:
            if response.status == 401 or response.status == 403:
                LOGGER.error("MP Token expired, attempting to re-login.")
                success = await login()
                if success:
                    request['headers']['Authorization'] = config.moviepilot_access_token
                    return await do_request(request)
                return None
            return await response.json()
async def login():
    url = f"{moviepilot_url}/api/v1/login/access-token"
    payload = f"username={moviepilot_username}&password={moviepilot_password}"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=payload, headers=headers, timeout=TIMEOUT)
    result = response.json()
    if 'access_token' in result:
        config.moviepilot_access_token = result['token_type'] + ' ' + result['access_token']
        save_config()
        LOGGER.info("MP Login successful, token stored")
        return True
    else:
        LOGGER.error(f"MP Login failed: {result}")
        return False

async def search(title):
    if title is None:
        return False, []
    url = f"{moviepilot_url}/api/v1/search/title?keyword={title}"
    headers = {'Authorization': config.moviepilot_access_token}
    request = {'method': 'GET', 'url': url, 'headers': headers}
    try:
        data = await do_request(request)
        results = []
        if data.get("success", False):
            data = data["data"]
            for item in data:
                meta_info = item.get("meta_info", {})
                torrent_info = item.get("torrent_info", {})
                result = {
                    "title": meta_info.get("title", ""),
                    "year": meta_info.get("year", ""),
                    "type": meta_info.get("type", ""),
                    "resource_pix": meta_info.get("resource_pix", ""),
                    "video_encode": meta_info.get("video_encode", ""),
                    "audio_encode": meta_info.get("audio_encode", ""),
                    "resource_team": meta_info.get("resource_team", ""),
                    "seeders": torrent_info.get("seeders", ""),
                    "size": torrent_info.get("size", ""),
                    "labels": torrent_info.get("labels", ""),
                    "description": torrent_info.get("description", ""),
                    "torrent_info": torrent_info,
                }
                results.append(result)
        results.sort(key=lambda x: int(x["seeders"]), reverse=True)
        if len(results) > 10:
            results = results[:10]
        else:
            results = results[:-1]
        LOGGER.info("MP Search successful!")
        return True, results
    except Exception as e:
        LOGGER.error(f"MP Search failed: {e}")
        return False, []


async def add_download_task(param):
    if param is None:
        return False, None
    url = f"{moviepilot_url}/api/v1/download/add"
    headers = {'Content-Type': 'application/json',
               'Authorization': config.moviepilot_access_token}
    jsonData = json.dumps(param)
    request = {'method': 'POST', 'url': url,
               'headers': headers, 'data': jsonData}
    try:
        result = await do_request(request)
        if result.get("success", False):
            LOGGER.info(f"MP add download task successful, ID: {result['data']['download_id']}")
            return True, result["data"]["download_id"]
        else:
            LOGGER.error(f"MP add download task failed: {result.get('message')}")
            return False, None
    except Exception as e:
        LOGGER.error(f"MP add download task failed: {e}")
        return False, None

async def get_download_task():
    url = f"{moviepilot_url}/api/v1/download"
    headers = {'Authorization': config.moviepilot_access_token}
    request = {'method': 'GET', 'url': url, 'headers': headers}
    try:
        result = await do_request(request)
        data = []
        for item in result:
            data.append({'download_id': item['hash'], 'state': item['state'], 'progress': item['progress']})
        return data
    except Exception as e:
        LOGGER.error(f"MP get download task failed: {e}")
        return None