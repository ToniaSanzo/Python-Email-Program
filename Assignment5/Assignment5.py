# Author: Tonia Sanzo
# Programming Languages Spring 2019
#
# Assignment 5
# collects, summarizes and e-mails all the programming assignments
# for the spring 2019 csc 344 course


# subprocess and os lets you run unix commands in Python
# re lets you use regular expressions
import subprocess
import os
import re
from zipfile import ZipFile


#--- takes a projects directory and returns the path and word count of
#--- all the files in the
def assignment5_Main(argPath,numb):
    # Create a list of all the files and directorys in a path
    p = subprocess.Popen(["ls",argPath],stdout=subprocess.PIPE)
    output, err = p.communicate()
    fL = output.split()

    # Loop through each element in a list and depending on whether its a
    # directory (recursively call itself), or a file (display the file name and
    # number of lines within this file)
    i = 0
    while i < len(fL):
        tempPath = argPath + "/" + fL[i]
        cmpPath = argPath + "/src"
        if cmpPath == tempPath:
            infoList = recursiveLineCount(cmpPath,numb)
            i += 1
        else:
            i += 1
    createHTMLPage(infoList,numb)
    return infoList
#---


#--- Takes the formatted list that is created within this program and
#--- creates a valid html formated page, and adds it to the CS
#--- departments website.
def createHTMLPage(infoList,numb):
    htmlName = "/home/asanzo/public_html/summary_a" + str(numb) + ".html"
    htmlBody = ("<!DOCTYPE HTML>\n<html>\n  <head>\n    <title>Ass" +
               "ignment " + str(numb) + "</title>\n  </head>\n  <" +
               "body>\n    Tonia T. Sanzo<br>\n    CSC 344-Spring" +
               "<br>\n    Assignment " + str(numb) + "<br><br>\n\n")
    
    idx = 0
    while idx < len(infoList):
        htmlBody = (htmlBody +"    <a href = " + infoList[idx + 1]  +
                   ">" + str(infoList[idx]) + "</a><br>\n    Identifiers: ")
        idList = infoList[idx + 2]
        jdx = 0
        while jdx < len(idList):
            htmlBody = htmlBody + "<span style=\"color: "+'#'+"FF4500\">" + str(idList[jdx]) +"</span>" + "&nbsp;&nbsp;&nbsp;&nbsp;"
            jdx = jdx + 1
            if (jdx % 6) == 0 and (jdx + 1) < len(idList):
                htmlBody = htmlBody + "<br>\n    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        htmlBody = htmlBody + "<br><br>\n"
        idx = idx + 4
    
    htmlBody = htmlBody + "  </body>\n</html>"
    f = open(htmlName,"w")
    f.write(htmlBody)
    f.close()
#---


#--- Generate an index.html file in the csc344 file
def createIdxHtml():
    path = "/home/asanzo/public_html/csc344/index.html"
    body = ("<!DOCTYPE HTML>\n<html>\n  <head>\n    <title>Index" +
           "</title>\n  </head>\n  <body>\n    Tonia T. Sanzo<b" +
           "r>\n    CSC 344 - Spring<br>\n    Assignment 5<br><" +
           "br>\n\n    <a href = http://cs.oswego.edu/~asanzo/s" +
           "ummary_a1.html>Assignment 1</a><br>    <a href = h" +
           "ttp://cs.oswego.edu/~asanzo/summary_a2.html>Assignm" +
           "ent 2</a><br>\n    <a href = http://cs.oswego.edu/~" +
           "asanzo/summary_a3.html>Assignment 3</a><br>\n    <a" +
           " href = http://cs.oswego.edu/~asanzo/summary_a4.htm" +
           "l>Assignment 4</a><br>\n    <a href = http://cs.osw" +
           "ego.edu/~asanzo/summary_a5.html>Assignment 5</a><br" +
           "><br>\n\n  </body>\n</html>")
    with open(path, 'w') as myfile:
        myfile.write(body)
#---
    
    
#--- Given a string, returns a list of all the identifiers, wth 
#--- all duplicates removed.
def returnIdentifiers(textStr,numb):
    if numb < 4:
        regex = "\/\*\*(\n\*.*)*|\".*\"|\[|\]|\(|\)|\-|\>|\<|\.|\;\;.*|\;|\&|=|!|\{|\}|\/\/.*|\*|#|,|\+|:|\^|~|\|"
    elif numb == 4:
        regex = "%.*|\(|\)|\||\[|\]|,|:-|=|\;|\.|\\\+|\+|-|\>|\<"
    else:
        regex = "\#.*\n|\".*\"|'.*'|=|\+|\(|\)|\[|\]|,|\.|\<|:|\>"

    x = re.sub(regex," ",textStr)
    x = x.split()
    setX = set()
    idx = 0
    while idx < len(x):
        setX.add((x[idx],))
        idx = idx + 1

    tList = []
    flag = True
    while flag:
        try:
            v = setX.pop()
            tList.append(v[0])
        except:
            flag = False
    return tList
#---

#--- Zips up the sorces files in the current directory
def zipUp(list,numb):
    zipList = []
    idx = 3
    while idx < len(list):
        zipList.append(list[idx])
        idx = idx + 4

    zipName = "Assignment" + str(numb) + ".zip"
    with ZipFile(zipName,"w") as zip:
        # writing each file one by one
        for file in zipList:
            zip.write(file)

    print "Successful zipping"
#---


def zipHtml():
    with ZipFile("htmlFiles.zip","w") as zip:
        zip.write("/home/asanzo/public_html/summary_a1.html")
        zip.write("/home/asanzo/public_html/summary_a2.html")
        zip.write("/home/asanzo/public_html/summary_a3.html")
        zip.write("/home/asanzo/public_html/summary_a4.html")
        zip.write("/home/asanzo/public_html/summary_a5.html")
        zip.write("/home/asanzo/public_html/csc344/index.html")
    print "Successful zipping"




#--- Returns a list of the word count and path to a specific file
#--- within the src file of a assignment directory.
def recursiveLineCount(argPath,numb):
    # Create a list of all the files and directorys in a path
    p = subprocess.Popen(["ls",argPath],stdout=subprocess.PIPE)
    output, err = p.communicate()
    fileList = output.split()
    returnList = []
    idx = 0

    while idx < len(fileList):
        tempPath = argPath + "/" + fileList[idx]
        if os.path.isdir(tempPath):
            recursiveList = recursiveLineCount(tempPath,numb)
            jdx = 0
            while jdx < len(recursiveList):
                returnList.append(recursiveList[jdx])
                returnList.append(recursiveList[jdx + 1])
                returnList.append(recursiveList[jdx + 2])
                returnList.append(recursiveList[jdx + 3])
                jdx = jdx + 4
            idx = idx + 1
        else:
            x = subprocess.check_output(["wc","-l",tempPath]).split()
            sTr = fileList[idx] + ":- Number of lines " + str(x[0])
            returnList.append(sTr)
            returnList.append("http://cs.oswego.edu/~asanzo"+tempPath[24:])
            with open(tempPath, 'r') as myfile:
                data = myfile.read()
            data = data.replace("\r","")
            returnList.append(returnIdentifiers(data,numb))
            returnList.append(tempPath)
            idx = idx + 1
    return returnList
#---


#---
def sendEmails(recipient):
    zipHtml()
    
    cmd1 = '/home/asanzo/uuencode Assignment1.zip Assignment1.zip | mail -s "Assignment 1, source files" ' + recipient
    cmd2 = '/home/asanzo/uuencode Assignment2.zip Assignment2.zip | mail -s "Assignment 2, source files" ' + recipient
    cmd3 = '/home/asanzo/uuencode Assignment3.zip Assignment3.zip | mail -s "Assignment 3, source files" ' + recipient
    cmd4 = '/home/asanzo/uuencode Assignment4.zip Assignment4.zip | mail -s "Assignment 4, source files" ' + recipient
    cmd5 = '/home/asanzo/uuencode Assignment5.zip Assignment5.zip | mail -s "Assignment 5, source files" ' + recipient
    cmd6 = '/home/asanzo/uuencode htmlFiles.zip htmlFiles.zip | mail -s "HTML files" ' + recipient


    os.system(cmd1)
    os.system(cmd2)
    os.system(cmd3)
    os.system(cmd4)
    os.system(cmd5)
    os.system(cmd6)




recipient = raw_input("Enter the recipient's Email address: ")

path1 = "/home/asanzo/public_html/csc344/a1"
path2 = "/home/asanzo/public_html/csc344/a2"
path3 = "/home/asanzo/public_html/csc344/a3"
path4 = "/home/asanzo/public_html/csc344/a4"
path5 = "/home/asanzo/public_html/csc344/a5"
l1 = assignment5_Main(path1,1)
l2 = assignment5_Main(path2,2)
l3 = assignment5_Main(path3,3)
l4 = assignment5_Main(path4,4)
l5 = assignment5_Main(path5,5)

zipUp(l1,1)
zipUp(l2,2)
zipUp(l3,3)
zipUp(l4,4)
zipUp(l5,5)

createIdxHtml()
sendEmails(recipient)
print("Emails sent too " + recipient)
