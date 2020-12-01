

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
from collections import OrderedDict
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
            'Keynote',
            'Atmosphere', 
            'Theory',
            'Solid-Earth', 
            'Datasets']

top = """

# Overview Schedule
| Start | End | Session | Session Chair | 
| ---- | ---- | --------- | ---------------- |  
| 06:45 | 06:55 |  Opening Remarks | S. Karthik Mukkavilli |  
| 06:55 | 08:55 | [Sensors and Sampling](#Sensors) | Johanna Hansen |  | 08:55 | 10:55 | [Ecology](#Ecology) | Natasha Dudek |   
| 10:55 | 12:45 | [Water](#Water) | S. Karthik Mukkavilli |   
| 12:45 | 13:25 | Keynote by Milind Tambe | S. Karthik Mukkavilli |   
| 13:25 | 15:25 | [Atmosphere](#Atmosphere) | Tom Beucler | | 15:25 | 17:20 | [Simulations, Physics-guided, and ML Theory](#ML-Theory) | Karthik Kashinath |  
| 17:20 | 18:00 | People-Earth Discussion | Mayur Mudigonda |  
| 18:00 | 19:00 | [Solid Earth](#Earth) | Kelly Kochanski |  
| 19:00 | 20:55 | [Datasets](#Datasets) | Karthik Kashinath |  
| 20:55 | 21:00 | Closing Remarks | Organizers |   

---

"""
#<!DOCTYPE html>
#th, td {
#<html>
#<head>
#<style>
#table, th, td {
#  border: 1px solid black;
#  border-collapse: collapse;
#}
#th, td {
#  padding: 5px;
#}
#th {
#  text-align: center 
#}
#</style>
#</head>
#<body>
#<style>
#table, th, td {
#  border: 1px solid black;
#  border-collapse: collapse;
#}
#<head>

table = """
<html>
<table style="width:90%">
  <colgroup>
  <col span="1" style="width: 2%;">
  <col span="1" style="width: 4%;">
  <col span="1" style="width: 10%;">
  <col span="1" style="width: 35%;">
  <col span="1" style="width: 20%;">
  </colgroup>
  <tr>
    <th>#</th>
    <th>Start Time</th>
    <th>Type</th>
    <th>Title</th>
    <th>Speakers/Authors</th>
    <th>Details</th>
  </tr>
"""

abs_ids = list(abstracts['Paper ID'].astype(np.int))
default_details = {'Introduction':'Short introduction to the session', 
                   'Discussion':'Live disccusion and Q&A with the speakers'}

long_length = int(len(default_details['Discussion']))

fo = open('schedule.md', 'w') 
fo.write(top)

for xx, session in enumerate(sessions):
    #fo = open('sessions/{}.html'.format(session.lower()), 'w') 
    session_name = session.title()
    fo.write("\n\n## {}  \n\n\n  ".format(session_name))
    fo.write(table)
    session_talks = papers.loc[papers['Primary Subject Area'] == session]
    order = sorted(list(session_talks['Order'].to_numpy().astype(np.int)))
    for ind in order:
        talk = session_talks.loc[session_talks['Order'] == ind]
        paper_id = talk['Paper ID'].to_numpy()[0]
        talk_type = talk['Type'].to_numpy()[0]
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
                        longform = abstracts[abstracts['Paper ID'] == paper_id]['Abstract'].to_numpy()[0]

            author = talk['Author Names'].to_numpy()[0].title()
        except Exception as e: 
            print(e)
            embed()


        spl_str = longform.split('. ')
        brk =  2  
        if len(spl_str) > brk:
            st = '. '.join(spl_str[:brk]) + '.'
            en = '. '.join(spl_str[brk:]) + '.'
            longline = """<p style="display:inline";>{} <details style="display:inline;"closed><summary>More</summary>{}</details></p>""".format(st, en)
        else:
            longline = longform

        line = """<tr>
                  <td style="text-align:center">{}</td>
                  <td style="text-align:center">{}</td>
                  <td style="text-align:center">{}</td>
                  <td style="text-align:center">{}</td>
                  <td style="text-align:center">{}</td>
                  <td style="text-align:justify">{}</td>
                  </tr>""".format(ind, talk_time, talk_type,
                             title, 
                             author, longline)

       

        fo.write(line)
    fo.write("</html>\n")
    fo.write("</table>\n\n\n")
    fo.write("end of {}".format(session_name))
    fo.write("#### [Return to top](#Overview-Schedule)\n\n  ")
    #fo.close()


