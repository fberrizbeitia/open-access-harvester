# Concordia University Library Open Access Harvester
The Open Access Harvester starts with an xml list of numbered, bibliographic citations (say, from a CV), which has been parsed. The harvester uses the xml file as input, and identifies any citations published in journals where Sherpa/Romeo indicates that a "Publisher PDF" may be deposited in an institutional repository.   

It is important to note that the program relies on the presence of citation numbers.  If these are not already present, citation numbers must be added/created before parsing takes place, e.g.:

1. Appel, R., & Trofimovich, P. (2017). Transitional probability predicts native and non-native use of formulaic sequences. International Journal of Applied Linguistics, 27, 24–43. doi: 10.1111/ijal.12100  Trofimovich, P.
2. Appel, R., Trofimovich, P., Saito, K., Isaacs, T., & Webb, S. (in press). Lexical aspects of comprehensibility and nativeness from the perspective of native-speaking English raters. ITL - International Journal of Applied Linguistics. Trofimovich, P.
3. Ayotte-Beaudet, J.-P., Potvin, P., Lapierre, H. G., & Glackin, M. (2017). Teaching and learning science outdoors in schools’ immediate surroundings at K-12 levels: A meta-synthesis. Eurasia Journal of Mathematics Science and Technology Education, 13(9), 5343-5363. doi: 10.12973/eurasia.2017.00833a Potvin, P.

We used [http://anystyle.io](http://anystyle.io) to produce the list of citations in xml format, but you can use any parser you like to prepare the list of citations.Using your parsed citations, the tool finds the DOIs of the citations, checking each journal against Sherpa/Romeo database to determine whether the journal allows a "green" Publisher PDF deposit.
  
If the journal publisher allows such a deposit, the harvester retrieves the publisher PDF and puts it into a "green" folder.  Where Sherpa/Romeo classifies as yellow [OA restricted] but depositing the publisher's PDF is permitted, these pdfs are also harvested and placed in respective "yellow" folder.

When the program is finished, two reports are generated:  report.json, and a formatted version of the results report.html, along with the folders containing the pdfs retrieved.


### Download and Run

Download the Open Access Harvester to install the .exe to run.

Enter your Target Directory, using the Browse button to navigate to the directory where you want the program's output to be located, e.g. a shared network drive, local PC, etc.

Enter Researcher's name use consistent naming convention, e.g.  LastName_FirstName_MiddleInitial

In the cv section, provide the directory path to your parsed CV in XML format.

Apply for Sherpa/Romeo api key by visiting http://sherpa.ac.uk/romeo/apiregistry.php, then enter the apikey. 

Click START to run. While the program is running, a green progress bar displays. Depending on the size of the file, it may take a while to run. To cancel, press Stop. When the program is finished, a dialog box will appear. 



### Viewing Output Results

Navigate to your target folder.  Two files are generated:  report.html and report.json.  If any PDFs were retrieved, a corresponding 'OA color' folder is generated (e.g., green, yellow, blue).  

Open report.html lists every citation processed by OA Harvester, and includes as much detail as can be found for the following elements:

* Notes – possible values:
  * Trying to fetch the article. PDF archiving is not allowed for this article
  * Unable to retrieve article information from Crossref. PDF archiving is not allowed for this article.
  * Article is possibly open access. Attempting to download full text from the publisher's site.  
  * Error retrieving the pdf.  Try manual download.
  * Attempting to download full text from the publisher's site.  PDF downloaded successfully.

* Citation number
* Author(s) of article
* Date article published.  
* Title of the article
* Volume/Issue
* Pages
* Journal in which article was published
* Short name
* Long journal title
* ISSN
* Sherpa link if found
* Colour (green, yellow, blue, white) as assigned by Sherpa
* PDF Archiving allowed – possible values:
    * Can
    * Cannot
    * Restricted
    * Unknown
    * Conditions of archiving listed at Sherpa
* DOI
* URL

All of the data contained in report.html is contained in the report.json file.  To view the results data as a spreadsheet, take the report.json and use a conversion tool like json to csv to change it into a csv or xlsx.    


### Folders  
Inside the green and/or yellow folders, retrieved PDFs are listed according to the citation number in the original parsed file. 

If a folder is empty, check the report.html for occurrences of "manual download" (use CTRL-F).    The URL link in the report can be used to download those pdf(s) manually.

Examples and screenshots are included in the full documentation.


# Documentation
For detailed, step by step intructions on how to use the software please read the [full documentation](./CU_Open_Access_Harvester.pdf).


# About and Contact

The Concordia University Library Open Access Harvester was developed at Concordia University Library as an ongoing academic effort. You can contact the current maintainers by email at francisco[dot]berrizbeitia[at]concordia[dot]ca

We strongly encourage you to please report any issues you have when using the software. You can do that over our contact email or creating a new issue here on Github.


# License

[BSD 3-Clause License](LICENSE). 
