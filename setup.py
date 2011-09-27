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

from setuptools import setup

setup(name="twitter2backlog",
      version="0.0.1",
      description="a small utility to collect twitter mentions in a certain period and post them to backlog as an issue",
      author="Takashi SOMEDA",
      author_email = "someda@isenshi.com",
      url = "https://github.com/tksmd/twitter2backlog",
      platforms = "any",      
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      twitter2backlog = twitter2backlog:main
      """,
      packages=["twitter2backlog"],
      package_dir={"twitter2backlog":"src/twitter2backlog"},
      package_data={"twitter2backlog":["tmpl/*.tmpl"]},
      install_requires=["tweepy","pytz","backloglib"],
      license="Apache Licence Version 2.0",
      keywords = "backlog twitter",            
      classifiers = [
                     "Operating System :: OS Independent",
                     "Environment :: Console",
                     "Programming Language :: Python",
                     "License :: OSI Approved :: Apache Software License",
                     "Development Status :: 2 - Pre-Alpha",
                     "Intended Audience :: Developers",
                     "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
                     "Topic :: Software Development :: Libraries :: Python Modules",
                     "Topic :: Utilities" 
                     ]        
      )