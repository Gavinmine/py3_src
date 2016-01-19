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
        class_path = os.path.join(CWD, class_name)
        print('class:', class_path)
        if not os.path.exists(class_path)
            os.makedirs(class_path)

        os.chdir(class_path)

        clss = classs[i]
        resources = clss.findAll('li')
        for resource in resources:
            heards = resource.find('a')
            name = heards.get_text()
            name = name.strip('\n')
            name = name.strip(' ')
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
                    #name = match.groups(0)[0]
                    cmd = 'wget -O %s.pdf %s' % (name, href)
                    print(cmd)
                    os.system(cmd)
                elif TXT.match(href):
                    cmd = 'wget -O %s.txt %s' % (name, href)
                    print(cmd)
                    os.system(cmd)
                elif SRT.match(href):
                    cmd = 'wget -O %s.srt %s' % (name, href)
                    print(cmd)
                    os.system(cmd)
                elif MP4.match(href):
                    cmd = 'wget -O %s.mp4 %s' % (name, href)
                    print(cmd)
                    os.system(cmd)
                else:
                    cmd = 'wget -O %s.pptx %s' % (name, href)
                    print(cmd)
                    os.system(cmd)

if __name__ == '__main__':
    url = 'https://class.coursera.org/ml-003/lecture'
    get_Download(url)