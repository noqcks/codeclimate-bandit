#!/usr/bin/env python3

import json
import os.path
import shlex
import sys

from ast import literal_eval
from subprocess import Popen, PIPE, STDOUT
import subprocess

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

    # set python version
    if config["config"].get("python_version"):
        version = config["config"].get("python_version")
        if version == "2" or version == 2:
            binstub = "bandit2"
        elif version != "3" and version != 3:
            sys.exit("Invalid python_version; must be either 2 or 3")

    # set included paths
    if config.get("include_paths"):
      include_paths = config.get("include_paths", ["."])
      include_paths = [shlex.quote(path) for path in include_paths if os.path.  isdir(path) or path.endswith(".py")]

if len(include_paths) > 0:
  included_paths = " ".join(include_paths)
  cmd = f"{binstub} -r {included_paths} -f json"

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
      "fingerprint": result["test_id"],
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
