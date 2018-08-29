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
        return json('hi 请输入短视频链接')

    # 加载该资源获取页面
    page = requests.get(uri)
    tree = html.fromstring(page.text)

    new_uri = tree.xpath('//meta[@property="og:video:url"]/@content')[0]

    # 加载new_uri, 获取真正视频名称
    res = request.get(new_uri)

    return json(res.url)


if __name__ == '__main__':
    app.run(host=settings.HOST, port=settings.PORT)