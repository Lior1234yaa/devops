#!/usr/bin/env python3
import argparse, os, sys, requests, statistics
from collections import Counter

def norm_type(s):
    s = (s or "").strip().lower().replace("_","").replace(" ", "")
    if s in ("show","s"): return "show"
    if s in ("averageage","average","avg","a"): return "average"
    if s in ("commoncountry","country","common","c"): return "common"
    raise ValueError("TYPE must be: Show / Average Age / Common Country")

def fetch(n):
    import requests
    r = requests.get(f"https://randomuser.me/api/?results={n}", timeout=30)
    r.raise_for_status()
    return r.json()["results"]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--type", default=os.getenv("TYPE", "Show"))
    p.add_argument("--count", type=int, default=int(os.getenv("NUMBER_OF_USERS","10")))
    a = p.parse_args()

    t = norm_type(a.type)
    n = a.count
    if not (1 <= n <= 300):
        print("NUMBER_OF_USERS must be 1..300", file=sys.stderr); sys.exit(2)

    users = fetch(n)
    rows = [{"name": f"{u['name']['first']} {u['name']['last']}",
             "age": int(u['dob']['age']),
             "country": u['location']['country']} for u in users]

    if t == "show":
        print("NAME | AGE | COUNTRY"); print("-"*40)
        for r in rows: print(f"{r['name']} | {r['age']} | {r['country']}")
    elif t == "average":
        print(round(statistics.mean(r["age"] for r in rows), 2))
    elif t == "common":
        for c, cnt in Counter(r["country"] for r in rows).most_common():
            print(f"{c}: {cnt}")

if __name__ == "__main__":
    main()
