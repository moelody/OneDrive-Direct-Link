# coding=utf-8
import requests
from flask import Flask, request, Response
from cachetools.func import ttl_cache

app = Flask(__name__)


@ttl_cache(1024, ttl=600)
def get_direct_url(ch, share_token):
    url_step1 = 'https://1drv.ms/{ch}/s!{share_token}'.format(
        ch=ch,  # the ch could be w u t or more
        share_token=share_token
    )
    resp_step1 = requests.get(url_step1, timeout=10, allow_redirects=False)
    url_step2 = resp_step1.headers['Location']
    url_step3 = url_step2.replace('/redir?', '/download?')
    resp_step3 = requests.get(url_step3, timeout=10, allow_redirects=False)
    url_final = resp_step3.headers['Location']

    return url_final


@app.route('/<ch>/s!<share_token>')
def share_ts(ch, share_token):
    url_direct = get_direct_url(ch, share_token)

    if 'txt' in request.args:
        # display plain text
        return url_direct
    else:
        # 301 redirect
        return Response('',
                        status=301,
                        headers={'Location': url_direct},
                        content_type='text/plain'
                        )


@app.route('/')
def index():
    return """<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>OneDrive直链提取工具</title>
<meta name="keywords" content="OneDrive,direct,download,link,OneDrive direct download,直链"/>
<meta name="description" content="通过地址转换获取OneDrive直链"/>

<script>
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?6d5ecb8da95b157d45f57c69467b05c2";
  var s = document.getElementsByTagName("script")[0]; 
  s.parentNode.insertBefore(hm, s);
})();
</script>

</head>
<body>
<h1>OneDrive直链提取使用说明</h1>
<p>将 OneDrive分享地址中"https://1drv.ms/"调整为"https://onedrive-direct-link.herokuapp.com/"，实现直链获取。</p>

<a href='https://www.moelody.com'>捐赠支持本站发展</a>

<h2>使用说明</h2>
1. 获取OneDrive分享链接，例如: <a href='https://1drv.ms/u/s!Aiw77soXua44hb4CEu6eSveUl0xUoA'>https://1drv.ms/u/s!Aiw77soXua44hb4CEu6eSveUl0xUoA</a><br>
2. 获取直分享链接中<b>"https://1drv.ms/"</b> 调整为 <b>"https://onedrive-direct-link.herokuapp.com"</b>, <br>成为 <a href='https://onedrive-direct-link.herokuapp.com/u/s!Aiw77soXua44hb4CEu6eSveUl0xUoA'>https://onedrive-direct-link.herokuapp.com/u/s!Aiw77soXua44hb4CEu6eSveUl0xUoA</a><br>

</body>
</html>
"""


if __name__ == '__main__':
    app.run()
