import sys
import xml.etree.ElementTree as ET

# Containing tags from 87~89
tags = ['DOC', 'DOCNO', 'DD', 'AN', 'HL', 'SO', 'CO', 'IN', 'TEXT', 'DATELINE', 'AUTHOR']
def main():

    # Read the file as a soup object
    # fname = sys.argv[1]
    with open("wsj87.dat") as f:
        soup = BeautifulSoup(f, "xml")
    # soup = BeautifulSoup("<DOC><DOCNO> wsj1212 </DOCNO><HL>funny</HL><TEXT>this is a test</TEXT></DOC>", "lxml")
    print(soup.prettify())

    outputFname = fname.split(".")[0] + "_output.dat"
    outputFile = open(outputFname, "w+")

    docs = soup.find_all("doc")

    docDict = dict()
    for doc in docs:
        no = doc.DOCNO
        hl = doc.Hl
        ln = doc.LN  # TODO: what if no <LN> tag?
        text = doc.TEXT

        # Process headline
        hls = [x.strip() for x in hl.split("----")]
        newhl = ""
        for hl in hls:
            newhl += hl
            newhl += " "

        usefulText = newhl + ln + text

        docDict[no] = usefulText

        outputFile.write(usefulText+"\n")

    outputFile.close()


if __name__ == "__main__":
    main()

