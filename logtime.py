import git
from pydriller import RepositoryMining
import sys
import datetime
import re
from pprint import pprint
import subprocess
from collections import Counter

HOURS = 8
current_user = subprocess.check_output(["git", "config", "user.name"]).decode().strip()
print("Checking for:", current_user)
issue_regex = re.compile('AA\-\d+')
today = datetime.datetime.now()
cutoff = today - datetime.timedelta(days=21)
g = RepositoryMining(sys.argv[1], only_authors=[current_user], since=cutoff, reversed_order=True)
last_date, last_time = None, None
stack = Counter()
for commit in g.traverse_commits():
    current_date = commit.author_date.date()
    #maybe use time since last commit?
    task_duration = None
    if last_date and last_date != current_date:
        print(last_date.ctime())
        total = len(list(stack.elements()))
        for msg, count in stack.items():
            print("%dh %s" % (count / total * HOURS, msg))
        stack = Counter()
    else:
        if last_time:
            task_duration = commit.author_date - last_time
    stack.update(issue_regex.findall(commit.msg) or [commit.msg.split("\n")[0]])
    last_date = current_date
    last_time = commit.author_date

