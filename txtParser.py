import sys
import xml.etree.ElementTree as ET
import subprocess
import json

def createCurlRequest(body):
    jsonStr1 = '''{
             "id": "string",
             "instanceAlignments": [
                 {
                 "alignments": [
                    {
                      "sourceTextEnd": 0,
                      "sourceTextStart": 0,
                      "targetTextEnd": 0,
                      "targetTextStart": 0
                    }
                  ],
                  "confidence": 0,
                  "sourceLanguage": "string",
                  "targetLanguage": "string"
                }
             ],
             "instances": [
                {
                  "body":"'''
    jsonStr2 = '''
                  ",
                    "metadata": {
                    "date": "string",
                    "language": "en",
                    "originalLanguage": "en",
                    "summary": "something",
                    "tags": ["string"],
                    "tokenizedText": [
                      {
                        "tokens": [
                          {
                            "offset": 0,
                            "sourceDocument": {
                              "id": "string",
                              "language": "string"
                            },
                            "token": "string"
                          }
                        ]
                      }
                    ],
                    "topics": ["string"]
                  },
                "title": "string"
              }
            ],
          "source": {
            "type": "string",
            "url": "string"
          }
       }'''
    jsonStr = jsonStr1 + body + jsonStr2
    jsonStr = jsonStr.replace('"', '\\"')
    jsonStr = '"' + jsonStr + '"'

    request = 'curl -X POST --header "Content-Type: application/json" --header "Accept: application/json" -d ' + jsonStr + ' "http://localhost:5001/EntityTagging/api/v2.0/processDocument?applyCoreference=true&applyEntityLinking=true"'
    print(request)
    return request

# curlAndRecordResponse:
# Sends the curl request containing body, and stores the result in the responseFile
def curlAndRecordResponse(body, responseFile):
    request = createCurlRequest(body)

    # requires python 3.5+
    result = subprocess.run(request, stdout=subprocess.PIPE, shell=True)
    responseFile.write(result.stdout.decode("utf-8") + "\n")

def main():

    # Read the file as a soup object
    fname = sys.argv[1]
    tree = ET.parse(fname)
    root = tree.getroot()
    docs = root.findall("DOC")

    prefix = fname.rstrip(".dat")
    prefix = prefix.split("/")[-1]
    outputFname = prefix + "_output.dat"
    responseFname = prefix + "_response.dat"
    outputFile = open(outputFname, "w+")
    responseFile = open(responseFname, "w+")

    docDict = dict()

    for doc in docs:
        no = doc.find("DOCNO").text
        hl = doc.find("HL").text
        # ln = doc.find("LN").text  # now dealing with 88
        text = doc.find("TEXT").text
        text = " ".join(text.split())

        # Process headline
        hls = [x.strip() for x in hl.split("----")]
        newhl = ""
        for hl in hls:
            newhl += hl
            newhl += " "

        usefulText = newhl + text

        docDict[no] = usefulText

        outputFile.write(usefulText+"\n")
        curlAndRecordResponse(usefulText, responseFile)

    outputFile.close()
    responseFile.close()


if __name__ == "__main__":
    main()

