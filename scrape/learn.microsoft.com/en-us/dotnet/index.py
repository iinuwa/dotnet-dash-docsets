#!/usr/bin/python3
from lxml.html import html5parser
from pathlib import Path

# import re
import sqlite3


conn = sqlite3.connect("docset.db")
cur = conn.cursor()

folder = Path("./api-slim")
# pat = re.compile(r"(\w+)</h1>")
sql = "INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (:name, :type, :path)"
for p in folder.iterdir():
    doc = html5parser.parse(str(p))
    h1 = doc.getroot().find(".//h1", namespaces={"": "http://www.w3.org/1999/xhtml"})
    if h1 is None:
        print(f"h1 not found for {p}")
        continue
    [name, doc_type] = h1.xpath("string()").rsplit(" ", 1)
    doc_type = 'Constructor' if doc_type == 'Constructors' else doc_type
    path = f"dotnet/api/{p.name}"
    cur.execute(sql, {"name": name, "type": doc_type, "path": path})
    # print(name, doc_type, path)
    # with open(p) as file:
    #     for line in file:
    #         match = pat.search(line)
    #         if match:
    #             doc_type = match.group(1)
    #            cur.execute(sql, [name, doc_type, path])
conn.commit()
cur.close()
conn.close()
