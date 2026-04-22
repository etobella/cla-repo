import yaml
import sys
import os
import re


MAIL_PATTERN_REGEX = re.compile(r"<([a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*)>")
DOMAIN_PATTERN_REGEX = re.compile(r"[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@([a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*)")

if __name__ == "__main__":
    corporates = []
    individuals = []
    not_found = []
    path, authors, = sys.argv[1:]
    for dirpath, _dirnames, filenames in os.walk(os.path.join(path, "corporate")):
        for filename in filenames:
            with open(os.path.join(dirpath, filename), "r") as f:
                corporate = yaml.safe_load(f)
                corporates += corporate.get("domain", [])
    for dirpath, _dirnames, filenames in os.walk(os.path.join(path, "individual")):
        for filename in filenames:
            with open(os.path.join(dirpath, filename), "r") as f:
                individual = yaml.safe_load(f)
                individuals += individual.get("email", [])
    for author in authors.splitlines():
        email = MAIL_PATTERN_REGEX.search(author)
        if email:
            email = email.group(1)
            if email in individuals:
                continue
            domain = DOMAIN_PATTERN_REGEX.search(email)
            if domain:
                domain = domain.group(1)
                if domain in corporates:
                    continue
        not_found.append(author)
    if not_found:
        print(",".join(not_found))