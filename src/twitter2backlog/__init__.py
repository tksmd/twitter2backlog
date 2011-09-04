#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2011 Takashi SOMEDA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

"""
一定期間に twitter アカウントに対してなされた mention をまとめて Backlog に課題として登録するユーティリティ
"""

import sys
import os
import datetime
import codecs

from ConfigParser import SafeConfigParser, InterpolationMissingOptionError
from optparse import OptionParser, OptionGroup, OptionValueError
from string import Template

import tweepy
import pytz
from backloglib import Backlog

__version__ = "0.0.1"
__author__ = "someda@isenshi.com"

_DATE_FORMAT_ = "%Y/%m/%d %H:%M:%S"

class _OptionParser(OptionParser):
        
    def _setup(self):
        self.add_option("-r", "--run", dest="run", action="store_true", default=False, help="if set, only fetching twitter mentions")
        self.add_option("-t", "--timezone", dest="timezone", default="Asia/Tokyo", help="timezone string default Asia/Tokyo")
        self.add_option("-H","--hours", dest="hours", default=0, type="int", action="callback", callback=_OptionParser.num_callback, help="period hours")
        self.add_option("-D","--days", dest="days", default=1, type="int", action="callback", callback=_OptionParser.num_callback, help="period days")    
        
        tw_parser = OptionGroup(self, "Twitter Related Options")
        tw_parser.add_option("--consumer_key", dest="consumer_key", help="OAuth consumer key")
        tw_parser.add_option("--consumer_secret", dest="consumer_secret", help="OAuth consumer secret")
        tw_parser.add_option("--access_token", dest="access_token", help="OAuth access token")
        tw_parser.add_option("--access_token_secret", dest="access_token_secret", help="OAuth access token secret")
        tw_parser.add_option("-T","--twitter_auth_file", dest="twitter_auth_file", help="file contains OAuth access")    
        self.add_option_group(tw_parser)
        
        blg_parser = OptionGroup(self, "Backlog Related Options")
        blg_parser.add_option("--username", dest="username", help="backlog username")
        blg_parser.add_option("--password", dest="password", help="backlog user password")
        blg_parser.add_option("--space", dest="space", help="backlog space")
        blg_parser.add_option("-p","--project", dest="project", help="backlog project to register")
        blg_parser.add_option("-B","--backlog_auth_file", dest="backlog_auth_file", help="file contains Backlog access")    
        self.add_option_group(blg_parser)
    
    @staticmethod
    def num_callback(option, opt, value, parser):
        if value < 0 :
            raise OptionValueError("%(opt)s should be larger than 0." % {"opt":opt})
        setattr(parser.values, option.dest, value)
            
def _create_parser():        
    parser = _OptionParser("usage: %prog [options]")
    parser._setup()
    return parser

def _create_config_loader(path):
    if not os.path.exists(path) :
        raise IOError(path + " not found")
    parser = SafeConfigParser()
    parser.readfp(codecs.open(path,"r","UTF-8"))    
    return parser

def find_mentions(options):
    """
    twitter から指定アカウントに対する mention を読み込む
    """    
    tz = pytz.timezone(options.timezone)
    utc = pytz.utc
    period = dict(days=options.days, hours=options.hours)
    
    end = datetime.datetime.now(tz)
    start = end - datetime.timedelta(**period)
    
    if options.twitter_auth_file :
        config = _create_config_loader(options.twitter_auth_file)
        options.consumer_key = config.get("default", "consumer_key")
        options.consumer_secret = config.get("default", "consumer_secret")
        options.access_token = config.get("default", "access_token")
        options.access_token_secret = config.get("default", "access_token_secret")            
    
    # twitter から mention を取得
    auth = tweepy.OAuthHandler(options.consumer_key, options.consumer_secret)
    auth.set_access_token(options.access_token, options.access_token_secret)
    api = tweepy.API(auth)
    mentions = []
    page = 0
    # ここの limit 回数は要検討
    page_limit = 3
    read_next = True
    
    while read_next and page < page_limit :
        timeline = api.mentions(count=100, page=page)        
        for t in timeline :
            local_created_at = utc.localize(t.created_at).astimezone(tz)        
            if local_created_at < start :
                read_next = False
                break
            t.local_created_at = local_created_at
            mentions.append(t)                        
        page = page + 1
        
    return dict(mentions=mentions,
                me=api.me(),
                start=start,
                end=end)

def create_issue(options,subject,mentions):
    """
    mention を Backlog で見やすい形式に変換して一つの課題として登録する
    """
    # テンプレートの読み込み
    tmpl_path = os.path.join(os.path.dirname(__file__), "timeline.tmpl")
    f = open(tmpl_path, "r")
    tmpl = Template(unicode(f.read(), "UTF-8"))
    f.close()
    
    # テンプレートの適用
    fmt_mentions = [ tmpl.safe_substitute({"screen_name" : x.user.screen_name,
                                           "status_text" : x.text,
                                           "status_id" : x.id,
                                           "status_created" : x.local_created_at.strftime(_DATE_FORMAT_)}) for x in mentions]

    if options.backlog_auth_file :
        config = _create_config_loader(options.backlog_auth_file)
        options.space = config.get("default", "space")
        options.username = config.get("default", "username")
        options.password = config.get("default", "password")
            
    # backlog へ登録
    backlog = Backlog(options.space, options.username, options.password)      
    project = backlog.get_project(options.project)    
    backlog.create_issue({
                          "projectId" : project.id,
                          "summary" : subject,
                          "description" : "\n".join(fmt_mentions)
                          })    

def main(argv):
            
    parser = _create_parser()
    options = parser.parse_args(argv)[0]
            
    res = find_mentions(options)
    mentions = res["mentions"]

    num = len(mentions)
    if num == 0 :
        print "No mentions were found and so no issues will be updated."
        return
    
    if not options.run :
        print "dryrun..."
                
    subject = "@%(me)s %(num)d mentions from %(start)s to %(end)s" % {"num":num, "me" : res["me"].screen_name, "start" : res["start"].strftime(_DATE_FORMAT_), "end" : res["end"].strftime(_DATE_FORMAT_)}
    print subject
    print "\n".join([x.local_created_at.strftime(_DATE_FORMAT_) + " " + x.text for x in mentions])
    
    if options.run :
        print "create issue..."
        create_issue(options, subject, mentions)

if __name__ == '__main__' :
    main(sys.argv)
