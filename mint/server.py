from sanic import Sanic
from sanic.response import json
import settings
import requests
import redis
from common import redis_client
from lxml import html
app = Sanic()


@app.route('/')
async def index(request):
    return json('hi')


@app.post('/share_uri/')
async def share_uri(request):
    uri = request.json.get('uri', None)
    if not uri:
        return json({'code': -1, 'message': '未收到链接地址'})

    # 加载该资源获取页面
    page = requests.get(uri)
    tree = html.fromstring(page.text)

    new_uri = tree.xpath('//meta[@property="og:video:url"]/@content')[0]
    if not new_uri:
        return json({'code': -1, 'message': '视频链接提取失败'})
    # 将视频链接存到redis后续在处理

    redis_client.lpush("%s:start_urls" % settings.SPIDER_NAME, uri)

    return json({'code': 0, 'message': None, 'rsp': new_uri})


if __name__ == '__main__':
    app.run(host=settings.HOST, port=settings.PORT)