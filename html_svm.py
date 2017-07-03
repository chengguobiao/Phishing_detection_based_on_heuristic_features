# !/usr/bin/python
#-*-coding:utf-8-*-

'''
__Author__:沂水寒城
功能：基于html的特征检测仿冒网站
'''


import re
import urllib2
from lxml import etree
from bs4 import BeautifulSoup


def get_html_length(Html):
    '''
    获取Html的长度
    '''
    return len(Html)


def get_div_num(Html):
    '''
    获得html中div标签的数量
    '''
    match = re.findall(r"<div.*?>(.*?)</div>", Html)
    if len(match) > 13:
        return 1
    else:
        return 0


def get_embed_num(Html):
    '''
    获得HTML中的<embed>标签数量(特征大多为0)
    '''
    match = re.compile(r'<embed[^>]+/>|<embed[^>]+[^/>]></embed>')
    embed_list = re.findall(match, Html)
    return len(embed_list)


def get_iframe_num(Html):
    '''
    获得html中的<iframe>标签的数量(特征大多为0)
    '''
    match = re.compile(r'<iframe[^>]+/>|<iframe[^>]+[^/>]></iframe>')
    iframe_list = re.findall(match, Html)
    return len(iframe_list)


def get_applet_num(Html):
    '''
    获得html中的<applet>标签的数量(特征大多为0)
    '''
    match = re.compile(r'<applet[\s\S]+/applet>')
    applet_list = re.findall(match, Html)
    return len(applet_list)


def get_frame_num(Html):
    '''
    获得html中的<frame>标签的数量(特征大多为0)
    '''
    match = re.compile(r'<frame[^>]+/>|<frame[^>]+[^/>]></frame>')
    frame_list = re.findall(match, Html)
    return len(frame_list)


def get_form_get_num(Html):
    '''
    提取form中的get方法数量(特征大多为0)
    '''
    match = re.compile(r'<form[\s\S]+method="get"[\s\S]+/form>')
    get_list = re.findall(match, Html)
    return len(get_list)


def get_form_post_num(Html):
    '''
    提取form中的post方法数量(特征大多为0和1)
    '''
    match = re.compile(r'<form[\s\S]+method="post"[\s\S]+/form>')
    post_list = re.findall(match, Html)
    if len(post_list) > 1:
        return 1
    else:
        return 0


def get_js_long(Html):
    '''
    计算网页中的script内容长度(特征大多为0)
    '''
    script_num = 0
    # 抽取script包含的内容
    re_alert = re.compile(r">\s*alert[\S\s]*</script>")
    alert_content = re_alert.findall(Html)
    # 计算script中内容的字符长度
    if alert_content != []:
        for once_alert_content in alert_content:
            script_num += len(once_alert_content)
    if script_num > 0:
        return 1
    else:
        return 0


def get_divonClick_num(Html):
    '''
    计算html中<div onClick = window.open()>方法出现的数量(均为0)
    '''
    match = re.compile(r'<div\s[\S]*onClick=window.open()')
    divonClick_list = re.findall(match, Html)
    return len(divonClick_list)


def get_headtitlebody_num(Html):
    '''
    计算html中<head><title><body>的数量
    '''
    #match = re.compile(r'<head>[\s\S]*<title>[\s\S]*<body>[\s\S]*</head>')
    head_num = 0
    title_num = 0
    body_num = 0
    match_head = re.compile(r'<head>[\s\S]*</head>')
    match_title = re.compile(r'<title>[\s\S]*</title>')
    match_body = re.compile(r'<body[\s\S]*body>')
    head_list = re.findall(match_head, Html)
    title_list = re.findall(match_title, Html)
    body_list = re.findall(match_body, Html)
    for head_content in head_list:
        head_num += head_content.count('<head>')
    for body_content in body_list:
        body_num += body_content.count('<body')
    for title_content in title_list:
        title_num += title_content.count('<title>')
    if head_num > 0:  # 1或者2
        head_num = 1
    else:
        head_num = 0
    if body_num > 0:  # 1或者2
        body_num = 1
    else:
        body_num = 0
    if title_num > 0:  # 1或者2
        title_num = 1
    else:
        title_num = 0
    return [head_num, title_num, body_num]
    #return head_list, title_list, body_list
    # print len(head_list), len(title_list), len(body_list)
    # print head_num, title_num, body_num


def get_input_num(Html):
    '''
    计算html中的<input>标签数量
    '''
    #match = re.compile(r'<input[\s\S]*/>')
    input_num = 0
    match = re.compile(r'<input')
    input_list = re.findall(match, Html)
    for input_content in input_list:
        input_num += input_content.count('<input')
    if input_num > 5:
        return 1
    else:
        return 0


def get_form_num(Html):
    '''
    计算html中的<form>表单数量
    '''
    form_num = 0
    match = re.compile(r'<form[\s\S]*</form>')
    form_list = re.findall(match, Html)
    # print 'form_list is :', form_list
    # print 'len_form_list is :', len(form_list)
    for form_content in form_list:
        form_num += form_content.count('</form>')
    #form = form_list[0]
    #form_num_list = form.split('</form>')
    #form_num = len(form_num_list) - 1
    # print form_num
    if form_num > 0:#以1，2，3居多，有较大值
        return 1
    else:
        return 0


def get_SetIntervel_num(html):
    '''
    获取页面html中SetIntervel()方法数量
    '''
    match = re.compile(r'setInterval\([\s\S]*\)', re.I)
    setInterval_list = re.findall(match, html)
    if len(setInterval_list)>0:#多数为0.有极少数为1
        return 1
    else: 
        return 0


def get_SetTimeout_num(html):
    '''
    获取页面html中SetTimeout()方法数量
    '''
    match = re.compile(r'setTimeout\([\s\S]*\)', re.I)
    setTimeout_list = re.findall(match, html)
    if len(setTimeout_list) > 0:#多数为0.有少数为1
        return 1
    else:
        return 0


def get_onload_num(html):
    '''
    获取页面html中onload()方法数
    '''
    match = re.compile(r'onload\([\s\S]\)', re.I)
    onload_list = re.findall(match, html)
    if len(onload_list)>0:#多数为0.微量为1
        return 1
    else:
        return 0


def get_onerror_num(html):
    '''
    获取页面html中onerror()方法数  #测试均为0
    '''
    match = re.compile(r'onerror\([\s\S]*\)', re.I)
    onerror_list = re.findall(match, html)
    return len(onerror_list)


def get_js_functions_num(html):
    '''
    获取页面html中js调用的方法数
    '''
    match_script = re.compile(r'<script>[\s\S]+</script>')
    script_list = re.findall(match_script, html)
    '''代码报错，数组越界
    script = script_list[0]
    '''
    match_functions = re.compile(r'function')
    functions_list = re.findall(match_functions, script)
    return len(functions_list)


def get_script_functions_num(html):
    '''
    获取页面html中<script>标签的方法数
    '''
    match_script = re.compile(r'<script>[\s\S]+</script>')
    script_list = re.findall(match_script, html)
    '''代码报错，数组越界
    script = script_list[0]
    '''
    match_functions = re.compile(r'function')
    functions_list = re.findall(match_functions, script)
    return len(functions_list)


def get_pop_num(html):
    '''
    获取页面html中pop()方法数
    '''
    match = re.compile(r'pop\([\s\S]*\)', re.I)
    pop_list = re.findall(match, html)
    if len(pop_list) >0:
        return 1
    else:
        return 0


def get_exec_num(html):
    '''
    获取页面html中的exec()方法数
    '''
    match = re.compile(r'exec\([\s\S]*\)', re.I)
    exec_list = re.findall(match, html)
    if len(exec_list) > 0:
        return 1
    else:
        return 0


def get_Dispatchevent_num(html):
    '''
    获取页面html中DispatchEvent()方法数
    '''
    match = re.compile(r'dispatchevent\([\s\S]*\)', re.I)
    dispatchevent_list = re.findall(match, html)
    return len(dispatchevent_list)
    # 极少数为0


def get_Eval_num(html):
    '''
    获取页面html中Eval()方法数
    '''
    match = re.compile(r'Eval\([\s\S]*\)', re.I)
    eval_list = re.findall(match, html)
    if len(eval_list) > 0:
        return 1
    else:
        return 0


def get_attachevent_num(html):
    '''
    获取页面html中attachEvent()方法数
    '''
    match = re.compile(r'attachevent\([\s\S]*\)', re.I)
    attachevent_list = re.findall(match, html)
    if len(attachevent_list) > 0:
        return 1
    else:
        return 0


def get_formcharcode_num(html):
    '''
    获取页面html中formcharcode()方法数
    '''
    match = re.compile(r'formcharcode\([\s\S]*\)', re.I)
    formcharcode_list = re.findall(match, html)
    return len(formcharcode_list)
    #测试文件均为0


def extract_html_feature(html_path):
    '''
    读取html文件，并抽取title分词后名词、正文关键词、ICP号, 均为字符串格式, 
    关键词由'/'分隔
    '''
    html = utf8_open_file(html_path)
    title_keyword = get_title_cut(html)
    text_keyword = get_html_keyword(html)
    ICP = get_ICP(html)  # 抽取html中ICP
    return title_keyword, text_keyword, ICP
    #这个函数有两个函数没有
    

def get_html_vector(Html):
    heuristic_vector = []
    soup = BeautifulSoup(Html, "lxml")
    if soup != None:
        heuristic_vector.append(get_html_length(Html))
        heuristic_vector.append(get_div_num(Html))
        heuristic_vector.append(get_embed_num(Html))
        heuristic_vector.append(get_iframe_num(Html))
        heuristic_vector.append(get_applet_num(Html))
        heuristic_vector.append(get_frame_num(Html))
        heuristic_vector.append(get_form_get_num(Html))
        heuristic_vector.append(get_form_post_num(Html))
        heuristic_vector.append(get_js_long(Html))
        heuristic_vector.append(get_divonClick_num(Html))
        heuristic_vector.extend(get_headtitlebody_num(Html))
        heuristic_vector.append(get_input_num(Html))
        heuristic_vector.append(get_form_num(Html))
        heuristic_vector.append(get_SetIntervel_num(Html))
        heuristic_vector.append(get_SetTimeout_num(Html))
        heuristic_vector.append(get_onload_num(Html))
        heuristic_vector.append(get_onerror_num(Html))
        heuristic_vector.append(get_form_get_num(Html))
        heuristic_vector.append(get_form_post_num(Html))
        heuristic_vector.append(get_pop_num(Html))
        heuristic_vector.append(get_exec_num(Html))
        heuristic_vector.append(get_Dispatchevent_num(Html))
        heuristic_vector.append(get_Eval_num(Html))
        heuristic_vector.append(get_attachevent_num(Html))
        heuristic_vector.append(get_formcharcode_num(Html))
        heuristic_vector.append(get_form_get_num(Html))
        heuristic_vector.append(get_form_post_num(Html))
    return heuristic_vector

if __name__ == '__main__':
    html_baidu = urllib2.urlopen('http://www.baidu.com').read()
    baidu_vector = []
    baidu_vector = get_html_vector(html_baidu)
    print baidu_vector
    '''
    [111666, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
    '''
