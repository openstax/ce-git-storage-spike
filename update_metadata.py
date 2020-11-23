"""Update metadata in repository during content sync"""

import sys
from pathlib import Path
from lxml import etree

METADATA_ACCEPT_TAGS = [
    "{http://cnx.rice.edu/mdml}title",
    "{http://cnx.rice.edu/mdml}abstract",
    "{http://cnx.rice.edu/mdml}content-id"
]


def filter_accepted_tags(cnxml_doc, accept_tags):
    """Remove metadata fields based upon an accepted tags list"""
    metadata = cnxml_doc.xpath(
        "//x:metadata",
        namespaces={"x": "http://cnx.rice.edu/cnxml"}
    )[0]

    for elem in metadata:
        if elem.tag not in accept_tags:
            metadata.remove(elem)


def main():
    modules_dir = Path(sys.argv[1]).resolve(strict=True)

    cnxml_files = [
        cf for cf in modules_dir.glob("**/*")
        if cf.is_file() and cf.name == "index.cnxml"
    ]

    for cnxml_file in cnxml_files:
        cnxml_doc = etree.parse(str(cnxml_file))
        filter_accepted_tags(cnxml_doc, METADATA_ACCEPT_TAGS)

        with open(cnxml_file, "wb") as f:
            cnxml_doc.write(f, encoding="utf-8", xml_declaration=False)


if __name__ == "__main__":
    main()
