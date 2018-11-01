#!/usr/bin/env python3


from ast import literal_eval
from subprocess import Popen, PIPE, STDOUT

import hashlib
import json
import os.path
import shlex
import subprocess
import sys

binstub = "bandit3"
include_paths = ["."]

# severity converts the severity of a bandit issue
# to the severity accepted by CodeClimate
def severity(sev):
  if sev == "HIGH":
    return "major"
  if sev == "MEDIUM":
    return "minor"
  if sev == "LOW":
    return "info"

if os.path.exists("/config.json"):
  contents = open("/config.json").read()
  config = json.loads(contents)

