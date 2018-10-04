# modified from
# https://github.com/rubik/radon/blob/b73c279acc321158c0b089b941e12a129daa9429/codeclimate-radon

import json
import os.path
import shlex
import sys

from ast import literal_eval
from subprocess import Popen, PIPE, STDOUT
import subprocess

include_paths = ["."]

if os.path.exists("/config.json"):
    contents = open("/config.json").read()
    config = json.loads(contents)

    if config.get("include_paths"):
        config_paths = config.get("include_paths")
        python_paths = []
        for i in config_paths:
            ext = os.path.splitext(i)[1]
            if os.path.isdir(i) or "py" in ext:
                python_paths.append(i)
        include_paths = python_paths

    include_paths = config.get("include_paths", ["."])
    include_paths = [shlex.quote(path) for path in include_paths
                     if os.path.isdir(path) or path.endswith(".py")]

if len(include_paths) > 0:
    paths = " ".join(include_paths)
    cmd = f"bandit -r {paths} -f json"
    ret = subprocess.run([cmd], stdout=subprocess.PIPE, shell=True)
    res = literal_eval(ret.stdout.decode('utf8'))
    for res in res["results"]:
      dict = {
        "type": "issue",
        "check_name": res["test_id"] + ": " + res["issue_text"],
        "description": res["more_info"],
        "categories": ["Security"],
        "location": {
          "path": res["filename"],
          "lines": {
            "begin": min(res["line_range"]),
            "end": max(res["line_range"])
          }
        }
      }
      print(json.dumps(dict) + '\0')
else:
    print("Empty workspace; skipping...", file = sys.stderr)
