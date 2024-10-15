#!/usr/bin/python3
from lxml.etree import tostring
from lxml.html import html5parser
from pathlib import Path
import re
import textwrap

LINK_PATTERN = re.compile(rb'href="(.+?)%3Fview=.+?\.html')


def foo(in_path, out_path):
    tree = html5parser.parse(in_path)
    root = tree.getroot()
    head = root.find("{http://www.w3.org/1999/xhtml}head")
    title = head.find("{http://www.w3.org/1999/xhtml}title").text

    with open(out_path, "wb") as file:
        file.write(
            textwrap.dedent(f"""\
        <!DOCTYPE html>
        <html
          class="hasSidebar hasPageActions hasBreadcrumb reference reference has-default-focus theme-light"
          lang="en-us"
          dir="ltr"
          data-authenticated="false"
          data-auth-status-determined="false"
          data-target="docs"
          x-ms-format-detection="none"
        >
          <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <link rel="stylesheet" href="../../../static/assets/0.4.028395994/styles/site-ltr.css">
            <title>{title}</title>
          </head>
          <body>
            <div class="mainContainer  uhf-container has-default-focus" data-bi-name="body"><div class="columns has-large-gaps is-gapless-mobile">
              <section class="primary-holder column is-two-thirds-tablet is-three-quarters-desktop">
                <div class="columns is-gapless-mobile has-large-gaps"><div id="main-column" class="column is-full is-8-desktop">
                  <main id="main" class="" role="main" data-bi-name="content" lang="en-us" dir="ltr">
        """).encode("utf-8")
        )

        body = root.find("{http://www.w3.org/1999/xhtml}body")
        main_container = body.getchildren()[1]
        columns = main_container.getchildren()[0]
        main_section = columns.getchildren()[2]
        main = main_section.getchildren()[1].getchildren()[0].getchildren()[0]
        content = main.getchildren()[5]
        # Remove feedback button
        # content.remove(content.getchildren()[3])
        ns_map = {"": "http://www.w3.org/1999/xhtml"}
        el = content.find(
            'div/div[@id="user-feedback"]/..',
            namespaces=ns_map,
        )
        el.getparent().remove(el)
        # content.remove(el)
        # Remove non-C# code
        # TODO: Re-implement tabular interface for code examples
        for lang in ["cpp", "fsharp", "vb"]:
            non_cs_code = tree.findall(
                f".//pre/code[@class='{lang} lang-{lang}']/..",
                namespaces=ns_map,
            ) + tree.findall(
                f".//pre/code[@class='lang-{lang}']/..",
                namespaces=ns_map,
            )
            for e in non_cs_code:
                e.getparent().remove(e)

        docs = (
            tostring(content, method="html")
            .replace(b"html:", b"")
            .replace(b' xmlns:html="http://www.w3.org/1999/xhtml"', b"")
        )
        # remove query parameters from relative links
        docs = LINK_PATTERN.sub(rb'href="\1.html', docs)

        file.write(docs)
        # file_contents += docs

        # file_contents += b"</main></div></div></section></div></body></html>"
        file.write(b"</main></div></div></section></div></body></html>")


out_dir = Path("./api-slim")
out_dir.mkdir(exist_ok=True)
in_dir = Path("./api")
PATH_PATTERN = re.compile(r"(.+?)\?view=.+?\.html$")
print("trimming files...")
for path in in_dir.iterdir():
    out_filename = PATH_PATTERN.sub(r"\1.html", path.name)
    out_path = out_dir / out_filename
    # print(f"Writing {path} to {out_path}")
    try:
        foo(str(path), out_path)
    except Exception as ex:
        print(f"Error processing {path}: {ex}")
