import requests
import time
from bs4 import BeautifulSoup
import re

class GoClimb:

	def __init__(self,url = None,ways = None,my_self = None,headers = {},time = 0):
		if not ways or not url or not my_self:
			raise Exception("The ways,url and self of you class is only thing you need set and must be set!")
		if not url[len(url) - 1] == '/':
			url = url + '/'
		self.url = url
		self.ways = way
		self.my_self = my_self
		self.all_step = len(self.ways)
		self.creat_need_list()
		if not headers:
			headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36','connection':'keep-alive'}
		self.headers = headers
		self.time = time
		self.timeout = 10
		self.c = 0
	
	#release the spider,and when finish callback^_^
	def let_it_go(self):
		self.climb_up(self.url,1,'main')
		try:
			self.my_self.finish()
		except:
			pass
	
	#get html page,grab down the content that you want from this page,create the path,and along them climb up.
	def climb_up(self,url,step,way_name):
		html = self.try_untill_get(url,'html')
		soup = BeautifulSoup(html,"html.parser")
		if step <= self.all_step:
			self.grab_down(soup,step,way_name,url)
			finder_list = self.create_finder('climb_up',step,way_name)
			if finder_list:
				for way_name in finder_list:
					finder = finder_list[way_name]
					get_list = eval(finder)
					if not get_list:
						raise Exception('the find path you set is not correct,check the way name is:%s' % way_name)					
					geter = self.create_geter(step,way_name)
					if way_name in self.pass_list:
						get_list = self.pass_clear(get_list,self.pass_list[way_name])
					if way_name in self.guess_list:
						get_list = self.guess_add(get_list,geter,soup)				
					for get in get_list:
						urls = eval(geter)
						if not urls:
							raise Exception('the grab path you set is not correct,check the way name is:%s' % way_name)
						urls = self.pack(urls,url)
						for url in urls:
							self.climb_up(url,step + 1,way_name)
	
	#create the path,and grab down the contents you want.
	def grab_down(self,soup,step,way_name,url):
		finder_list = self.create_finder('grab_down',step,way_name)
		if finder_list:
			for way_name in finder_list:
				finder = finder_list[way_name]
				get_list = eval(finder)
				if not get_list:
					raise Exception('the find path you set is not correct,check the way name is:%s' % way_name)
				geter = self.create_geter(step,way_name)
				for get in get_list:
					need_gets = eval(geter)
					if not need_gets:
						raise Exception('the grab path you set is not correct,check the way name is:%s' % way_name)
					need_gets = self.pack(need_gets,url)
					for need_get in need_gets:
						content = self.get_content(need_get,way_name)
						self.save_data(content)
		
	def try_untill_get(self,url,what):
		while 1:
			try:
				if what == 'html':
						the_get = requests.get(url,headers=self.headers,timeout=self.timeout).text
				else:
						the_get = requests.get(url,headers=self.headers,timeout=self.timeout).content
				time.sleep( self.time )
				break
			except:
				time.sleep( 3 )	
		return the_get
	
	#according to way that you set,create the code that can find the item list that include the url to climb or contents to grab
	def create_finder(self,which,step,way_name):
		index = step - 1
		finder_list = {}
		code = "soup"
		fun = '.find'
		branch = self.ways[index]		
		for key in branch:
			if way_name == 'main' or way_name == '~'.join(key.split('~')[:step]):
				branch_child = branch[key]
				if branch_child[0] == which:
					branch_child_len = len(branch_child)
					for i in range(1,branch_child_len - 1):
						d = branch_child[i]
						if 'tag' in d:
							if 'many' in d or i + 1 == branch_child_len - 1:
								fun = '.find_all'
							code = self.write_find_code(fun,d,code)
						else :
							raise Exception('must need "tag" in way you set! check the way name:%s index:%d' % (key,i))
						if fun == '.find_all':
							break
					finder_list[key] = code	
		
		return finder_list						
	
	#according to way that you set,create the code that can find the url to climb or contents to grab from the item list
	def create_geter(self,step,way_name):
		index = step - 1
		finder_list = {}
		code = "get"
		fun = '.find'
		branch = self.ways[index]		
		branch_child = branch[way_name]
		begin_index = self.get_index(branch_child)
		branch_child_len = len(branch_child)
		for i in range(begin_index,branch_child_len):	
			d = branch_child[i]
			if 'tag' in d:
				code = self.write_find_code(fun,d,code)
			elif 'get' in d:
				code = self.write_get_code(d,code,way_name)
			else:
				raise Exception('must need "tag" or "get" in way you set! check the way name:%s index:%d' % (way_name,i))
		return code
		
	def get_index(self,branch_child):
		branch_child_len = len(branch_child)
		begin_index = branch_child_len - 1
		for i in range(1,branch_child_len - 1):
			d = branch_child[i]
			if 'many' in d or 're' in d:
				begin_index = i + 1
				break
		return begin_index
			
	def write_find_code(self,fun,d,code):
		code = code + fun + '("' + d['tag'] + '"'
		if 'attr' in d and 'value' in d:
			code = code + ',attrs={'
			attr_list = d['attr'].split('~')
			value_list = d['value'].split('~')
			for (attr,value) in zip(attr_list,value_list):
				code = code + '"' + attr + '":"' + value + '",'
			code = code[:-1] + '}'
		code = code + ')'
		return code
		
	def write_get_code(self,d,code,way_name):
		if d['get'] == 'attr':
			code = code + '["' + d['name'] + '"]'
		elif d['get'] == 'string':
			code = code + '.string'
		elif d['get'] == 'html':
			code = 'str(' + code + ')'
		else:
			raise Exception('"get" only can set value "attr","string" or "html",check the way name:%s' % way_name)
		if 're' in d:
			code = self.write_re_code(d,code)
		return code
		
	def write_re_code(self,d,code):
		code = 're.findall("' + d['re'] + '",' + code + ')'
			
	def pack(self,need_gets,url):
		gets = []
		if type(need_gets) == str:
			gets.append(need_gets)
		else:
			gets = need_gets
		return self.complet_url(gets,url)
		 
		
	def creat_need_list(self):
		self.type_list = {}
		self.guess_list = {}
		self.pass_list = {}
		for i in range(0,self.all_step):
			branch = self.ways[i]
			for key in branch:
				branch_child = branch[key]
				d = branch_child[len(branch_child) - 1]
				if branch_child[0] == 'grab_down':					
					if 'type' in d:
						self.type_list[key] = d['type']
					else :
						raise Exception('if the way action is grab_down,then "type" must set in last dict!check the way name: %s' % key)
				else:
					if 'guess' in d:
						self.guess_list[key] = d['guess']
					if 'pass' in d:
						self.pass_list[key] = d['pass']
					
	def get_content(self,need_get,way_name):
		the_type = self.type_list[way_name]
		if not the_type == 'nogoin':
			the_get = self.try_untill_get(need_get,the_type)
		else:
			the_get = need_get
		return the_get
		
	def save_data(self,content):
		self.my_self.save_data(content)
				
	def guess_add(self,get_list,geter,soup):
		new_get_list = []
		urls = []
		get = get_list[0]
		urls.append(eval(geter))
		get = get_list[len(get_list)-1]
		urls.append(eval(geter))
		tmp_begin = re.findall('[0-9]+',urls[0])
		tmp_begin = int(tmp_begin[len(tmp_begin)-1])		
		tmp_last = re.findall('[0-9]+',urls[1])
		tmp_last = int(tmp_last[len(tmp_last)-1])
		url_left = str(tmp_begin).join(urls[0].split(str(tmp_begin))[:-1])
		url_right = str(tmp_begin).join(urls[0].split(str(tmp_begin))[-1:])
		for num in range(tmp_begin,tmp_last + 1):
			a_tag = soup.new_tag('a',href=url_left + str(num) + url_right)
			new_get_list.append(a_tag)
		return new_get_list
			
	def pass_clear(self,get_list,the_pass):
		left_num = int(the_pass.split(':')[0])
		right_num = int(the_pass.split(':')[1])	
		return get_list[left_num:right_num]
		
	def complet_url(self,gets,url):
		new_gets = []
		for path in gets:
			if not path.find('http://') == 0 and not path.find('https://') == 0:
				if path[0] == '.':
					if path[1] == '/':
						path = path[1:]
						url = '/'.join(url.split('/')[:-1]) + path
					elif path[1] == '.':
						path = path[2:]
						url = '/'.join(url.split('/')[:-2]) + path
				elif path[0] == '/':
					url = '/'.join(url.split('/')[:3]) + path
				else:
					url = '/'.join(url.split('/')[:-1]) + '/' + path
			else :
				url = path
			new_gets.append(url)
		return new_gets
		