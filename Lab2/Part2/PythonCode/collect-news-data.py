import urllib2
import json
import datetime
import time
import sys, os
from urllib2 import HTTPError
from ConfigParser import SafeConfigParser

# helper function to iterate through dates
def daterange( start_date, end_date ):
    if start_date <= end_date:
        for n in range( ( end_date - start_date ).days + 1 ):
            yield start_date + datetime.timedelta( n )
    else:
        for n in range( ( start_date - end_date ).days + 1 ):
            yield start_date - datetime.timedelta( n )

# helper function to get json into a form I can work with       
def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

# helpful function to figure out what to name individual JSON files        
def getJsonFileName(date, page, json_file_path, query):
    json_file_name = "_".join([query, date, str(page)])
    json_file_name = "".join([json_file_name, ".", 'json'])
    json_file_name = "".join([json_file_path,json_file_name])
    return json_file_name
    
# get the articles from the NYTimes Article API    
def getArticles(start_date, end_date, query, api_key, json_file_path):
    # LOOP THROUGH THE 101 PAGES NYTIMES ALLOWS FOR THAT DATE
    for page in range(101):
        for n in range(5): # 5 tries
            try:
                request_string = "http://api.nytimes.com/svc/search/v2/articlesearch.json?q=" + query + "&begin_date=" + start_date + "&end_date=" + end_date + "&page=" + str(page) + "&api-key=" + api_key
                response = urllib2.urlopen(request_string)
                content = response.read()
                if content:
                    articles = convert(json.loads(content))
                    # if there are articles here
                    if len(articles["response"]["docs"]) >= 1:
                        json_file_name = getJsonFileName(start_date, page, json_file_path, query)
                        json_file = open(json_file_name, 'w')
                        json_file.write(content)
                        json_file.close()
                    # if no more articles, go to next date
                    else:
                        return
                time.sleep(3) # wait so we don't overwhelm the API
            except HTTPError as e:
                print("HTTPError on page %s on %s (err no. %s: %s) Here's the URL of the call: %s", page, start_date, e.code, e.reason, request_string)
                if e.code == 403:
                    print "Script hit a snag and got an HTTPError 403. Check your log file for more info."
                    return
                if e.code == 429:
                    print "Waiting. You've probably reached an API limit."
                    time.sleep(30) # wait 30 seconds and try again
            except: 
                print("Error on %s page %s: %s", start_date, file_number, sys.exc_info()[0])
                continue
        
# Main function where stuff gets done
def main():
    api_key = "67736f1f941b44dc95f63619f6bdc9fb"
    start = datetime.date(year=2018, month=4, day=4)
    end = datetime.date(year=2018,month=4, day=4) 
    query = 'immigration'
    try:
        # LOOP THROUGH THE SPECIFIED DATES
        for date in daterange(start, end):
            start_date = date.strftime("%Y%m%d")
            print start_date            
            date += datetime.timedelta(days=1)
            end_date = date.strftime("%Y%m%d")
            print end_date
            json_file_path = "NewsData/"
            try:
                if not os.path.exists(os.path.dirname(json_file_path)):
                    os.makedirs(os.path.dirname(json_file_path))
            except OSError as err:
                print(err)
            getArticles(start_date, end_date, query, api_key, json_file_path)
    except:
        print("Unexpected error: %s", str(sys.exc_info()[0]))
    finally:
        print("Finished.")

if __name__ == '__main__' :
    main()
