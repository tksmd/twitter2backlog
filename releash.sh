#!/bin/bash
#
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
#
# リリース作業用のシェル
# - git のタグ付け
# - pypi の更新
#
if [ $# -lt 1 ]; then
  echo "$0 <VERSION>"
  exit 1
fi
Version=$1

if [ $(git status . | wc -l) -gt 0 ]; then
  echo -n "modified items exist, continue ? [y|n] "
  while read ans
  do
    case ${ans} in
	    "y"|"Y")
	      echo "ok continue..."
	      break
	    ;;
	    "n"|"N")
	      exit 1
	    ;;
	    *)
	      echo "please answer y or n"
	    ;;
    esac 
  done
fi

# (1) タグ付け
git tag -a "${Version}"
git push --tags

# (2) pypi の更新
python setup.py register
python setup.py sdist upload
