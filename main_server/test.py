import requests,json
host="http://cs-linux:32134/UCS"
response=requests.post(host,data=json.dumps({"password":"dasd","username":"dsadas","command":"login"})) 

print response.text 

response=requests.post(host,data=json.dumps({"token":"dasd","command":"search_by_name","center":"dsad","placename":"dsads"})) 
print response.text 

response=requests.post(host,data=json.dumps({"token":"dasd","command":"search_bounding_box","xmin":1,"xmax":2,"ymin":3,"ymax":4,"placename":"dsads"})) 
print response.text 

response=requests.post(host,data=json.dumps({"token":"dasd","command":"search_coordinate","longtitude":2,"latitude":3})) 
print response.text





# coding=utf-8
from baidu_map_engine import baidu_map

t=baidu_map()
print "Search by name:"
print 
input = {"placename":"银行","max_long":"40","min_long":"39","max_lat":"117","min_lat":"116"}
print "input: " + str(input)
print "result:"
print t.search_by_name(input)
print 
print "---------------------------------------------"
input1 = {"placename":"银行","max_long":"0","min_long":"0","max_lat":"0","min_lat":"0"}
print "input: " + str(input1)
print "result:"
print t.search_by_name(input1)
print "---------------------------------------------"
print 
input3 = {}
print "input: " + str(input3)
print "result:"
print t.search_by_name(input3)
print "---------------------------------------------"

print ('\n'*5)
print "Search coordinate:"
print
input4 = {"longitude":"120.167930","latitude":"30.277693"}
print "input: " + str(input4)
print "result:"
print t.search_coordinate(input4)  

print "---------------------------------------------"
input5 = {"longitude":"39.983424","latitude":"116.322987"}
print "input: " + str(input5)
print "result:"
print t.search_coordinate(input5)  

print "---------------------------------------------"
input6 = {"longitude":"39.983424"}
print "input: " + str(input6)
print "result:"
print t.search_coordinate(input6)  
print "---------------------------------------------"


print ('\n'*5)
print "Search bounding box"
print
input7 = {"max_long":"121.53300","min_long":"121.53068","max_lat":"29.86300","min_lat":"29.86123"}
print "input: " + str(input7)
print "result:"
print t.search_bounding_box(input7)
print "---------------------------------------------"

print
input8 = {"max_long":"121.53300","max_lat":"29.86300","min_lat":"29.86123"}
print "input: " + str(input8)
print "result:"
print t.search_bounding_box(input8)
print "---------------------------------------------"
print
input9 = {"max_long":"120.53300","min_long":"120.53333","max_lat":"40.00000","min_lat":"40.00000"}
print "input: " + str(input9)
print "result:"
print t.search_bounding_box(input9)
print "---------------------------------------------"


