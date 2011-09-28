# What is twitter2backlog

twitter2backlog is a utility to collect twitter mentions to your account
and post them to Backlog as an issue.

![Overview](https://cacoo.com/diagrams/VPIA0D2s6Kp98LFI-B9C35.png)

# Install

## pip

If pip is installed on your system, you can install by

    pip install twitter2backlog

NOTE: pip installation itself is also very easy if you have setuptools like

    easy_install pip

## source

If you want to use the latest (unstable) release, checkout source code and then run setup.py.

    git clone git://github.com/tksmd/twitter2backlog.git
    python setup.py install

# How to use

To run twitter2backlog, you need 2 configuration files, one for twitter and the other for Backlog.
Both of them have to contain authentication information to access their API.

## Twitter configuration

First, you have to create your application on dev.twitter.com.
To do this, first go https://dev.twitter.com/apps/new and fill in the form.
Submitting the form will show you a detail information of your application
and you will also find the "create my access token" button at the bottom of the page.
Click the button and finally you'll get your own access token and access token secret.

![Access token](https://cacoo.com/diagrams/VPIA0D2s6Kp98LFI-2DD38.png)

Now, you have enough information, so save it to a file like this.

    [default]
    consumer_key = XXXXXXXXXX
    consumer_secret = XXXXXXXXXX
    access_token = XXXXXXXXXX
    access_token_secret = XXXXXXXXXX

## Backlog configuration

Backlog configuration is quite simple, which gives
space, username and password with plain text. 
Example is below,

    [default]
    space = sample
    username = XXXXXXXXX
    password = XXXXXXXXX

## Run!

For example, you have authentication files named twitter.cfg 
and backlog.cfg, and then run

    twitter2backlog -r -H 12 -T twitter.cfg -B backlog.cfg -p TEST

will collect all the mentions created from the 12 hours ago to now 
and then post them to the Backlog project named "TEST".
If you want to run this script periodically, use cron like this. 

    0 0,12 * * * twitter2backlog -r -H 12 -T twitter.cfg -B backlog.cfg -p TEST

-h flags shows all available options of twitter2backlog.
