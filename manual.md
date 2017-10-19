*****SpiderBone***** ———— `manual`
=================================================
no need the `code` only need set the `ways`
---------------------------------------------
#### _ways structure like below_
```
ways = (
	#step one 
	{
		#below is way name:(way tuple)
		'one':
		(
			'climb_up',	#get url for step two
			{'tag':'div','attr':'class','value':'content'},	
			{'tag':'article','many':'true'},
			{'tag':'a'},
			{'get':'attr','name':'href'}
		)
	},
	#step two
	{	
		'one~one':#one way follow above one way
		(
			'grab_down',	#grab content from the page we get
			{'tag':'article','attr':'class','value':'article-content'},	
			{'tag':'img'},
			{'get':'attr','name':'src','type':'img'}
		),
		'one~two':
		(
			'climb_up',
			{'tag':'div','attr':'class','value':'article-paging'},
			{'tag':'a'},
			{'get':'attr','name':'href'}
		)
	},
	#step three
	{
		'one~two~one':
		(
			'grab_down',
			{'tag':'article','attr':'class','value':'article-content'},
			{'tag':'img'},
			{'get':'attr','name':'src','type':'img'}
		)
	}
)
```
the way's name use `'~'` to connect,child way's nmae need include his father way's name! in each way, first element is the action `'grab_down'` or `'climb_up'`;
***
then you can use key `'tag'`,`'attr'`,`'value'`,`'many'` in middle dict,only thing must need is `tag`:
>need pay attention to is the: if you want climb each same child tag of his father tag,what you only need is add the `'many':'true'` in that child tag's dict,if you not add,the SpiderBone will automatically get all last tag which in dict you set
<br></br>
and they also can set multiple attr use '~': `{'tag':'div','attr':'id~class','value':'dark~light'}`,and class must be the full value;
***
in the end dict of the each way,you can use key `'get'`,`'name'`,`'re'`,`'type'`,`'pass'`,`'guess'`:
>the key `'get'`: _it must be set!_ you can use value `'attr'`,`'string'`,`'html'` to get the attr,text inner last tag,or just html tag.
<br></br>
the key `'name'`: if you set `'attr'` in key 'get',then must tell is attr's name.
<br></br>
the key `'type'`: if way's action is `'grab_down'` _then it must be set!_ you need tell which type is the things you grab right? only use `'nogoin'`,`'html'`,`'data'`,`'nogoin'`mean the things you grab at that page is not a url,so spider will not request it,for example,if you just want the string at the <title></title> you need:
```
{'tag':'title'}
{'get':'string','type':'nogoin'}
```
the key `'re'`:if you want deal with you tag,you can use regex,like
```
{'get':'string','re':'http://.+?\.py','type':'data'}
```
when spider get the string and it will use regex deal with that.
<br></br>
the key `'pass'`: use this like python list section  _tmp_list[1:-1]_ can pass the many same tag that you don't want, for exapmle, below way get the all child a tag of the unique div tag,and pass the first a tag and last a tag:
```
#the 'a~2' way
'a~2':
(
  'climb_up',
  {'tag':'div','attr':'id','value':'pages'},
  {'tag':'a'},
  {'get':'attr','name':'href','pass':'1:-1','guess':'true'}
)
```
the key `'guess'`: some time we may meet situation like page 1,2,3,4,5,6,7...19,20,there not have 8-18 in that page! so that if you only along the link in page will miss some thing!,use `'guess':'true'`,can automatically completion the miss url,and the SpiderBone deal pass first before deal guess
<br></br>
##### that's all about `ways`
***
#### below is the work well example:(and I create it only cost 2 min,oh my^_^)
```
from SpiderBone import GoClimb

class exp:
	def __init__(self):
		self.c = 0
		url = 'http://www.gifbin.com/thumbs/'
		ways = (
			{
				'a':
				(
					'climb_up',
					{'tag':'li','attr':'class','value':'tooltips','many':'true'},
					{'tag':'a'},
					{'get':'attr','name':'href'}
				)
			},
			{
				'a~1':
				(
					'grab_down',
					{'tag':'div','attr':'class','value':'content'},
					{'tag':'img'},
					{'get':'attr','name':'src','type':'data'}
				)				
			}
		)
		GoClimb(url = url,ways = ways,my_self = self).let_it_go()
		
	def save_data(self,content):
		name = str(self.c) + '.jpg'
		self.c = self.c + 1
		path = r"E:\WebSite\test" + '\\' + name
		with open(path,'wb+') as f:
			f.write(content)
		print('jpg:%s done' % name)
		
if __name__ == '__main__':
	exp()
```
##### there is only one function in SpiderBone you need to know `GoClimb(url = url,ways = ways,my_self = self).let_it_go()`,the define of GoClibm is 
```
def __init__(self,url = None,ways = None,my_self = None,headers = {},time = 0):
```
my_self is the self of you class;
<br></br>
headers is the http headers;
<br></br>
time is each time when you finish one request,the time for sleep.
<br></br>
##### function save_data: 
```
def save_data(self,content):
```
this function is by user define but SpiderBone used,every time when spider grab any content, the function will be be call, so of cause it can be use to save the data.
##### function finish:
```
def finish(self):
```
let we see the only useful function you called at SpiderBone:
```
	def let_it_go(self):
		print('let_it_go')
		self.climb_up(self.url,1,'main')
		try:
			self.my_self.finish()
		except:
			pass
```
so that's clearly right,when the SpiderBone finish, it will be call,but you can ignore it!
