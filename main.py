# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from tornado import ioloop
import tornado.web

from tornado import httpserver
import json
import os.path
import tornado.escape
import Connect

class LoginHandler(tornado.web.RequestHandler):
	def post(self, *args, **kwargs):
		data = tornado.escape.json_decode(self.request.body)
		userid = data['userid']
		userpwd = data['userpwd']
		schoolid = data['schoolid']

		result = Connect.login(schoolid, userid, userpwd)
		statu = result['statu']
		self.set_header('Content-Type', 'application/json; charset=UTF-8')
		if statu == '100':
			self.write(json.dumps({'success': True,
									'name':result['username'],
									'userId':result['userid'],
									'schoolId':relust['schoolid']
									}))
		elif statu == '101':
			self.write(json.dumps({'success':False,
									'reason':'用户名或密码错误'
									}))
		else:
			self.write(json.dumps({'success':False,
									'reason':'连接超时'
									}))


	def get(self):
		'''
			Just For Test
		'''
		result = Connect.login('1', 'YourSchoolId', 'YourPassword')
		statu = result['statu']
		self.set_header('Connect-Type', 'application/json; charset=UTF-8')
		if statu == '100':
			self.write(json.dumps({'success':True,
									'name':result['username'],
									'userId':result['userid'],
									'schoolId':relust['schoolid']
									}))
		elif statu == '101':
			self.write(json.dumps({'success':False,
									'reason':'用户名或密码错误'
									}))
		else:
			self.write(json.dumps({'success':False,
									'reason':'连接超时'
									}))


class GradeHandler(tornado.web.RequestHandler):
	def post(self, *args, **kwargs):
		data = tornado.escape.json_decode(self.request.body)
		userid = data['userId']
		schoolid = data['schoolId']
		classTime = data['classTime']
		classNature = data['classNature']
		className = data['className']
		classShow = data['classShow']


		result = Connect.getGrade(schoolid, userid, classTime, classNature, className, classShow)
		statu = result['statu']
		self.set_header('Content-Type', 'application/json; charset=UTF-8')
		if statu == '100':
			self.write(json.dumps({'success':True, 
									'info':result['info']
									}))
		elif statu == '101':
			self.write(json.dumps({'success':True, 
									'info':'empty'
									}))
		elif statu == '103':
			self.write(json.dumps({'success':False, 
									'reason':'登陆已经失效,请重新登录!'
									}))
		else:
			self.write(json.dumps({'success':False, 
									'reason':'连接超时'
									}))


	def get(self):
		'''
			Just For Test
		'''
		userid = 'YourSchoolId'
		schoolid = '1'
		classTime = ''
		classNature = ''
		className = 'YourClassName'
		classShow = 'all'
		result = Connect.getGrade(schoolid, userid, classTime, classNature, className, classShow)
		statu = result['statu']
		self.set_header('Content-Type', 'application/json; charset=UTF-8')
		if statu == '100':
			self.write(json.dumps({'success':True, 'info':result['info']}))
		elif statu == '101':
			self.write(json.dumps({'success':True, 'info':'empty'}))
		elif statu == '103':
			self.write(json.dumps({'success':False, 'reason':'登陆已经失效,请重新登录!'}))
		else:
			self.write(json.dumps({'success':False, 'reason':'连接超时'}))

class RankGradeHandler(tornado.web.RequestHandler):
	def post(self, *args, **kwargs):
		data = tornado.escape.json_decode(self.request.body)
		schoolid = data['schoolId']
		userid = data['userId']
		result = Connect.getRankGrade(schoolid,userid)
		statu = result['statu']
		self.set_header('Content-Type', 'application/json; charset=UTF-8')
		if statu == '100':
			self.write(json.dumps({'success':True, 
									'info':result['info']
									}))
		elif statu == '101':
			self.write(json.dumps({'success':True, 
									'info':'empty'
									}))
		elif statu == '103':
			self.write(json.dumps({'success':False, 
									'reason':'登陆已经失效,请重新登录!'
									}))
		else:
			self.write(json.dumps({'success':False, 
									'reason':'查询失败,连接超时'
									}))

	
	def get(self):
		'''
			Just For Test
		'''
		schoolid = '1'
		userid = 'YourSchoolId'
		result = Connect.getRankGrade(schoolid,userid)
		statu = result['statu']
		self.set_header('Content-Type', 'application/json; charset=UTF-8')
		if statu == '100':
			self.write(json.dumps({'success':True, 
									'info':result['info']
									}))
		elif statu == '101':
			self.write(json.dumps({'success':True, 
									'info':'empty'
									}))
		elif statu == '103':
			self.write(json.dumps({'success':False, 
									'reason':'登陆已经失效,请重新登录!'
									}))
		else:
			self.write(json.dumps({'success':False, 
									'reason':'查询失败,连接超时'
									}))




def main():
	settings = {
		"static_path": os.path.join(os.path.dirname(__file__), "static")
	}
	application = tornado.web.Application([
		(r"/login", LoginHandler),
		(r"/grade",GradeHandler),
		(r"/rankgrade",RankGradeHandler)
		#(r"/getgrade",GetGradeHandler)
	])
	application.add_handlers(r"^yoursite\login$",[(r"/login",LoginHandler)])
	application.add_handlers(r"^yoursite\grade$",[(r"/grade",GradeHandler)])
	application.add_handlers(r"^yoursite\rankgrade$",[(r"/rankgrade",RankGradeHandler)])
	#application.add_handlers(r"^yoursite\getgrade$",[(r"/getgrade",GetGradeHandler)])
	#application.add_handlers(r"^yoursite\getgrade2$",[(r"/getgrade2",RankGradeHandler2)])
	server = httpserver.HTTPServer(application, ssl_options={
		"certfile": os.path.join(os.path.abspath("."), "yoursite.crt"),
		"keyfile": os.path.join(os.path.abspath("."), "yoursite.key"),
	})
	server.listen(443)
	ioloop.IOLoop.instance().start()

def test():
	application = tornado.web.Application([
		(r"/login", LoginHandler),
		(r"/grade",GradeHandler),
		(r"/rankgrade",RankGradeHandler),
		(r"/getgrade",GetGradeHandler),
		(r"/getgrade2",RankGradeHandler2)
	])
	application.add_handlers(r"^localhost\login$",[(r"/login",LoginHandler)])
	application.add_handlers(r"^localhost\grade$",[(r"/grade",GradeHandler)])
	application.add_handlers(r"^localhost\rankgrade$",[(r"/rankgrade",RankGradeHandler)])
	application.add_handlers(r"^localhost\getgrade$",[(r"/getgrade",GetGradeHandler)])
	application.add_handlers(r"^localhost\getgrade2$",[(r"/getgrade2",RankGradeHandler2)])

	server = httpserver.HTTPServer(application)
	server.listen(80)
	ioloop.IOLoop.instance().start()

if __name__ == '__main__':
	main()
	#test()