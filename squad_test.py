from bs4 import BeautifulSoup
import urllib.request as ur
import json

# From AA/wiki_00
entities00 = ["Alien"]
# , "Bug", "Euphoria (disambiguation)", "Frank", "FSB", "GPS (disambiguation)"]
# From AA/wiki_20
entities20 = ["MJ"]
# , "Elmwood Park", "Smith and Jones", "Dietsch"]

# number of titles to request in one query
BLOCKSIZE = 20

def main():

  # read files
  with open ("wiki_00") as w0:
    wiki00 = BeautifulSoup(w0)
  with open ("wiki_20") as w2:
    wiki20 = BeautifulSoup(w2)


  # Construct disambiguiation entity dict
  disambiguations = dict()
  for entity in entities00:
    doc = wiki00.find("doc", {"title": entity})
    disambiguations[entity] = []
    allA = doc.find_all("a")
    numBlocks = len(allA) // BLOCKSIZE + 1
    if len(allA) / BLOCKSIZE == len(allA) // BLOCKSIZE:
      numBlocks -= 1
    #  construct the format such that it can be passed to the API
    for j in range(numBlocks):
      for i in range(BLOCKSIZE):
        ind = j * BLOCKSIZE + i
        if ind == len(allA):
          break
        disambiguations[entity].append("")
        a = allA[ind]
        if i % BLOCKSIZE != 0 and i % BLOCKSIZE != BLOCKSIZE - 1:
          disambiguations[entity][j] += "|"
        disambiguations[entity][j] += a["href"]
      if i == len(allA):
        break

  for entity in entities20:
    doc = wiki20.find("doc", {"title": entity})
    disambiguations[entity] = []
    allA = doc.find_all("a")
    numBlocks = len(allA) // BLOCKSIZE + 1
    if len(allA) / BLOCKSIZE == len(allA) // BLOCKSIZE:
      numBlocks -= 1
    #  construct the format such that it can be passed to the API
    for j in range(numBlocks):
      for i in range(BLOCKSIZE):
        ind = j * BLOCKSIZE + i
        if ind == len(allA):
          break
        disambiguations[entity].append("")
        a = allA[ind]
        if i % BLOCKSIZE != 0 and i % BLOCKSIZE != BLOCKSIZE - 1:
          disambiguations[entity][j] += "|"
        disambiguations[entity][j] += a["href"]
      if i == len(allA):
        break


  print(disambiguations)

  # Make queries to the API
  responses = dict()
  for entity in disambiguations:
    responses[entity] = []
    for query in disambiguations[entity]:
      # Construct request
      request = "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&titles="
      request += query
      request += "&exintro=&exsentences=5&explaintext=&redirects=&format=json"

      response = ur.urlopen(request).read()
      responses[entity].append(response)

  # Parse the responses and construct the context
  contexts = dict()
  for entity, resArr in responses.items():
    context = ""
    for jsonRes in resArr:
      res = json.loads(jsonRes)
      pages = res["query"]["pages"]
      for pageID, page in pages.items():
        extract = page["extract"]
        title = page["title"]
        context += entity + " has title '" + title + "' and pageID " + pageID + ". " + extract + "\n\n"
    contexts[entity] = context








