from sanic import Sanic
from sanic.response import json
from mint import settings
import requests
from mint.common import redis_client
from mint.util.sanic_jinja import render
from lxml import html

app = Sanic()
app.static('/static', settings.STATIC_URL)
app.static('/media', settings.MEDIA_URL)


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

    video_url = tree.xpath('//meta[@property="og:video:url"]/@content')[0]
    if not video_url:
        return json({'code': -1, 'message': '视频链接提取失败'})

    # 将视频链接存到redis后续在处理,
    redis_client.lpush("%s:start_urls" % settings.SPIDER_NAME, video_url)

    # 返回一个能读取视频的链接
    new_url = request.host + '/play/?' + video_url
    return json({'code': 0, 'message': None, 'rsp': new_url})


@app.get('/play')
async def play(request):
    key = request.query_string

    sign = redis_client.hget('mint', key)
    sign = str(sign, encoding="utf-8")
    return render('index.html', request, sign=sign)


if __name__ == '__main__':
    app.run(host=settings.HOST, port=settings.PORT)

