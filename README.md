#Differently Spider frame ———— ***SpiderBone***
====================================================================================================
#author by ———— *HiredMagician*
---------------------------------------------------------------------------------------------------
#### _need module: BeautifulSoup, requests_
### usually the web spider look like this:
```
import requests
import time
import os
from bs4 import BeautifulSoup

class EggsClimber:

	self.c = 0
	headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36','connection':'keep-alive'}
	timeout = 10
	base_url = "https://77nali.com/dongtaitu/"
	base_path = r"E:\test" #the path where you want save

	def try_untill_get(self,url,what):
		while 1:
			try:
				if what == 'html':
						the_get = requests.get(url,headers=self.headers,timeout=self.timeout).text
				else:
						the_get = requests.get(url,headers=self.headers,timeout=self.timeout).content
				break
			except:
				time.sleep( 3 )	
		return the_get

	def get_num(self,list):
		num = 0
		for item in list:
			num = num + 1
		return num

	def get_img(self,soup):
		img_list = soup.find('article').find_all('img')
		for img in img_list:
			content = self.try_untill_get(img['src'],'gif')
			name = str(self.c)
			path = self.base_path + "\\" + name
			with open(path,'wb+') as f:
				f.write(content)
			self.c = self.c + 1
			print('gif:%s done' % name)

	def get_reset_all(self,link,all_num):
		num = 2
		while num < all_num:
			html = self.try_untill_get(link + '/' + str(num),'html')
			num = num + 1
			soup = BeautifulSoup(html,"html.parser")
			self.get_img(soup)
			time.sleep( 1 )

	def GoGet(self):
		choose = input("Witch url you want me to climb?[1:https://77nali.com/dongtaitu/ ; 2:https://77nali.com/gifchuchu]")
		if choose == '2':
			self.base_url = 'https://77nali.com/gifchuchu'
		else :
		if not os.path.exists(self.base_path):
			os.makedirs(self.base_path)
		article = 1
		article = input("How many article you want?:" )
		current_article = int(article)
		if current_article <= 0:
		current_page = int(current_article / 20) + 1
		else_path = ''
		while current_page > 0:
			url = self.base_url + else_path
			html = self.try_untill_get(url,'html')		
			soup = BeautifulSoup(html,"html.parser")
			article_list = soup.find_all('article', class_='excerpt')
			for article in article_list:
				link = article.find('a')['href']
				soup = BeautifulSoup(html,"html.parser")
				try:
					a_list = soup.find('div',class_ = 'article-paging').find_all('a')
					all_num = self.get_num(a_list)
					self.get_img(soup)
					time.sleep( 1 )
					self.get_reset_all(link,all_num)					
				except:
					continue
				current_article = current_article - 1
				if current_article == 0:
					return 0
			current_page = current_page - 1

if __name__=='__main__':
	EggsClimber().GoGet()
```
### _but_ when it use the _SpiderBone_ it look like this:
```
from SpiderBone import GoClimb
class exp:
	def __init__(self):
		self.c = 0
		url = 'https://77nali.com/dongtaitu'
		ways = (
			{
				'one':
				(
					'climb_up',
					{'tag':'div','attr':'class','value':'content'},
					{'tag':'article','many':'true'},
					{'tag':'a'},
					{'get':'attr','name':'href'}
				)
			},
			{
				'one~one':
				(
					'grab_down',
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
		GoClimb(url = url,ways = ways,my_self = self).let_it_go()
		
	def save_data(self,content):
		self.c = self.c + 1
		path = r"E:\test" + '\\' + str(self.c) + '.jpg'
		with open(path,'wb+') as f:
			f.write(content)
		print('gif:%s done' % name)
				
if __name__ == '__main__':
	exp()
```
***
if I tell you two code they do same thing 
<br></br>
you may say: what happen? where is code? or even what a hell?
<br></br>
give me a breath,let me explain^_^
***
One —— Situation
>Let's think about how we usually create the web spider:
>>step 1: we need location the target we want grab.
<br></br>
>>step 2: we need find the way for spider reach the target.
<br></br>
>>which is quite easy that we can just use our browser's Inspect Element,when we see the unique tag then we find the way.
<br></br>
>>step 3: we need programming.
<br></br>
>>of cause we need to step by step tell the spider how to move his leg for get what we want they grab,this part is kernel part so is most spend time!!!
***
Two —— Question
>Now as we see all this spider create process,we find out that step 3 is most cost time,and look like every time we programming the web spider is do the same thing——along the way we find and grab the thing we want.
>so qusetion is:
>>can we do step 3 automatic?
***
Three —— Solution
>according to the climb way you set SpiderBone can automatically create the code to find the way to climb up or grab down by use `eval()`
<br></br>
>2:
>which mean we nearly only need step 1,2 and finish,no more code,no more time to waste,only left the beautiful code and things we want
***
you need understand few thing befor you get start:
>1: the url you give must be completely whit _http://_ or _https://_
<br></br>
>2: the structure of the ways you set:
<br></br>
>each step is corresponding one html page,for example is your url set "https://www.google.com/", then step one is work on that root html page, step two is work on every page that is you Follow-up at inner root page's url, step three is same principle. all tree structure is start at one root
![three](https://github.com/HiredMagician/SpiderBone/raw/master/three.png)
<br></br>
>3: write the each way dict:
<br></br>
>the normaly ways structure is at below;
<br></br>
for each way,at first,you need chose the way name and set action('climb_up' or 'grab_down'),then you need set the way dict(the path to do action),from top to bottom one tag by one tag to close you target(url for next step or things you want grab)
<br></br>
need pay attention to is the: if you want climb each same child tag of his father tag,what you only need is add the `'many':'true'` in that child tag's dict,if you not add,the SpiderBone will automatically get all last tag which in dict you set 
<br></br>
>now you can release you own web spider by use: `GoClimb(url = url,ways = ways,my_self = self).let_it_go()`
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
### And for more information please read the [manual](https://github.com/HiredMagician/SpiderBone/blob/master/manual.md)
## __have good time^_^__
