from annotation import *

import json
from annotation import *

GRAPH_THRESHOLD = 10
SORT_CRITERIA = "degree" # or "pagerank"

def sortGraphNodes(nodes, sortCriteria):
    try:
        return sorted(nodes, key=lambda n: float(n.get("attributes").get(sortCriteria)), reverse=True)
    except:
        return []

def graphBuilder(annotations, sortCriteria, depth = 2, resourceLimit = 100): # annotations can be result of Spotlight/Babelfy
    """Returns a description of a graph (nodes, edges)"""
    results = jsonRequestServer(SERVER_ADDRESS + ":8081/graph", {
        "mynivelProfundidad": depth,        # Optional -> Default 1 Max 2
        "limitRecur": resourceLimit,        # Max number of resources take into account in the graph builder
        "annotations": json.dumps(annotations)
    }) or {}

    nodes = results.get("nodes") or []

    return sortGraphNodes(nodes, sortCriteria)

def extractInfoFromGraphNode(node):
    #print(node)
    return {
        "label": node.get("label"),
        "degree": node.get("attributes").get("degree"),
        "pagerank": node.get("attributes").get("pagerank")
    }

def combineResults(*annotatorResults):
    allResults = {}

    for result in annotatorResults:
        for (concept, frequency) in result:
            if concept not in allResults:
                allResults[concept] = 0
            allResults[concept] += frequency

    return allResults

def graph(*annotatorResults):
    initialConcepts = sorted(list(combineResults(*annotatorResults).items()), key=lambda t: int(t[1]), reverse=True)[:GRAPH_THRESHOLD]
    #print("---initialConcepts---")
    #print(initialConcepts)
    if len(initialConcepts) > 0:
        graphBuilderResults = graphBuilder(initialConcepts, SORT_CRITERIA)
        #print("---graphBuilderResults---")
        #print(graphBuilderResults)
        #print(len(graphBuilderResults))

        graphResults = [extractInfoFromGraphNode(node) for node in graphBuilderResults]
        #print("---graphResults---")
        #print(graphResults)



        return sorted(graphResults, key=lambda g: g[SORT_CRITERIA], reverse=True)
    return {}

def avgDegree(nodeResultList):
    sum = 0
    for n in nodeResultList:
        degree = n.get("degree")
        #print(degree)
        sum = sum + degree
    avg = round(sum/len(nodeResultList),2)
    #print("Sum: "+str(sum))
    #print("Avg :" + str(avg))
    return avg

def filteredResults(nodeResultList,average):
    results_filtered = []
    for n in nodeResultList:
        if n.get("degree") >= average:
            results_filtered.append(n)
    return results_filtered

