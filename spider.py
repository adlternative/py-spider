import os
import requests as req
import re
from bs4 import BeautifulSoup as bs
import sys
import pandas as pd
import numpy as np

url = "https://maoyan.com/board/4?"

movie_attrs = ['排名', '电影名', '主演', '上映时间', '评分']
movie_ranks = []
movie_names = []
movie_actors = []
movie_times = []
movie_scores = []

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,bs;q=0.7,fr;q=0.6",
    "Connection": "keep-alive",
    "Host": "maoyan.com",
    "sec-ch-ua-mobile": "?0",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",  # 注意下面Cookie需要到浏览器开发者工具中拿
    "Cookie": "__mta=247395259.1619520687299.1619784125856.1619786855408.48; uuid_n_v=v1; uuid=7F25B8E0A74611EB9FD2CDCBCD6867A9DF2C62206F82401FA4F151417FC2528C; _lxsdk_cuid=17912f478b2c8-0ae251f66e362a-172f1a0c-1fa400-17912f478b2c8; _lxsdk=7F25B8E0A74611EB9FD2CDCBCD6867A9DF2C62206F82401FA4F151417FC2528C; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; _csrf=c7caa0899d353fd4abaca0c0d1287efad6683bfc4b22a24bee1fa825d920f213; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1619520682,1619534916,1619535077,1619707579; __mta=247395259.1619520687299.1619766636911.1619778252346.28; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1619786855; _lxsdk_s=179229c199a-19-48e-f6d%7C%7C16"
}


def getUrl(url, if_print, store_to_file):
    res = req.get(url, headers=header)
    i = bs(res.text, 'html.parser')
    if if_print:
        if store_to_file:
            with open("a.html", "w") as f:
                print(i, file=f)
        else:
            print(i)
    if i.title.string == "猫眼验证中心":
        print("反爬虫老哥来了,溜！", file=sys.stderr)
        exit(0)
    return i


def getLocal(path, if_print, store_to_file):
    with open(path, "r") as f:
        i = bs(f, 'html.parser')
        if if_print:
            if store_to_file:
                with open("a.html", "w") as f:
                    print(i, file=f)
            else:
                print(i)
        return i


def localTest():
    if False == os.path.exists("source/"):
        os.makedirs("source/")
    soup = getLocal("./b.html", False, False)
    # print("标题的html数据：", soup.title)
    # print("标题的html数据标签：", soup.title.name)
    # print("标题html父标签：", soup.title.parent.name)
    # print("标题：", soup.title.string)
    # print("似乎是第一个段落：", soup.p)
    # print("第一个段落标签属性：", soup.p['class'])
    # print("第一个锚元素：", soup.a)
    # for i in soup.find_all('a'):
    #   print("所有锚元素：", i)
    # for link in soup.find_all('img'):
    #     print(link.get('data-src'))
    # print("所有文字:", soup.get_text())
    # for dd in soup.find_all('dd'):
    #     for child in dd.children:
    #         print("子结点 ",child)
    # for dd in soup.find_all('dd'):
    #     for child in dd.descendants:
    #         print("子孙递归 ",child)
    for dd in soup.find_all('dd'):
        print("序号 ", dd.i.string)
        graph_link = dd.find_all('img')[1]['data-src']
        print("download %s".format(graph_link))
        html = req.get(graph_link)
        if html.ok:
            img_name = "source/" + dd.i.string + ".jpg"
            with open(img_name, 'wb+') as file:
                file.write(html.content)
                file.flush()

        paragraph = dd.find('p', class_="name")
        print("电影名 ", paragraph.string)
        paragraph = dd.find('p', class_="star")
        print(paragraph.string.lstrip())
        paragraph = dd.find('p', class_="releasetime")
        print(paragraph.string)
        scores = dd.find(
            'div', class_="movie-item-number score-num").p.find_all('i')
        print(
            "评分 ", scores[0].string+scores[1].string)
        print()
        # class_val = paragraph['class']
        # if class_val == "name":
        #     print("电影名", paragraph.string)
        # elif class_val == "star":
        #     print("演员", paragraph.string)
        # elif class_val == "releasetime":
        #     print("上映时间", paragraph.string)
        # elif class_val == "score":
        #     print("评分", paragraph.string)


def netTest(url):
    if False == os.path.exists("source/pictures"):
        os.makedirs("source/pictures")
    soup = getUrl(url, False, False)
    for dd in soup.find_all('dd'):

        ''' 排名 '''
        # print("序号 ", dd.i.string)
        movie_ranks.append(dd.i.string)

        ''' 下载图片 '''
        graph_link = dd.find_all('img')[1]['data-src']
        print("download {}".format(graph_link))
        html = req.get(graph_link)
        if html.ok:
            img_name = "source/pictures" + dd.i.string + ".jpg"
            with open(img_name, 'wb+') as file:
                file.write(html.content)
                file.flush()
            print("download to {}".format(img_name))
        else:
            print("下载 %s 失败！".format(graph_link), file=sys.stderr)
            sys.exit(1)

        ''' 电影名 '''
        paragraph = dd.find('p', class_="name")
        movie_names.append(paragraph.string)

        ''' 主演 '''
        paragraph = dd.find('p', class_="star")
        movie_actors.append(paragraph.string.strip().lstrip('主演： '))

        ''' 上映时间 '''
        paragraph = dd.find('p', class_="releasetime")
        movie_times.append(paragraph.string.lstrip('上映时间： '))

        ''' 分数 '''
        try:
            scores = dd.find(
                'div', class_="movie-item-number score-num").p.find_all('i')
            if scores:
                score = scores[0].string+scores[1].string
                movie_scores.append(score)
            else:
                movie_scores.append('')
        except AttributeError as e:
            movie_scores.append('')


def main():
    moveMetaData = [movie_ranks, movie_names,
                    movie_actors, movie_times, movie_scores]
    for i in range(0, 100, 10):
        url = "https://maoyan.com/board/4?offset=" + str(i)
        netTest(url)
    max_length = max([len(l) for l in moveMetaData])  # 求最大长度
    data = [l + [None] * (max_length-len(l))
            for l in moveMetaData]  # 用None补全
    df = pd.DataFrame(dict(zip(movie_attrs, data)))
    df.to_csv('./source/test.csv', index=False)


if __name__ == '__main__':
    main()
