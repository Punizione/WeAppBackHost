# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import urllib.request
import urllib.parse

import http.cookiejar

import json
import random
import math
import html5lib
import os
from bs4 import BeautifulSoup
import re

import ConnectUtils


school = {'1' : 'http://jwxt.gduf.edu.cn/jsxsd/xk/LoginTOXk' }

school_grade = {'1' : 'http://jwxt.gduf.edu.cn/jsxsd/ksxj/cjxc_list' }

school_rankgrade = {'1' : 'http://jwxt.gduf.edu.cn/jsxsd/kscj/djkscj_list' }

def login(schoolid, userid, userpwd):
	global school

	filename = schoolid+'#'+userid+'.txt'

	url = school.get(schoolid)
	cj = http.cookiejar.MozillaCookieJar(filename)
	opener = ConnectUtils.getUrlOpener(cj, schoolid, 'login')
	postData = urllib.parse.urlencode({'encoded': ConnectUtils.encodedInp(userid)+'%%%'+ConnectUtils.encodedInp(userpwd) })
	pattern = re.compile(ur'<div id="Top1_divLoginName" class="Nsb_top_menu_nc" style="color: #000000;"(.+?)/div>')

	try:
		op = opener.open(url, postData)
		result = op.read().decode('utf-8')
		user = re.findall(pattern, result)

		if len(user) == 0:
			statu = '101'
			return {'statu':statu }
		else:
			statu = '100'
			cj.save(ignore_discard=True, ignore_expires=True)
			username = re.findall(ur'\>(.+?)\(', user[0])[0]
			userid = re.findall(ur'\((.+?)\)', user[0])[0]

			return {'statu':statu,
					'username':username,
					'userid':userid,
					'schoolid':schoolid }
	except Exception,e:
		print(e)
		return {'statu':'102'}



def geaGrade(schoolid, userid, classTime, classNature, className, classShow):
	global school_grade

	filename = schoolid+'#'+userid+'.txt'

	if not os.path.exists(filename):
		return {'statu':'103'}

	url = school_grade.get(schoolid)
	cj = http.cookiejar.MozillaCookieJar()
	cj.load(filename, ignore_discard=True, ignore_expires=True)
	opener = ConnectUtils.getUrlOpener(cj, schoolid, 'grade')

	postData = {'kksj':classTime, 
				'kcxz':classNature, 
				'kcmc':className, 
				'xsfs':classShow }
	postData = urllib.parse.urlencode(postData)

	try:
		op = opener.open(url, postData)
		soup = BeautifulSoup(op.read().decode('utf-8'), 'html5lib', from_encoding='utf-8')
		tableDiv = soup.find_all('div', class_='Nsb_pw')
		if tableDiv:
			items = tableDiv[2].find_all('tr')
			if items:
				info = []
				if len(items)==2 and len(items[1].find_all('td'))==1:
					statu = '101'
					print('empty')
					return {'statu': statu}
				else:
					for i in range(1, len(items)):
						tds = items[i].find_all('td')
						kcbh = tds[2].text
						kcmc = tds[3].text
						kccj = tds[4].find('a').text
						kcxf = tds[5].text
						kcjd = tds[7].text
						kcsx = tds[9].text
						info.append({'kcbh':kcbh,
									'kcmc':kcmc, 
									'kccj':kccj, 
									'kcxf':kcxf, 
									'kcjd':kcjd, 
									'kcsx':kcsx})
					statu = '100'
					return {'statu':statu, 'info':info}
			else:
				return {'statu':'102'}
		else:
			return {'statu':'102'}
	except Exception,e:
		print(e)
		return {'statu':'102'}


def getRankGrade(schoolid, userid):
	global school_rankgrade
	filename = schoolid+'#'+userid+'.txt'
	if not os.path.exists(filename):
		return {'statu':'103'}
	url = school_rankgrade.get(schoolid)
	cj =  http.cookiejar.MozillaCookieJar()
	cj.load(filename, ignore_discard=True, ignore_expires=True)
	opener = ConnectUtils.getUrlOpener(cj, schoolid, 'rankgrade')
	try:
		op = opener.open(url)
		soup = BeautifulSoup(op.read().decoded('utf-8'), 'html5lib', from_encoding='utf-8')
		table = soup.find("table",attrs={"id":"dataList"})
		if table:
			li = table.find_all("tr")
			if len(li)>2:
				info = []
				for i in range(2,len(li)):
					tds = li[i].find_all("td");
					zkzh = tds[1].text
					kjkc = tds[2].text
					bscj1 = tds[3].text
					jscj1 = tds[4].text
					zcj1 = tds[5].text
					fslcj = {'bscj':bscj1, 'jscj':jscj1, 'zcj':zcj1}
					bscj2 = tds[6].text
					jscj2 = tds[7].text
					zcj2 = tds[8].text
					djlcj = {'bscj':bscj2, 'jscj':jscj2, 'zcj':zcj2}
					kjsj = tds[9].text
					item = {'zkzh':zkzh, 'kjkc':kjkc, 'fslcj':fslcj, 'djlcj':djlcj, 'kjsj':kjsj}
					info.append(item)
				return {'statu':'100','info':info}
			elif len(li)==2:
				return {'statu':'101'}
			else:
				return {'statu':'102'}
		else:
			return {'statu':'102'}
	except Exception,e:
		print(e)
		return {'statu':'102'}



