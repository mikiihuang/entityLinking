import sys
import xml.etree.ElementTree as ET

def main():

    # Read the file as a soup object
    fname = sys.argv[1]
    tree = ET.parse(fname)
    root = tree.getroot()
    docs = root.findall("DOC")
    print(docs[0].find("TEXT").text)

    outputFname = fname.split(".")[0] + "_output.dat"
    outputFile = open(outputFname, "w+")

    docDict = dict()
    for doc in docs:
        no = doc.find("DOCNO").text
        hl = doc.find("HL").text
        # ln = doc.find("LN").text  # now dealing with 88
        text = doc.find("TEXT").text

        # Process headline
        hls = [x.strip() for x in hl.split("----")]
        newhl = ""
        for hl in hls:
            newhl += hl
            newhl += " "

        usefulText = newhl + text

        docDict[no] = usefulText

        outputFile.write(usefulText+"\n")

    outputFile.close()


if __name__ == "__main__":
    main()

