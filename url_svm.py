# !/usr/bin/python
#-*-coding:utf-8-*-


'''
__Author__:沂水寒城
功能：基于url的特征设计轻量级的仿冒网站检测工具
'''


import codecs
import sys
import re
from urllib2 import urlparse



RED_KEYWORDS = ["account", "admin", "administrator",
                "auth", "bank", "client", "confirm", "email", "host",
                "password", "pay", "private", "safe", "secure", "security",
                "sign", "user", "validation", "verification", "icbc"]
PATH_KEYWORDS = ["www", "net", "com", "cn"]



def geturlat(url):
    '''
    判断URL中是否含有@，？，-,_等符号
    '''
    re_script = re.compile(r'@|-|_|\?|~')
    return 1 if re_script.search(url) else 0

def get_has_ip(url):
    '''
    判断url中是否包含ip，包含返回1，不包含返回0
    '''
    compile_rule_ip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
    ip_list=re.findall(compile_rule_ip, url)
    if ip_list:
        return 1
    else:
        return 0


def geturldot(url):
    '''
    判断URL中.的个数
    '''
    dotnum = 0
    for u in url:
        if u == '.':
            dotnum += 1
    return dotnum


def get_url_length(url):
    '''
    获得URL的总长度
    '''
    return len(url)


def get_url_number_length(url):
    '''
    获得URL的最长的数字串长度
    '''
    result = 0
    match = re.findall(r"\d+", url)
    if match:
        match.sort(key=lambda x: len(x), reverse=True)
        result = len(match[0])
    return result


def get_red_keyword(url):
    '''
    判断URL中是否包含敏感词汇
    '''
    url = url.lower()
    for key in RED_KEYWORDS:
        if url.find(key) != -1:
            return 1
    return 0


def get_path_key(url):
    '''
    判断URL的路径中是否包含敏感词汇 
    '''
    url=url.replace('//', '')
    if '/' in url:
        url_path_list=url.split('/')[1:]
        if url_path_list:
            for key in PATH_KEYWORDS:
                if url_path_list.lower().find(key)!=-1:
                    return 1
    return 0
    # url_parse = urlparse(url)
    # path = url_parse.path
    # if path:
    #     for key in PATH_KEYWORDS:
    #         if path.lower().find(key) != -1:
    #             return 1
    # return 0


def get_url_vector(url):
    '''
    输入：URL，网页存储路径，关键字列表
    输出：当前网页的结果list 包含所有特征的返回值
    '''
    heuristic_vector = []
    heuristic_vector.append(get_has_ip(url))
    heuristic_vector.append(geturlat(url))
    heuristic_vector.append(geturldot(url))
    heuristic_vector.append(get_url_length(url))
    heuristic_vector.append(get_url_number_length(url))
    heuristic_vector.append(get_red_keyword(url))
    heuristic_vector.append(get_path_key(url))
    return heuristic_vector

if __name__ == '__main__':
    url='http://www.baidu.com'
    baidu_vector=get_url_vector(url)
    print baidu_vector
    '''
    [0, 0, 2, 20, 0, 0, 0]
    '''
    

    '''
    下述代码存储特征数据使用
    '''
    # white_urlresult = open('result/white_urlresult.txt', 'wb')
    # #存储白名单数据
    # white_urlresult.write('url_sign, url_dot, url_length, url_number_length, red_keyword, label')
    # white_urlresult.write('\n')
    # urlfile = open('dataset/white.txt', 'r')
    # urlfile_list = urlfile.readlines()
    # for one_url in urlfile_list:
    #     heuristic_vector = get_url_vector(one_url.strip())
    #     heuristic_url_str = [str(vector) for vector in heuristic_vector]
    #     #fw.write(url + ',Y,1,' + ','.join(heuristic_vector_str) + '\n')
    #     white_urlresult.write(','.join(heuristic_url_str) + ',' + '0' + '\n')

    # #存储黑名单数据
    # black_urlresult = open('black_urlresult.txt', 'wb')
    # id = 1
    # black_urlresult.write('id, url_sign, url_dot, url_length, url_number_length, red_keyword, label')
    # black_urlresult.write('\n')
    # urlfile = open('dataset/all.txt', 'r')
    # urlfile_list = urlfile.readlines()
    # url_list_len = len(urlfile_list)
    # i = 0
    # for one1_url in urlfile_list:
    #     heuristic_vector = get_url_vector(one1_url.strip())
    #     heuristic_url_str = [str(vector) for vector in heuristic_vector]
    #     #fw.write(url + ',Y,1,' + ','.join(heuristic_vector_str) + '\n')
    #     i += 1
    #     if i == url_list_len:
    #         black_urlresult.write(str(id) + ',' + ','.join(heuristic_url_str) + ',' + '1' )
    #         id += 1
    #     else:
    #         black_urlresult.write(str(id) + ',' + ','.join(heuristic_url_str) + ',' + '1' + '\n')
    #         id += 1
    
