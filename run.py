#!/usr/bin/env python3


from ast import literal_eval
from subprocess import Popen, PIPE, STDOUT

import hashlib
import json
import os.path
import shlex
import subprocess
import sys

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

  # set included paths
  if config.get("include_paths"):
    include_paths = config.get("include_paths", ["."])
    include_paths = [shlex.quote(path) for path in include_paths if os.path.  isdir(path) or path.endswith(".py")]

if len(include_paths) > 0:
  included_paths = " ".join(include_paths)
  cmd = f"bandit -r {included_paths} -f json"

  if os.path.exists("/code/.bandit.yaml"):
    cmd = cmd + f" -c /code/.bandit.yaml"

  output = subprocess.run([cmd], stdout=subprocess.PIPE, shell=True)
  output = literal_eval(output.stdout.decode('utf8'))

  for result in output["results"]:
    dict = {
      "type": "issue",
      "check_name": result["test_name"],
      "description": result["issue_text"],
      "categories": ["Security"],
      "severity": severity(result["issue_severity"]),
      "fingerprint": hashlib.md5((result["test_id"] + result['filename'] + result['code']).encode('utf-8')).hexdigest(),
      "location": {
        "path": result["filename"],
        "lines": {
          "begin": min(result["line_range"]),
          "end": max(result["line_range"])
        }
      }
    }
    print(json.dumps(dict) + '\0')
else:
  print("Empty workspace; skipping...", file = sys.stderr)
