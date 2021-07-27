import sys
from urllib.parse import parse_qsl
from urllib.parse import urlencode

import xbmc
import xbmcgui
import xbmcplugin

from lib import util

BASE_URL = ""
VIDEO_SERVICE_URL = ""
IMAGE_URL = ""


# https://vod.pl/api/items/categories?lang=pl&platform=ANDROID
# https://vod.pl/api/products/sections/main?lang=pl&platform=ANDROID
# https://vod.pl/api/products/7012/videos/playlist?platform=BROWSER&videoType=TRAILER&lang=pl&platform=BROWSER


BASE_COUNT = 100
BASE_CATEGORY_ID = 0

HANDLE = int(sys.argv[1])
PLUGIN_URL = sys.argv[0]
ARGS = dict(parse_qsl(sys.argv[2][1:]))


def open_folder(folder_id, page=1):
    folder_url = BASE_URL % (folder_id, BASE_COUNT, page)
    content = util.get_url_content(folder_url)

    xbmcplugin.setContent(handle=HANDLE, content="files")

    title = "VOD.PL Onet"
    url_params = []
    meta_data = []
    image_url = None
    is_folder = False

    add_dir(title, url_params, meta_data, image_url, None, is_folder)

    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)


def add_dir(name, url_params, meta_data, icon_image=None, thumbnail=None, folder=False):
    item = xbmcgui.ListItem(name)
    if icon_image is not None:
        # xbmc.log("[info] image: " + icon_image, level=xbmc.LOGINFO)
        item.setArt({'poster': icon_image, 'banner': icon_image})

    item.setInfo(type="Video", infoLabels=meta_data)

    url = PLUGIN_URL + '?' + urlencode(url_params)
    dir_item = xbmcplugin.addDirectoryItem(handle=HANDLE, url=url, listitem=item, isFolder=folder)
    return dir_item


def route(self):
    xbmc.log("[info] ARGS: " + str(ARGS), level=xbmc.LOGINFO)
    if "action" in ARGS:
        action = ARGS["action"]
    else:
        action = None

    if action is None:
        # start base action
        xbmc.log("[info] no action", level=xbmc.LOGINFO)
        open_folder(BASE_CATEGORY_ID, 1)

    elif action == "openFolder" and "id" in ARGS:
        xbmc.log("[info] opening folder with id: " + ARGS["id"], level=xbmc.LOGINFO)

        page = 1
        if "page" in ARGS:
            page = int(ARGS["page"])

        open_folder(int(ARGS["id"]), page)

    elif action == "openVideo" and "id" in ARGS:
        xbmc.log("[info] opening video with id: " + ARGS["id"], level=xbmc.LOGINFO)
        open_video(int(ARGS["id"]), "video/mp4")

    else:
        # start action
        xbmc.log("[info] no known action: " + str(ARGS), level=xbmc.LOGINFO)
