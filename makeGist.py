#!/usr/bin/env python

# Copyright (c) 2012 Brett Kelly
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import urllib2
import urllib
import base64
import json
from optparse import OptionParser
import os.path
import sys

github_user = 'your github username'
github_pass = 'your github password'

auth_url = 'https://api.github.com/authorizations'
gist_url = 'https://api.github.com/gists'

# tokens are shoved into ~/.ghtoken because why the hell not.
token_file = os.path.join(os.path.expanduser('~'),'.ghtoken')

class Gist(object):
    "Represents a single gist"
    def __init__(self, description, files, public):
        self.description = description
        if type(files) != list: 
        	files = [files]
		self.files = files
        self.public = public
    
    @property
    def asJSON(self):
    	"Return Gist as a JSON block"
        data = {
            'description': self.description,
            'public': self.public,
            'files': {}
        }
        for f in self.files:
            data['files'][f.name] = {'content': f.content}
        return json.dumps(data)
    
class GistFile(object):
    "A file attached to a gist"
    def __init__(self, name, content):
        self.name = name
        self.content = content
        
def makeOptsParser():
	"options for Filename, description, public/private"
	parser = OptionParser()
	parser.add_option('-f','--filename', dest="filename")
	parser.add_option('-d','--description', dest="description", default="")
	parser.add_option('-p','--public', action="store_true", dest="public")
	parser.add_option('-c','--contents', dest="gist_text")
	return parser	

def loadGithubAuthToken():
    "Get a stored auth token if we already have one"
    if os.path.exists(token_file):
        return open(token_file).read()
    return None

def saveGithubAuthToken(token):
    "Write our auth token to a dotfile in the user's home directory"
    with open(token_file, 'w+') as fd:
        fd.write(token)
    
def getGithubAuthToken():
    "Get a Github auth token and return it"
    gist_data = json.dumps({"scopes":["gist"], "note":"Accessing gists"})
    req = urllib2.Request(auth_url)
    base64str = base64.encodestring("%s:%s" % \
        (github_user, github_pass)).replace('\n','')
    req.add_header("Authorization", "Basic %s" % base64str);
    req.add_data(gist_data)

    try:
        response = urllib2.urlopen(req)
    except urllib2.URLError, e:
        print "Something broke connecting to Github: %s" % e
        return None
         
    if response.getcode() == 201:
        jresp = json.loads('\n'.join(response.readlines()))
        return jresp['token']
    return None 

def createGist(token, gist):
    "Create a github gist and return the URL"
    req = urllib2.Request(gist_url, gist.asJSON)
    req.add_header("Authorization", "token %s" % token)
    
    try:
        response = urllib2.urlopen(req)
    except urllib2.URLError, e:
        return None
    
    if response.getcode() == 201:
        jresp = json.loads('\n'.join(response.readlines()))
        return jresp['html_url']
    return None

(opts, args) = makeOptsParser().parse_args()

## First, attempt to load the existing token
token = loadGithubAuthToken()
 
## If no token exists, get a new one and save it    
if not token:
    token = getGithubAuthToken()
    if not token:
        raise SystemExit('Broken')
    saveGithubAuthToken(token)

snippetText = opts.gist_text

gFile = GistFile(opts.filename, snippetText)
gist = Gist(opts.description, gFile, opts.public)
gistUrl = createGist(token, gist)

print gistUrl
