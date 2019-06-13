import argparse
import requests
import xml.etree.ElementTree as ET
import hashlib
import io
import os
import json
import  urllib
from bs4 import BeautifulSoup
from json2html import *
import random


def get_pdf(doiurl,name):
    
    
    req = urllib.request.Request(doiurl)
    req.add_header('User-Agent', 'uMozilla/5.0')
    mgs = ""
	
    try:
        webpage = urllib.request.urlopen(req)
    except:
        mgs = "Error retrieving the pdf. Connection Error. Try manual download"
        return (mgs)

    
    soup = BeautifulSoup(webpage.read(), "html.parser")
    pdf_url_tag = soup.find_all("meta",attrs={"name": "citation_pdf_url"})
    
    if (len(pdf_url_tag) > 0):
        pdf_url =  pdf_url_tag[0]['content']
        try:
            urllib.request.urlretrieve(pdf_url, name)
            mgs = "PDF downloaded successfully"
            return (mgs)
        except:
            mgs = "Error retrieving the pdf. Try manual download"
            return (mgs)


def generateJson(dataset,filename):
    with io.open(filename, "w", encoding="utf-8") as f:
        f.write(json.dumps(dataset))
        f.close()
    
    

def generateHTML(dataset,filename):
    with io.open(filename, "w", encoding="utf-8") as f:
        f.write("<html>")
        f.write("<title>Report</title>")
        f.write("<link rel=\"stylesheet\" href=\"https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css\" integrity=\"sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T\" crossorigin=\"anonymous\">")
        f.write("<script src=\"https://code.jquery.com/jquery-3.3.1.slim.min.js\" integrity=\"sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo\" crossorigin=\"anonymous\"></script><script src=\"https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js\" integrity=\"sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1\" crossorigin=\"anonymous\"></script><script src=\"https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js\" integrity=\"sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM\" crossorigin=\"anonymous\"></script>")
        f.write("<style>li{list-style-type: none;} .table td, .table th {padding: .25rem; font-size: 12;} h1 {margin-left: 20px;} h2 {margin-left: 20px;} #summary-table {max-width: 600px; margin-left:30px}</style>")
        f.write("<body><h1>Report</h1>")
        f.write("<hr /><h2>Summary</h2>")
        f.write(json2html.convert(json.dumps(generateSummary(dataset)),table_attributes="id=\"summary-table\" class=\"table table-bordered table-hover\" ") )
        f.write("<hr/><h2>Details</h2>")
        f.write(json2html.convert(json.dumps(dataset),table_attributes="id=\"info-table\" class=\"table table-bordered table-hover\""))
        f.write("</body></html>")
        f.close()
    
    
def generateSummary(dataset):
    summary = {}
    totalOfCitations = 0
    totalOfPDFfetched = 0
    totalOfPDFattempted = 0
    totalOfCan = 0
    totalOfCannot = 0
    totalOfRestricted = 0
    totalCrossrefFailure = 0
    totalJournalNotFound = 0
    for citation in dataset:
        totalOfCitations = totalOfCitations + 1

        if('Attempting to download full text' in citation['Notes']):
            totalOfPDFattempted = totalOfPDFattempted + 1
        
        if('Unable to retrieve article information from Crossref' in citation['Notes']):
            totalCrossrefFailure = totalCrossrefFailure + 1
        
        if('PDF downloaded succesfully' in citation['Notes']):
            totalOfPDFfetched = totalOfPDFfetched + 1

        if('journal' in citation and  'pdf archiving' in citation['journal']):
           if( citation['journal']['pdf archiving'] == 'cannot' ):
               totalOfCannot = totalOfCannot +1
           if(citation['journal']['pdf archiving'] == 'restricted'):
               totalOfRestricted = totalOfRestricted +1
           if(citation['journal']['pdf archiving'] == 'can'):
               totalOfCan = totalOfCan +1
        
        if('journal' in citation and 'Note' in  citation['journal']):
            totalJournalNotFound = totalJournalNotFound + 1
        
    summary['Citations Checked'] = totalOfCitations
    summary['PDF Retrieved'] = totalOfPDFfetched
    summary['PDF Download Attempted'] = totalOfPDFattempted
    summary['Articles not found in Crossref'] = totalCrossrefFailure

    summary['Journals not resolved in Sherpa'] = totalJournalNotFound
    summary['Journals (Can Archive Publisher\'s PDF) in Sherpa'] = totalOfCan
    summary['Journals (Cannot Archive Publisher\'s PDF) in Sherpa'] = totalOfCannot
    summary['Journals (Restricted Archive Publisher\'s PDF) in Sherpa'] = totalOfRestricted

    return summary


    

        
        


    
    


def get_article_info(title,issn):
    url = "https://api.crossref.org/works?query="+title
    r = requests.get(url)
    cr_json = json.loads(r.text)
    info = {}
    for item in cr_json["message"]["items"]:
        found = False
        if 'ISSN' in item:    
            if (not found):
                for cr_issn in item["ISSN"]:
                    if (cr_issn == issn ):
                        info["DOI"] = item["DOI"]
                        info["URL"] = item["URL"]
                        found = True
    
    return info


def get_journal_info(jname,apikey):
    url = "http://www.sherpa.ac.uk/romeo/api29.php?jtitle="+jname+"&ak="+apikey
    r = requests.get(url)
    xml = ET.fromstring(r.text)
    journals = xml.findall("./journals/journal")
    
    result = {}
    result['shortName'] = jname
 
    for journal in journals:
        title = journal.find('./jtitle') 
        result['name'] = title.text
        issn = journal.find('./issn')
        result['issn'] = issn.text
        if issn.text is not None:
            result['sherpa link'] = "http://www.sherpa.ac.uk/romeo/issn/"+issn.text+"/ "
    

    publishers = xml.findall("./publishers/publisher")
    for publisher in publishers:
        colour = publisher.find('./romeocolour') 
        result['colour'] = colour.text

        pdfArchiving = publisher.find('./pdfversion/pdfarchiving')
        result['pdf archiving'] = pdfArchiving.text

        conditions = publisher.findall('./conditions/condition')
        conditionStr = ""
        counter = 1
        for condition in conditions:
            conditionStr = conditionStr + "(" + str(counter) + ") " + condition.text 
            counter = counter + 1

        result["conditions"] = conditionStr


    return result
    

def generate_reference(reference,name,apikey):
    

     objreference = {}
     objreference["Notes"] = "Trying to fetch the article"
    
     if(reference.find("./citation_number") != None):
         objreference["citation_number"] = reference.find("./citation_number").text
     else:
         objreference["citation_number"] = "unknown_reference_number" + str(random.randint(1,101))

     if(reference.find("./author") != None):
         objreference["author"] = reference.find("./author").text
     
          
     if(reference.find("./date") != None):
         objreference["date"] = reference.find("./date").text
    

     if(reference.find("./title") != None):
         objreference["title"] = reference.find("./title").text
         

     if(reference.find("./volume") != None):
         objreference["volume"] = reference.find("./volume").text
        
     if(reference.find("./pages") != None):
         objreference["pages"] = reference.find("./pages").text

     
     if(reference.find("./journal") != None and reference.find("./title") != None):
         
         objreference["journal"] = get_journal_info(reference.find("./journal").text,apikey)
         
         if('issn' in objreference["journal"] and 'title' in objreference):
         
             article_info = get_article_info(objreference["title"],objreference["journal"]["issn"])
             if('DOI' in article_info):
                 objreference["DOI"] = article_info["DOI"]
             else:
                 mgs = 'Unable to retrieve article information from Crossref'
                 objreference["Notes"] = objreference["Notes"] + ". " + mgs
         

             if('URL' in article_info):
                 objreference["URL"] = article_info["URL"]
         else:
             objreference["journal"]["Note"] = "Journal Information not found in Sherpa"

     #if open access try to download the pdf 
     if ('journal' in objreference  and 'URL' in objreference and  'colour' in objreference["journal"] and 'conditions' in objreference['journal'] and 'version/PDF may be used' in objreference['journal']['conditions'] ):
         path = name+"/"+objreference['journal']['colour']
         if(not os.path.isdir(path)):
            os.mkdir(path)
         filename = name +"/" + objreference['journal']['colour'] + "/" + objreference["citation_number"] + ".pdf"

         mgs = "Article is possibly open access. Attempting to download full text from the publisher's site" 
         objreference["Notes"] =objreference["Notes"] + ". " + mgs
         mgs = get_pdf(objreference["URL"],filename)
         if(type(mgs) is str):
             objreference["Notes"] =objreference["Notes"] + ". " + mgs

     else:
         mgs = "According to Sherpa, PDF archiving is not allowed for this article" 
         objreference["Notes"] = objreference["Notes"] + ". " + mgs
     return objreference

def reference_lookup(path,name,apikey):
     objxml = ET.parse(path)
     references = objxml.findall("./reference")
     objreferences = []

     for reference in references:
         if(reference.find("./citation_number") != None):
             print("Working of references number: " + reference.find("./citation_number").text)
         objreferences.append(generate_reference(reference,name,apikey))
 
     generateJson(objreferences,name+"/"+ "report.json")
     generateHTML(objreferences,name+"/"+ "report.html")
    


from gooey import Gooey
from gooey import GooeyParser
@Gooey(
    program_name = 'Concordia University Library Open Access Harvester',
    program_description = 'Harvest Open Access Articles from a parsed CV',
    image_dir='./img'
    )    

def main():
    parser = GooeyParser()
    
    parser.add_argument(    "target",
                            type=str,
                            help="Target Directory",
                        
                            widget='DirChooser')

    parser.add_argument(    "name",
                            type=str,
                            help="Researcher's name"
                            )

    parser.add_argument(    "cv",
                            type=str,
                            help="Path to the parsed CV in XML format",
                            widget='FileChooser')

    parser.add_argument(    "apikey",
                            type=str,
                            help="Sherpa / Romeo API key"
                            )


    args = parser.parse_args()
    if(args.target != None and args.name != None):
        
        target = args.target + "\\" + args.name
        os.mkdir(target)
        if(args.cv != None):
            reference_lookup(args.cv,target,args.apikey)



if __name__ == "__main__":
    main()
