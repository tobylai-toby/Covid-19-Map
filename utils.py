from typing import Union
import requests
import json
from lxml import etree
from pprint import pprint
from pyecharts.charts import Map
from pyecharts import options as opts


def getAllCovid19Data():
    req = requests.get("https://voice.baidu.com/act/newpneumonia/newpneumonia",
                       headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"})
    req.encoding = req.apparent_encoding
    dom = etree.HTML(req.text, etree.HTMLParser())
    return json.loads(dom.xpath('//*[@id="captain-config"]/text()')[0])

# 本土累计
# @return


def chinaCovid19Map(type_=["confirmed"],size=["900px","500px"]) -> Union[dict, Map]:
    data = getAllCovid19Data()
    chinaData = data["component"][0]["caseList"]

    provinces = [cdata["area"] for cdata in chinaData]  # 省份
    confirmed = [int(cdata["confirmed"]) for cdata in chinaData]  # 累计确诊
    died = [int(cdata["died"]) for cdata in chinaData]  # 累计死亡
    crued = [int(cdata["crued"]) for cdata in chinaData]  # 累计治愈
    asymptomatic = [int(cdata["asymptomatic"]) for cdata in chinaData]  # 累计无症状

    max_aver=0
    max_=0
    all_=["confirmed","died","crued","asymptomatic"]
    for x in all_:
        if x in type_:
            max_+=max(eval(x))
            max_aver+=max(eval(x))/len(eval(x))

    _ill=0
    _ill+=sum(confirmed)+sum(asymptomatic)

    cn_map = Map(
        init_opts=opts.InitOpts(width=size[0], height=size[1])
    ).set_global_opts(
        title_opts=opts.TitleOpts(subtitle=f"累计确诊/无症状：{_ill}"),
        visualmap_opts=opts.VisualMapOpts(max_=max_aver),
    )

    if "confirmed" in type_:
        cn_map.add("累计确诊", [tuple(zp) for zp in zip(provinces, confirmed)], "china",
                        is_map_symbol_show=False)
    if "died" in type_:
        cn_map.add("累计死亡", [tuple(zp) for zp in zip(provinces, died)], "china",
                        is_map_symbol_show=False)
    if "crued" in type_:
        cn_map.add("累计治愈", [tuple(zp) for zp in zip(provinces, crued)], "china",
                        is_map_symbol_show=False)
    if "asymptomatic" in type_:
        cn_map.add("累计无症状", [tuple(zp) for zp in zip(provinces, asymptomatic)], "china",
                        is_map_symbol_show=False)
    return chinaData, cn_map

def chinaCovid19MapRelative(type_=["confirmed"],size=["900px","500px"]) -> Union[dict, Map]:
    data = getAllCovid19Data()
    chinaData = data["component"][0]["caseList"]

    provinces = [cdata["area"] for cdata in chinaData]  # 省份
    confirmed = [int(cdata["confirmedRelative"]) for cdata in chinaData]  # 累计确诊
    died = [int(cdata["diedRelative"]) for cdata in chinaData]  # 累计死亡
    crued = [int(cdata["curedRelative"]) for cdata in chinaData]  # 累计治愈
    asymptomatic = [int(cdata["asymptomaticRelative"] or "0") for cdata in chinaData]  # 累计无症状

    max_aver=0
    max_=0
    all_=["confirmed","died","crued","asymptomatic"]
    for x in all_:
        if x in type_:
            max_+=max(eval(x))
            max_aver+=max(eval(x))/len(eval(x))

    _ill=0
    _ill+=sum(confirmed)+sum(asymptomatic)

    cn_map = Map(
        init_opts=opts.InitOpts(width=size[0], height=size[1])
    ).set_global_opts(
        title_opts=opts.TitleOpts(subtitle=f"新增确诊/无症状：{_ill}"),
        visualmap_opts=opts.VisualMapOpts(max_=max_aver),
    )

    if "confirmed" in type_:
        cn_map.add("新增确诊", [tuple(zp) for zp in zip(provinces, confirmed)], "china",
                        is_map_symbol_show=False)
    if "died" in type_:
        cn_map.add("新增死亡", [tuple(zp) for zp in zip(provinces, died)], "china",
                        is_map_symbol_show=False)
    if "crued" in type_:
        cn_map.add("新增治愈", [tuple(zp) for zp in zip(provinces, crued)], "china",
                        is_map_symbol_show=False)
    if "asymptomatic" in type_:
        cn_map.add("新增无症状", [tuple(zp) for zp in zip(provinces, asymptomatic)], "china",
                        is_map_symbol_show=False)
    return chinaData, cn_map


# _, cn_map = chinaCovid19Map(["confirmed","died","crued","asymptomatic"])
# cn_map.render("china_covid19_map.html")
