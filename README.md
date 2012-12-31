You'd better believe this is `bbedit-gist-maker`
=================

### Preamble

This little dingus lets you create Github gists from within BBEdit.

### Requirements

You'll need the following:

* An Apple Macintosh Computer
* An account on Github
* BBEdit installed

The first of many caveats: this has been tested with the following versions of the above applications:

* **Python 2.7.2**
* **BBEdit 10.5.x**

It may or may not work with other versions. If in doubt, give it a try and see.

### Setup

Put the AppleScript (or a symlink to the AppleScript) in your `~/Library/Application Support/BBEdit/Scripts` directory. That will place 'Make BBEdit Gist' in your Scripts menu in BBEdit. The AppleScript expects the Python script to be in the same directory, so make sure it is.

Next, make sure you populate the `github_user` and `github_pass` variables in `makeGist.py` with your Github username and password. This thing won't work otherwise (sry).

### Usage

To use the Python program on its own, run it like this:

`$ python makeGist.py -f filename.txt -d "gist description" -c "contents of the gist"`

This will create a private gist; to create a public gist, add the `-p` flag.

### Known Issues/To Do

* This thing uses your Github username/password to get an auth token for the Gist API. It's sent over SSL, but there's surely a better way to go about it.
* Add a UI for notifying the user that something broke or that the process completed successfully.
* Error handling in the python script could be much nice and non-crappy.
* When adding the two files to the Scripts directory in BBEdit's Application Support folder, there's now way to suppress the appearance of `makeGist.py`. This is annoying and I'm not sure how to prevent this from happening.

If you use this and want to make it better, feel free to dink around with it and send me a pull request if you do something awesome.