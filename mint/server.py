from sanic import Sanic
from sanic.response import json
from mint import settings
import requests
from mint.common import redis_client
from mint.util.sanic_jinja import render
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

    redis_client.lpush("%s:start_urls" % settings.SPIDER_NAME, new_uri)

    return json({'code': 0, 'message': None, 'rsp': new_uri})


@app.get('/play')
async def play(request):
    key = request.json.get('sign', None)

    sign = redis_client.hget('mint', key)

    return render('index.html', request, sign=sign)


if __name__ == '__main__':
    app.run(host=settings.HOST, port=settings.PORT)
