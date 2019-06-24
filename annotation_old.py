import requests, textwrap, time
from langdetect import detect
import urllib.request
from collections import Counter


SERVER_ADDRESS = "http://172.24.99.127"
reqheaders = {'accept': 'application/json'}

BASE_URL = "https://api.dbpedia-spotlight.org/"

service_url = 'https://babelfy.io/v1/disambiguate'
KEY = "ad4bb18a-b189-4b7c-9635-1633bd1ee1af"

PROXIES = {
    "http": "http://connect.virtual.uniandes.edu.co:22",
    "https": "http://connect.virtual.uniandes.edu.co:22"
}

text_EN = "Bach Bach was a composer of baroque music."
text_DE = "Erstmals 1237 urkundlich erwähnt, war Berlin im Verlauf der Geschichte und in verschiedenen Staatsformen Hauptstadt Brandenburgs, Preußens und des Deutschen Reichs."

def jsonRequest(url,data):

    response, results= None, None


    try:
        response = requests.get(url, params= data,headers=reqheaders)
        print("response:"+str(response))
        #print(response.url)
    except requests.exceptions.RequestException as e:
        print("Request exception: {}".format(e))
    except ValueError:
        print("Invalid JSON response")
    except urllib.request.HTTPError as e:
        if e.code == 502:
            print("error "+str(e.code))
            while(response == None):
                time.sleep(5)
                response = requests.get(url, params=data, headers=reqheaders)

    return response.json()

def jsonRequestServer(url, data, verbose = False):
    response, results = None, None
    #print(data)
    try:
        response = requests.post(url, params=data, proxies=PROXIES)
        #response = requests.get(url, params=data, headers=reqheaders)
        if verbose:
            print("Request to {} took {}".format(url, response.elapsed))

        response.raise_for_status()
        results = response.json()
    except requests.exceptions.RequestException as e:
        print("Request exception: {}".format(e))
       # print(response.text)
    except ValueError:
        print("Invalid JSON response")
    #print(results)
    return results

def detectLanguage(text):
    detectedLanguage = detect(text).upper()
    acceptedLanguages = ['EN', 'FR', 'ES', 'DE']
    language = detectedLanguage if detectedLanguage in acceptedLanguages else acceptedLanguages[0]
    return language.lower()

def frequencyService(url, data, chunkSize = 6000):
    chunks = textwrap.wrap(data["text"], width=chunkSize, break_long_words=False, break_on_hyphens=False)
    #print("chunks: "+str(chunks))

    results = {}
    resultsAugmented = []

    for chunk in chunks:
        data.update({"text": chunk})
        #print(data)
        r = jsonRequest(url, data) or []
        print(r)
        #res = jsonRequest(url, data) or []
        #r= tupleList(res)
        #print("---")
       # print(r)

        r = tupleList(r)
        #print(r)

        for (concept, frequency, word) in r:
            #print(concept,word)
            if concept not in results:
                results[concept] = 0
            results[concept] += frequency

        for (concept, frequency, word) in r:
            resultsAugmented.append((concept, frequency, word))


    return results.items(), resultsAugmented

def frequencyServiceBabelfy(url, data, chunkSize = 6000):
    chunks = textwrap.wrap(data["text"], width=chunkSize, break_long_words=False, break_on_hyphens=False)
    #print("chunks: "+str(chunks))

    results = {}
    resultsAugmented = []

    for chunk in chunks:
        data.update({"text": chunk})
        #print(data)
        r = jsonRequest(url, data) or []

        #res = jsonRequest(url, data) or []
        #r= tupleList(res)
        #print("---")
        #print(r)

        r = tripleList(r,chunk)
        #print(r)

        for (concept, frequency, word) in r:
            #print(concept,word)
            if concept not in results:
                results[concept] = 0
            results[concept] += frequency

        for (concept, frequency, word) in r:
            resultsAugmented.append((concept, frequency, word))


    return results.items(), resultsAugmented

def tripleList(jsonResult,text):
    tripleList = []
    c = Counter(j['DBpediaURL'] for j in jsonResult if j['DBpediaURL'] !='')
    #print(c)
    #print(text)
    if jsonResult:
        for j in jsonResult:
            unique = True

            if j['DBpediaURL'] !='':
                char = j['charFragment']
                start = char['start']
                end = char['end']
                #print(start,end)
                word = text[start:end+1]
                #print(word)
                for t in tripleList:
                    # print("t: "+str(t))
                    if j['DBpediaURL'] == t[0]:

                        unique = False
                        if word.lower() not in t[2]:
                            t[2].append(word.lower())
                        break
                if unique:
                    triple = [j['DBpediaURL'], c[j['DBpediaURL']], [word.lower()]]
                    tripleList.append(triple)
    return tripleList


def tupleList(jsonResult):
    tuple_list = []


    c = Counter(j['@URI'] for j in jsonResult['Resources'])
    #print(c)
    if jsonResult['Resources']:

        for j in jsonResult['Resources']:
            unique = True
            #print("j:" + str(j))
            for t in tuple_list:
                #print("t: "+str(t))
                if j['@URI'] == t[0]:

                    unique = False
                    if j['@surfaceForm'].lower() not in t[2]:
                        t[2].append(j['@surfaceForm'].lower())
                    break
            if unique:
                tuple = [j['@URI'],c[j['@URI']],[j['@surfaceForm'].lower()]]
                tuple_list.append(tuple)

    return tuple_list


def spotlight(text, canonical = True, sort = True):
    def get_slope_intercept(x1, x2, y1, y2):
        slope = (y2 - y1) / (x2 - x1)
        intercept = y1 - slope * x1
        return slope, intercept

    def interpolate(xRange, yRange, x):
        slope, intercept = get_slope_intercept(*xRange, *yRange)
        y = slope * x + intercept
        return y

    def calculate_confidence_support(l):
        if l in range(500):
            # confidence: 0.1 - 0.25, support: 5 - 10
            confidence = interpolate((0, 500), (.1,.25), l)
            support = interpolate((0, 500), (5, 10), l)
        elif l in range(500,1000):
            # confidence: 0.2 - 0.35, support: 5 - 10
            confidence = interpolate((500, 1000), (.2, .35), l)
            support = interpolate((500, 1000), (5, 10), l)
        else: # >= 1000:
            # confidence: 0.3 - 0.4, support: 10 - 20
            confidence = .4
            support = 20

        return confidence, support

    confidence, support = calculate_confidence_support(len(text))
    #print(confidence,support)

    results, resultsAugmented = frequencyService(BASE_URL+detectLanguage(text)+'/annotate',{
        "support": round(support),
        "confidence": confidence,
        "canoncial": int(canonical),
        "text": text
    })
    #print("results: "+str(results))


    if sort:
        resultsAugmented = sorted(resultsAugmented, key=lambda t: (-t[1],t[0]))
        results = sorted(results, key=lambda t: int(t[1]), reverse=True)

    #print("results: "+str(results))

    return results, resultsAugmented


def babelfy(text, sort = True):

    """Returns an array of tuples (concept, frequency)"""
    results, resultsAugmented = frequencyServiceBabelfy(service_url, {
        "lang": detectLanguage(text),   # Required: EN-ES-FR
        "text": text,
        "key": KEY
    })

    if sort:
        resultsAugmented = sorted(resultsAugmented, key=lambda t: (-t[1],t[0]))
        results = sorted(results, key=lambda t: int(t[1]), reverse=True)

    return results, resultsAugmented


def augmentedResults(nodeResultList, augmentedListSpotlight, augmentedListBabelfy):
    link = "http://dbpedia.org/resource/"
    for n in nodeResultList:
        n['word'] = []
        labelValue = n['label']
        #print("labelvalue: "+str(labelValue))
        for a in augmentedListSpotlight:
            ending = a[0].rsplit('/', 1)[1]
            resource = "dbr:"+ending
            #print(resource)
            if labelValue == resource:

                for word in a[2]:
                    if word not in n['word']:
                        n['word'].append(word)
        for b in augmentedListBabelfy:
            ending = b[0].rsplit('/', 1)[1]
            resource = "dbr:" + ending
            #print(resource)
            if labelValue == resource:

                for word in b[2]:
                    if word not in n['word']:
                        n['word'].append(word)
        n['label'] = link+labelValue.rsplit(':',1)[1]
    return nodeResultList
"""

data= {"text":text_EN,
       "support":20,
       "confidence":0.4}
language = detectLanguage(text_EN)

result = jsonRequest(BASE_URL+language+'/annotate',data)
list = tupleList(result)
for l in list: print(l)
"""