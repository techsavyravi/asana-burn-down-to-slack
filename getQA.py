# Importing libraries 
import imaplib, email 
from urllib.parse import urlparse, unquote
import re
import pandas as pd
import quopri
import html
import requests
import os

user = 'ravi@idreamcareer.com'
password = 'ravi12345'
imap_url = 'imap.gmail.com'

if os.path.exists("./pdfs/a.sh"):
  os.remove("./pdfs/a.sh")

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

# Function to get email content part i.e its body part 
def get_body(msg): 
    if msg.is_multipart(): 
        return get_body(msg.get_payload(0)) 
    else: 
        return msg.get_payload(None, True) 
  
# Function to search for a key value pair  
def search(key, value, con):  
    result, data = con.search(None, key, '"{}"'.format(value)) 
    return data 
  
# Function to get the list of emails under this label 
def get_emails(result_bytes): 
    msgs = [] # all the email data are pushed inside an array 
    for num in result_bytes[0].split(): 
        typ, data = con.fetch(num, '(RFC822)') 
        msgs.append(data) 
  
    return msgs 
  
# this is done to make SSL connnection with GMAIL 
con = imaplib.IMAP4_SSL(imap_url)  
  
# logging the user in 
con.login(user, password)  

# calling function to check for email under this label 
con.select('"QA Job"')  
  
 # fetching emails from this user "tu**h*****1@gmail.com" 
msgs = get_emails(search('FROM', 'jobs-listings@linkedin.com', con)) 
  
# Uncomment this to see what actually comes as data  
# print(msgs)  
  
  
# Finding the required content from our msgs 
# User can make custom changes in this part to 
# fetch the required content he / she needs 
  
# printing them by the order they are displayed in your gmail  

for msg in msgs[::-1]:  
    for sent in msg: 
        if type(sent) is tuple:  
            # print(sent)
            # encoding set as utf-8 
            content = str(sent[1], 'utf-8')  
            data = str(content) 
  
            # Handling errors related to unicodenecode 
            try:  
                indexstart = data.find("ltr") 
                data2 = data[indexstart + 5: len(data)] 
                indexend = data2.find("</div>") 
  
                # printtng the required content which we need 
                # to extract from our email i.e our body 
                try:
                    name = find_between(data2[0: indexend], ".....................................", "Download resume:").splitlines()[8]
                    print(name)
                except:
                    pass
                


                url = find_between(data2[0: indexend],"Download resume:","View full application:")
                decoded_string=quopri.decodestring(url)
                newlineremoved = " ".join(str(decoded_string.decode('utf-8')).split())
                finalURL = html.unescape(newlineremoved)
                print(finalURL)
                # r = requests.get(finalURL, stream=True)
                
                with open('./pdfs/a.sh', 'a+') as fd:
                    fd.write("wget " + finalURL + "\n")

  
            except UnicodeEncodeError as e: 
                pass
            except:
                pass
