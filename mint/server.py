from sanic import Sanic
from sanic.response import json
from mint import settings
import requests

from lxml import html

app = Sanic()


@app.route('/')
async def index(request):
    return json('hi')


@app.post('/share_uri/')
async def share_uri(request):
    uri = request.json.get('uri', None)
    if not uri:
        uri = request.data.get('uri', None)
        if not uri:
            return json({'code': -1, 'message': '未收到链接地址'})

    # 加载该资源获取页面
    page = requests.get(uri)
    tree = html.fromstring(page.text)

    video_url = tree.xpath('//meta[@property="og:video:url"]/@content')[0]
    if not video_url:
        return json({'code': -1, 'message': '视频链接提取失败'})

    video_url = video_url.replace('playwm', 'play')

    return json({'code': 0, 'message': None, 'rsp': video_url})

if __name__ == '__main__':
    app.run(host=settings.HOST, port=settings.PORT)

