'''
Brandon Hew


'''

import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import json
import time







def instagram_photos():

	driver = webdriver.PhantomJS()
	
	
	#change access token here
	access_token = ''	

	
	
	
	
	driver.get('https://api.instagram.com/v1/tags/dctech/media/recent?access_token='+access_token)
	#print(driver.page_source)



	#get json
	myjson = re.search("{.+}",driver.page_source)[0]
	parsed_json = json.loads(myjson)
	#print(parsed_json)


	#remove photos before month
	month_seconds = 60*60*24*7*4
	indexes_to_delete=[]
	for j in range(0, len(parsed_json['data'])):
		if float(parsed_json['data'][j]['created_time']) < (time.time() - month_seconds):
			indexes_to_delete.append(j)
		elif parsed_json['data'][j]['type'] != 'image':
			indexes_to_delete.append(j)
	for j in range(0,len(indexes_to_delete)):
		del parsed_json['data'][indexes_to_delete[j]]

		




	#make a tuple of number of comments and link to photo, then sort by number of comments	
	comment_count_and_link=[]
	for j in range(0, len(parsed_json['data'])):
		comment_count_and_link.append((parsed_json['data'][j]['comments']['count'],parsed_json['data'][j]['link']))
		

	sorted(comment_count_and_link,reverse=True)
	print("Instagram answer: \n")
	print(comment_count_and_link)





def flikr_photos():
	driver = webdriver.PhantomJS()
	
	
	api_key = ""		#insert key here
	
	
	driver.get('https://api.flickr.com/services/rest/?method=flickr.photos.search&min_upload_date=2017-04-25%2008:14:07&api_key='+api_key+'&tags=dctech&format=json')
	myjson = re.search("{.+}",driver.page_source)[0]
	parsed_json = json.loads(myjson)
	#print(parsed_json)




	#run through all photo id's and search comments
	photo_ids=[]
	owner=[]
	data=[]
	for j in range(0,len(parsed_json['photos']['photo'])):
		photo_ids.append(parsed_json['photos']['photo'][j]['id'])
		owner.append(parsed_json['photos']['photo'][j]['owner'])
	for j in range(0,len(photo_ids)):
		print(str(100*(j/len(photo_ids)))+"%")
		url='https://api.flickr.com/services/rest/?method=flickr.photos.comments.getList&photo_id='+str(photo_ids[j])+'&api_key='+api_key+'&format=json'
		driver.get(url)
		myjson = re.search("{.+}",driver.page_source)[0]
		parsed_json = json.loads(myjson)
		#comment_count.append(len(parsed_json['comments']))
		data.append((len(parsed_json['comments']),photo_ids[j], owner[j]))
		
		

	print("Flickr answer: \n")
	print(sorted(data,reverse=True))


from threading import Thread
t=Thread(target=instagram_photos)
t.start()
t2=Thread(target=flikr_photos)
t2.start()










