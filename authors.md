---
layout: default
title: AI for Earth Sciences
--- 


## Info for Accepted Papers

Please update your .sty files in latex to the [this version](https://github.com/ai4earthscience/neurips-2020-workshop/blob/master/misc/neurips_2020.sty) which reflects the name of the workshop. 

Alternatively, you may do this manually by replacing lines 73:81 in your current .sty file with: 

`
\else  
  \if@neuripsfinal  
    \newcommand{\@noticestring}{%  
    AI for Earth Sciences Workshop at NeurIPS \@neuripsyear.% 
    } 
    \else 
    \newcommand{\@noticestring}{% 
    Submitted to the AI for Earth Sciences Workshop at NeurIPS \@neuripsyear. Do not distribute.% 
    }  
`
