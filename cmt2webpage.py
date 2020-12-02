

#---
#layout: default
#title: AI for Earth Sciences
#description: org
#---
#
### Sensors and Sampling Schedule
#
#| Start | End | Type | Speaker | Title and Info |
#| ---- | ---- | --------- | ------------- | ----------------- |
#| 6:55 | 6:58 | Intro | Johanna Hansen | Session Overview and Introduction |
#| 6:58 | 7:22 | Keynote | [Yogesh Girdhar](http://warp.whoi.edu/) | [Curious Robots for Scientific Sampling](#yogesh-girdhar) |

import pandas as pd
import numpy as np
from glob import glob
import os
from collections import OrderedDict
import pytz
from datetime import datetime
from icalendar import vDatetime, Calendar, Event
import shutil
from IPython import embed
p = pd.read_csv("AI4Earth_Papers_all.csv") # export from google doc which was from cmt
a = pd.read_csv("abstracts.csv")
abstracts = a[['Paper ID', 'Abstract', 'Paper Title']]
# some rows are nan because they are breaks bt sessions
isna = [pd.notna(x) for x in p['Authors']]
papers = p[isna]
# we only want to work with accepts
papers = papers[papers['Accept/Reject'] != 'reject']
# fix author names
# collect abstracts
papers.loc[papers['Primary Subject Area'] == 'Sensors & Sampling', 'Primary Subject Area'] = 'Sensors'
# dont merge since some dont have abstracts
#papers = pd.merge(papers, abstracts, on='Paper ID')
sessions = ['Sensors', 
            'Ecology', 
            'Water', 
            'Atmosphere', 
            'Theory',
            'Earth', 
            'Datasets']

top = """

# Overview Schedule
| Start | End | Session | Session Chair |  
| ---- | ---- | --------- | ---------------- |  
| 06:45 | 06:55 | Opening Remarks                  | S. Karthik Mukkavilli |  
| 06:55 | 08:55 | [Sensors and Sampling](#sensors) | Johanna Hansen |  
| 08:55 | 10:55 | [Ecology](#ecology)              | Natasha Dudek |   
| 10:55 | 12:45 | [Water](#water)                  | S. Karthik Mukkavilli |   
| 12:45 | 13:25 | [Keynote: Milind Tambe](https://teamcore.seas.harvard.edu/people/milind-tambe)  | S. Karthik Mukkavilli |   
| 13:25 | 15:25 | [Atmosphere](#atmosphere)        | Tom Beucler |  
| 15:25 | 17:20 | [ML Theory](#theory) | Karthik Kashinath |  
| 17:20 | 18:00 | People-Earth Roundtable          | Mayur Mudigonda |  
| 18:00 | 19:00 | [Solid Earth](#earth)            | Kelly Kochanski |  
| 19:00 | 20:55 | [Datasets](#datasets)            | Karthik Kashinath |  
| 20:55 | 21:00 | Closing Remarks                  | Organizers |   

## [Join our slack for live Q&A](https://join.slack.com/t/ai4earth/shared_invite/zt-jkg0i982-VYRAd0HbjCG_6970Hcqfwg)  


---

"""

table = """
<html>
<p style="display:inline";>
<table>
  <colgroup>
  <col span="1" style="width: 1%;">
  <col span="1" style="width: 2%;">
  <col span="1" style="width: 8%;">
  <col span="1" style="width: 20%;">
  <col span="1" style="width: 15%;">
  </colgroup>
  <tr>
    <th>#</th>
    <th>Start Time</th>
    <th>Type</th>
    <th>Title</th>
    <th>Speakers</th>
    <th>Details</th>
  </tr>
"""

abs_ids = list(abstracts['Paper ID'].astype(np.int))
default_details = {'Introduction':'Short introduction to the session', 
                   'Discussion':'Live discussion and Q&A with the speakers. Post questions to slack to hear from our speakers.', 
                   'Break':'Break to grab a coffee and check out our on-demand talks'}

long_length = int(len(default_details['Discussion']))
# paper have the ID\CameraReady in beginning of name
cam_readys = glob('papers/*CameraReady*.pdf')
fo = open('schedule.md', 'w') 
fo.write(top)
tz = pytz.timezone('US/PAcific')
sitename = 'https://ai4earthscience.github.io/neurips-2020-workshop/'
for xx, session in enumerate(sessions):
    #fo = open('sessions/{}.html'.format(session.lower()), 'w') 
    session_name = session.title()
    fo.write("\n\n---".format(session_name))
    fo.write("\n\n## {}  \n\n\n  ".format(session_name))
    fo.write(table)
    session_talks = papers.loc[papers['Primary Subject Area'] == session]
    order = sorted(list(session_talks['Order'].to_numpy().astype(np.int)))
    for ind in order:
        talk = session_talks.loc[session_talks['Order'] == ind]
        paper_id = talk['Paper ID'].to_numpy()[0]
        talk_type = talk['Type'].to_numpy()[0].title()
        talk_time = talk['Time'].to_numpy()[0]
        if talk_time == 'On-demand':
            talk_time = '---'
        longform = "" 
        longline = ""
        title = talk['Paper Title'].to_numpy()[0].title()
       
        try:
            # enter abstract
            if talk_type in default_details.keys():
                longform = default_details[talk_type]
                longline = longform 
            else:
                if np.isnan(paper_id):
                    longform = talk['Bio'].to_numpy()[0]
                else:
                    if paper_id in abs_ids:
                        # check to see if camera ready is available

                        paper_id = int(paper_id)
                        st_with = 'papers/{}'.format(paper_id)
                        for x in cam_readys:
                            if x.startswith(st_with):
                                target_link = 'papers/ai4earth_neurips_2020_%02d.pdf' %paper_id
                                shutil.copy2(x, target_link)
                                title = '<a href="{}">{}</a>'.format(os.path.join(sitename,target_link), title)
                                print(title)
                        # get the abstract
                        longform = abstracts[abstracts['Paper ID'] == paper_id]['Abstract'].to_numpy()[0]

            author = talk['Authors'].to_numpy()[0].replace('()', '')

            link = talk['Link'].to_numpy()[0]
            if type(link) == str:
                author = '<a href="{}">{}</a>'.format(link.strip(), author.strip())

            # split long abstracts/bios in to visible and "more" after 2 sentences
            # hacky 
            spl_str = longform.strip().split('. ')
            brk =  2
            if len(spl_str) > brk:
                st = '. '.join(spl_str[:brk]) + '.'
                en = '. '.join(spl_str[brk:]) 
                # something about Deepfish messes up the html summary function 
                if 'Deepfish' in title:
                    longline = longform.strip() 
                elif 'Boots' in title: 
                    longline = longform.strip() 
                else:
                #longline = """<p style="display:inline";>{}<details style="display:inline;"closed><summary>More</summary>{}</details></p>""".format(st, en)
                    longline = """{}<details style="display:inline;"closed><summary>More</summary>{}</details>""".format(st, en)
            else:
                longline = longform

            line = """<tr>
                      <td style="text-align:center">{}</td>
                      <td style="text-align:center">{}</td>
                      <td style="text-align:center">{}</td>
                      <td style="text-align:center">{}</td>
                      <td style="text-align:center">{}</td>
                      <td style="text-align:left">{}</td>
                      </tr>""".format(ind, talk_time, talk_type,
                                 title, 
                                 author, longline)

       

            fo.write(line)

        except Exception as e: 
            print(e)
            embed()
    fo.write("</table>\n")
    fo.write("</html>\n\n")
    session_jumps = ['[{}](#{})'.format(s, s.lower()) for s in sessions]
    fo.write('### Jump to: [Overview](#overview-schedule)  -  {}\n\n'.format('  -  '.join(session_jumps)))
fo.close()


