#!/usr/bin/env python3
# coding=utf-8

from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
from re import compile
import os

TXT = compile('.*format=txt')
SRT = compile('.*format=srt')
LECTURE = compile('.*\/(\w+)\.pdf')
FORUM = compile('.*forum_id.*')
MP4 = compile('.*download\.mp4.*')

CWD = os.getcwd()

def get_Download(url):
    if not url:
        print("please input url, exit")
        return 1

    contents = urlopen(url).read()
    soup = bs(contents, 'html.parser')

    all_resources = soup.find('div', attrs={'class':'course-lectures-list'})
    weeks = all_resources.findAll('div', attrs={'class':'course-item-list-header expanded'})
    classs = all_resources.findAll('ul', attrs={'class':'course-item-list-section-list'})

    if len(weeks) != len(classs):
        print('There is some wrong, week is less!')
        return 1

    counts = len(weeks)
    for i in range(counts):
        week = weeks[i]
        class_name = week.find('h3')
        class_name = class_name.get_text()
        class_name = class_name.encode('utf8')
        #print('class_name:', class_name)
        class_name = class_name.split(b' ')
        class_name.pop(0)
        class_name.pop(0)
        class_name = b'_'.join(class_name)
        class_name = class_name.decode('utf8')
        class_path = os.path.join(CWD, class_name)
        if not os.path.exists(class_path):
            os.makedirs(class_path)

        os.chdir(class_path)

        clss = classs[i]
        resources = clss.findAll('li')
        for resource in resources:
            heards = resource.find('a')
            name = heards.get_text()
            name = name.strip('\n')
            name = name.strip(' ')
            name = name.split(' ')
            name = '_'.join(name)
            name = name.replace('"', ' ')
            print('default name:', name)
            lecture = resource.find('div', attrs={'class':'course-lecture-item-resource'})
            links = lecture.findAll('a', attrs={'target':'_new'})
            for link in links:
                href = link.get('href')
                if FORUM.match(href):
                    print("it's a forum link, continue")
                    continue
                match = LECTURE.search(href)
                if match:
                    name = match.groups(0)[0]
                    name = name.strip('\n')
                    name = name.strip(' ')
                    name = name.split(' ')
                    name = '_'.join(name)
                    name = name.replace('"', ' ')
                    pdf_name = "%s.pdf" % name
                    if os.path.exists(pdf_name):
                        continue
                    cmd = 'wget -O "%s" %s' % (pdf_name, href)
                    print(cmd)
                    os.system(cmd)
                elif TXT.match(href):
                    txt_name = "%s.txt" % name
                    if os.path.exists(txt_name):
                        continue
                    cmd = 'wget -O "%s" %s' % (txt_name, href)
                    print(cmd)
                    os.system(cmd)
                elif SRT.match(href):
                    srt_name = "%s.srt" % name
                    if os.path.exists(srt_name):
                        continue
                    cmd = 'wget -O "%s" %s' % (srt_name, href)
                    print(cmd)
                    os.system(cmd)
                elif MP4.match(href):
                    mp4_name = "%s.mp4" % name
                    if os.path.exists(mp4_name):
                        continue
                    cmd = 'wget -O "%s" %s' % (mp4_name, href)
                    print(cmd)
                    os.system(cmd)
                else:
                    pptx_name = "%s.pptx" % name
                    if os.path.exists(pptx_name):
                        continue
                    cmd = 'wget -O "%s" %s' % (pptx_name, href)
                    print(cmd)
                    os.system(cmd)

if __name__ == '__main__':
    url = 'https://class.coursera.org/ml-003/lecture'
    get_Download(url)
