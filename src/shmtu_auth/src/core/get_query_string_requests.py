# -*- coding: utf-8 -*-

import requests


def get_text_code(url: str) -> (str, int):
    # noinspection PyBroadException
    try:
        response = requests.get(url)
        return response.text, response.status_code
    except Exception:
        return "", 0


def is_connect_by_google() -> bool:
    url = "http://www.google.cn/generate_204"
    res_string, res_code = get_text_code(url)
    # print("Connect Status Check", url, res_string, res_code)
    result = res_code == 204
    # print("Connect Status Check", url, result)
    return result


def get_query_string_by_url(url: str = "http://www.shmtu.edu.cn") -> str:
    if is_connect_by_google():
        return ""
    res_string, res_code = get_text_code(url)
    # print(url, res_code)
    if res_code != 200:
        return ""
    list_spilt = res_string.split("'")
    if len(list_spilt) > 1:
        login_page_url = list_spilt[1]
        list_spilt_url = login_page_url.split("?")
        if len(list_spilt_url) > 1 and list_spilt_url[0].index("index.jsp") > 0:
            query_string = list_spilt_url[1]
            query_string = query_string.replace("&", "%26").replace("=", "%3D")
            # github上其他学校的锐捷都是下面这样操作的，不清楚以哪个为准。
            # query_string = query_string.replace("&", "%2526").replace("=", "%253D")
            return query_string

    return ""


def get_query_string_by_baidu(url="http://www.baidu.com"):
    return get_query_string_by_url(url)


if __name__ == "__main__":
    print(get_query_string_by_url("http://www.shmtu.edu.cn"))
