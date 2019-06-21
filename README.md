## Install

1. Install Python 3.4 + virtualenv
2. (optional) `virtualenv -p python3 pyenv`
3. (optional) `. pyenv/bin/activate`
4. `pip3 install flask`

## Run

1. (if in virtualenv) `. pyenv/bin/activate`
2. `python3 BrokenApp.py`
3. Open [http://localhost:8001](http://localhost:8001) in your browser

Credentials: user/pass

## Burp

The file *BurpSessionHandling.burp-projectopts.json* can be loaded as project
options file and contains session handling rules to solve the challenges
from the slides in Burp Session Handling.pdf.

