import requests, bs4
import json
import math
import time
from urllib.parse import urlparse
import urllib
import pathlib
import datetime

urlData = [
    {
        'name': 'gaming',
        'url': 'https://api.takealot.com/rest/v-1-6-0/productlines/search?sort=Price%20Descending&rows=50&start=0&detail=mlisting&backend=fbye-snprg-pyvrag&filter=Type:2&filter=Available:true&callback=type',
        'enabled': True
    },
    {
        'name': 'boardgames',
        'url': 'https://api.takealot.com/rest/v-1-6-0/productlines/search?sort=BestSelling%20Descending&rows=50&start=0&detail=mlisting&backend=arj-fbye-zz-fla-fcenax&filter=Type:7&filter=Category:19910&filter=Available:true',
        'enabled': True
    },
    {
        'name': 'computer_components',
        'url': 'https://api.takealot.com/rest/v-1-6-0/productlines/search?sort=BestSelling%20Descending&rows=50&start=0&detail=mlisting&backend=arj-fbye-zz-fla-fcenax&filter=Type:13&filter=Category:10066&filter=Available:true',
        'enabled': True
    },
    {
        'name': 'computer_accessories',
        'url': 'https://api.takealot.com/rest/v-1-6-0/productlines/search?sort=BestSelling%20Descending&rows=10&start=0&detail=mlisting&backend=arj-fbye-zz-fla-fcenax&filter=Type:13&filter=Category:9899&filter=Available:true',
        'enabled': True
    },
    {
        'name': 'television',
        'url': 'https://api.takealot.com/rest/v-1-6-0/productlines/search?sort=BestSelling%20Descending&rows=50&start=0&detail=mlisting&backend=arj-fbye-zz-fla-fcenax&filter=Type:15&filter=Category:9834&filter=Available:true',
        'enabled': True
    },
    {
        'name': 'cellphones',
        'url': 'https://api.takealot.com/rest/v-1-6-0/productlines/search?sort=BestSelling%20Descending&rows=10&start=0&detail=mlisting&backend=arj-fbye-zz-fla-fcenax&filter=Type:16&filter=Category:6479&filter=Available:true',
        'enabled': True
    },
    {
        'name': 'cellphone_accessories',
        'url': 'https://api.takealot.com/rest/v-1-6-0/productlines/search?sort=BestSelling%20Descending&rows=10&start=0&detail=mlisting&backend=arj-fbye-zz-fla-fcenax&filter=Type:16&filter=Category:6520&filter=Available:true',
        'enabled': True
    },
    {
        'name': 'kitchen_appliances',
        'url': 'https://api.takealot.com/rest/v-1-6-0/productlines/search?sort=BestSelling%20Descending&rows=10&start=0&detail=mlisting&backend=arj-fbye-zz-fla-fcenax&filter=Type:12&filter=Category:10816&filter=Available:true',
        'enabled': True
    },
    {
        'name': 'liquor',
        'url': 'https://api.takealot.com/rest/v-1-6-0/productlines/search?sort=BestSelling%20Descending&rows=10&start=0&detail=mlisting&backend=arj-fbye-zz-fla-fcenax&filter=Type:12&filter=Category:19271&filter=Available:true',
        'enabled': True
    },
    {
        'name': 'beer',
        'url': 'https://api.takealot.com/rest/v-1-6-0/productlines/search?sort=BestSelling%20Descending&rows=10&start=0&detail=mlisting&backend=arj-fbye-zz-fla-fcenax&filter=Type:12&filter=Category:19272&filter=Available:true',
        'enabled': True
    },
    {
        'name': 'DIY',
        'url': 'https://api.takealot.com/rest/v-1-6-0/productlines/search?sort=BestSelling%20Descending&rows=10&start=0&detail=mlisting&backend=arj-fbye-zz-fla-fcenax&filter=Type:23&filter=Category:11277&filter=Available:true',
        'enabled': True
    }
]
outputPath = "/home/rsimpson/Documents/takealot/"

def makeRequest(url, page):
    errorCount = 0
    maxErrorCount = 10
    while (errorCount < maxErrorCount):
        try:
            res = requests.get(url)
            res.raise_for_status()
            jsonObj = 0
            try:
                jsonObj = json.loads(res.text)
            except json.decoder.JSONDecodeError:
                jsonObj = json.loads(res.text[9:-2])
            return jsonObj
        except Exception as err:
            print("Download Error. Retrying page ", page)
            print(err)
            errorCount += 1
            time.sleep(5)
    return False

def getJSONData(url, page):
    urlParams = urlparse(url)
    queryParams = urllib.parse.parse_qs(urlParams.query)
    newStart = page * int(queryParams["rows"][0])
    queryParams["start"][0] = str(newStart)
    queryParams["rows"][0] = str(50);
    queryString = urllib.parse.urlencode(queryParams, doseq=True)
    urlParams = urlParams._replace(query=queryString)
    finalURL = urllib.parse.urlunparse(urlParams)
    print(finalURL)
    jsonObj = makeRequest(finalURL, page)
    return jsonObj

def writeJSonToFile(jsonObj, path, outputFile):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    with open(path + str(outputFile) + ".json", 'w') as outFile:
        json.dump(jsonObj, outFile, indent=4, sort_keys=True, separators=(',', ': '))

def processSite(name, url):
    currentPage = 0
    jsonObj = getJSONData(url, currentPage)
    totalRecords = int(jsonObj["results"]["num_found"])
    recordsPerRow = int(jsonObj["params"]["rows"][0])
    pageCount = math.ceil(totalRecords/recordsPerRow)
    outputFolder = outputPath + datetime.datetime.now().strftime("%Y-%m-%d") + "/" + name + "/"
    writeJSonToFile(jsonObj, outputFolder, currentPage)
    currentPage += 1

    while currentPage <= pageCount:
        print("Page", currentPage, "of", pageCount)
        jsonObj = getJSONData(url, currentPage)
        if (jsonObj == False):
            print("Failed to download page", currentPage)
        else:
            print(jsonObj)
            writeJSonToFile(jsonObj, outputFolder, currentPage)
        currentPage += 1
        # time.sleep(1)


for site in urlData:
    if (site["enabled"] == True):
        print("Processing", site["name"])
        processSite(site["name"], site["url"])
