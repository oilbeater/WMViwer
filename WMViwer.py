#!/usr/bin/python

import ConfigParser
import urllib2
import re
import time

def item_parse(item):
    title = re.findall(r'<title>(.*?)</title>',item,re.IGNORECASE|re.MULTILINE|re.DOTALL)[0]
    raw_link = re.findall(r'<link>(.*?)</link>',item,re.IGNORECASE|re.MULTILINE|re.DOTALL)[0]
    link = re.findall(r'(http:.*)]]>',raw_link,re.IGNORECASE|re.MULTILINE|re.DOTALL)[0]
    thread_id = re.findall(r'threadid=(\d*)',link,re.IGNORECASE|re.MULTILINE|re.DOTALL)[0]
    raw_data = re.findall(r'<description>(.*?)</description>',item,re.IGNORECASE|re.MULTILINE|re.DOTALL)[0]
    data = re.findall(r'CDATA\[(.*?)]',raw_data,re.IGNORECASE|re.MULTILINE|re.DOTALL)[0]
    return title,link,int(thread_id),data

config = ConfigParser.ConfigParser()
with open("config.ini","r") as cfgfile:
    config.readfp(cfgfile)
fresh_time = int(config.get("default","fresh_time"))
base_url = config.get("default","base_url")
boards = config.get("default","boards").split(",")
show_content = config.get("default","show_content")
board_tops = {}.fromkeys(boards,0)

print "----------------------------------------------"
print "Thank you to use WM Viewer"
print "The boards you are tracing : " + ",".join(boards)
print "----------------------------------------------"


while True:
    for board in boards:
        board_url = base_url + board
        xml = unicode(urllib2.urlopen(board_url).read(),'gbk')
        items = re.findall(r'<item .*?>.*?</item>',xml,re.IGNORECASE|re.MULTILINE|re.DOTALL)
        for item in items[::-1]:
            item_info = item_parse(item)
            if item_info[2] > board_tops[board]:
                board_tops[board] = item_info[2]
                print item_info[0]
                print item_info[1]
                if show_content == "true":
                    print item_info[3]
                print ""
    time.sleep(fresh_time)
