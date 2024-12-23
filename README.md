# Mapping-of-Greater-India-Journal

**How to Open the Mapping Tool in 3 Steps**

**Step 1:** *Open Terminal*

Terminal is an app on your laptop that you can find by searching. This
is what developers use to run scripts and download software

**Step 2:** *Enter the Correct Folder*

Using the command "cd" we can enter folders until we are in the one
called UI which contains the script for our app. Type the following:

cd Documents/Github/Mapping-of-Greater-India-Journal/UI

Then click enter.

**Step 3:** *Run the Script*

The script to run this app is called app.py. The .py extension means it
is written in the coding language Python. So, in the terminal
type:

python app.py

And click enter. If this doesn't work it is probably because your python
system is "too updated" instead try:

python3 app.py

This tells your computer to use python's updated version 3 software.

**How to Build a Map from pdfs**

**Step 1:** *Name your pdfs*

To label the document in the map name your document anything with a
number. The number as well as any text after the number will be included
in the final map.

Ex. text_that_won't_appear123MyDocument.pdf -\> 123MyDocument

**Step 2:** *clear directory and upload*

Click "Clear File Directory" to remove previously scanned documents.
Then Click "Upload Files" and select your pdfs. (It may help to have the
pdfs in a folder)

**Step 3:** *OCR the pdfs*

Click "OCR Scanned PDFs" to convert the uploaded documents into text
documents. This process can take 5 minutes per document. Alternatively,
if you want to make a map from text documents you will still have to
click this button to make sure the files are in the right place for the
next step, but the process will take only a second. IMPORTANT NOTE: If
you are running with text documents change the names of the documents so
that they end in "OCR.pdf.txt"

**Step 4:** *Run NLP (Natural Language Processing)*

Click "Use NLP to Scan for Location Names." Unfortunately, this step
takes 10-15 minutes per file. This generates a csv file containing named
locations by document that will be converted to the map in the next
step.

To exit without completing this step x out of the application and click
control C and enter in the terminal really fast until it stops showing
new location names

**Step 5:** *Name and Create The Map*

Enter the map name where it says to *before* clicking create map. Then
click "create map." For a huge data set this takes around 5 minutes.

**Step 6:** *Open The Map*

Clicking "Display Map" opens a list of all maps you or we have made (in
the map folder). Simply click a map and it will be displayed. The final
map we created is called "Blue Map"

**Other Features of the Mapping Tool: ft. Where are these files?**

**Generate Word Count Sheet:** Generates word count table for uploaded
documents

**Change API Key:** An API key is a string of letters like a password
that you get from google cloud and allows you to use their service to
locate places. We are using a free trial of one of our accounts, so once
you create your own you can enter the key hear to keep the system
working

**Finding these Files Manually:**

Remember that cd command? That is the path to the files meaning they are
in your GitHub folder which is in your Documents folder. Get to your
Documents Folder through Finder. Then click GitHub, then
Mapping-of-Greater-\...-Journal which contains the following:

*ReadMe:* This document of instructions

textFilestoScan: The files you provided converted to text. There is a
full file of all the documents and a small testing subset

*UI:* Everything Else

**Things you may want to do manually in this Folder:**

*Open word count sheet*

This sheet is in uploads, then in pdfs, then in Text Docs

*Open the csv file of info that gets mapped*

This is in UI and called MasterLocationFile.csv. Also, the file
MasterLocationFileFullDataSave.csv is a file that won't be modified by
the code but contains all the data from the provided journals.

*Delete Maps*

All your maps are in the uploads folder then in the maps folder. You can
open them or remove them from here.
