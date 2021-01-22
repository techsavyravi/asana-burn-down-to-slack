from resume_parser import resumeparse
import os
import pandas as pd


bifurrrr = []


i = 0
for filename in os.listdir('./pdfs'):
    # if(i == 4):
    #     break
    i = i+1
    try:
        data = resumeparse.read_file('./pdfs/'+filename)
        print(data)
        bifurrrr.append(data)
    except:
        pass
    
    print(str(i) + " done")
df = pd.DataFrame(bifurrrr)
df.to_csv('yourfile.csv', index=False)
