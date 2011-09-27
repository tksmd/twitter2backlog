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

import unittest
import os
from test import test_support

import twitter2backlog

class OptionParserTest(unittest.TestCase):
    
    def testCreateParser1(self):
        """
        引数なしのテスト時のデフォルト値
        """
        parser = twitter2backlog._create_parser()
        args = []
        (options,optargs) = parser.parse_args(args)
        self.assertEqual(0, options.hours)
        self.assertEqual(1, options.days)
        self.assertEquals(False, options.run)
        self.assertEquals("Asia/Tokyo",options.timezone)
        self.assertEquals("@%(me)s %(num)d mentions from %(start)s to %(end)s", options.summary)        
        for k,v in options.__dict__.iteritems() :
            if k not in ["hours","days","run","timezone", "summary"] :
                self.assertFalse(v)        
        self.assertEquals(0,len(optargs))

    def testCreateParser2(self):
        """
        数値のテスト
        """
        parser = twitter2backlog._create_parser()
        args = ["--hours","3","--days","2"]
        (options,optargs) = parser.parse_args(args)
        self.assertEqual(3, options.hours)
        self.assertEqual(2, options.days)
        self.assertEquals(False, options.run)
        self.assertEquals("Asia/Tokyo",options.timezone)
        self.assertEquals("@%(me)s %(num)d mentions from %(start)s to %(end)s", options.summary)
        for k,v in options.__dict__.iteritems() :
            if k not in ["hours","days","run","timezone","summary"] :
                self.assertFalse(v)        
        self.assertEquals(0,len(optargs))        
                    
    def testCreateParser3(self):
        """
        twitter の設定のテスト
        """
        parser = twitter2backlog._create_parser()
        args = ["--consumer_key","key","--consumer_secret","secret2","--access_token","token","--access_token_secret","secret2"]
        (options,optargs) = parser.parse_args(args)
        self.assertEqual(0, options.hours)
        self.assertEqual(1, options.days)
        self.assertEquals(False, options.run)
        self.assertEquals("Asia/Tokyo",options.timezone)
        self.assertEquals("@%(me)s %(num)d mentions from %(start)s to %(end)s", options.summary)        
        self.assertEquals(0,len(optargs))
        
    def testCreateParser4(self):
        """
        文字列の設定のテスト
        """
        parser = twitter2backlog._create_parser()
        args = ["--summary",u"Twitter から @%(me)s 宛に %(num)d 件の mentions がありました [%(start)s - %(end)s]"]
        (options,optargs) = parser.parse_args(args)
        self.assertEqual(0, options.hours)
        self.assertEqual(1, options.days)
        self.assertEquals(False, options.run)
        self.assertEquals("Asia/Tokyo",options.timezone)
        self.assertEquals(u"Twitter から @%(me)s 宛に %(num)d 件の mentions がありました [%(start)s - %(end)s]", options.summary)                
        self.assertEquals(0,len(optargs))        


class Twitter2BacklogTest(unittest.TestCase):
            
    def testMain1(self):        
        twitter_auth_file = os.path.join(os.path.dirname(__file__),"test_twitter.cfg")
        backlog_auth_file = os.path.join(os.path.dirname(__file__),"test_backlog.cfg")        
        args = ["-D","2","-r",
                "-T",twitter_auth_file,
                "-B",backlog_auth_file,
                "-p","TEST",
                "--summary",u"@%(me)s 宛に %(num)d 件の言及がありました [%(start)s - %(end)s]"]
        twitter2backlog.main(args)

def test_main():
    test_support.run_unittest(OptionParserTest,
                              Twitter2BacklogTest)
        
if __name__ == '__main__' :
    test_main()
