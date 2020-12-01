"""Update metadata in repository during content sync"""

import sys
import json
from pathlib import Path
from lxml import etree


NS_MDML = "http://cnx.rice.edu/mdml"
NS_CNXML = "http://cnx.rice.edu/cnxml"
METADATA_ACCEPT_TAGS = [
    f"{{{NS_MDML}}}title",
    f"{{{NS_MDML}}}abstract",
    f"{{{NS_MDML}}}content-id"
]
METADATA_ADDED_TAGS_FROM_JSON = {
    "id": "uuid",
    "canonical": "canonical-book-uuid"
}


def filter_accepted_tags(cnxml_doc, accept_tags):
    """Remove metadata fields based upon an accepted tags list"""
    metadata = cnxml_doc.xpath(
        "//x:metadata",
        namespaces={"x": NS_CNXML}
    )[0]

    for elem in metadata:
        if elem.tag not in accept_tags:
            metadata.remove(elem)


def add_metadata_from_json(cnxml_doc, metadata_json, added_tags):
    metadata = cnxml_doc.xpath(
        "//x:metadata",
        namespaces={"x": NS_CNXML}
    )[0]

    for from_key, to_tag in added_tags.items():
        value = metadata_json[from_key]
        element = etree.Element(f"{{{NS_MDML}}}{to_tag}")
        element.text = value
        element.tail = "\n"
        metadata.append(element)


def main():
    modules_dir = Path(sys.argv[1]).resolve(strict=True)

    module_files = [
        (
            cf.resolve(strict=True),
            (cf / ".." / "metadata.json").resolve(strict=True)
        )
        for cf in modules_dir.glob("**/*")
        if cf.is_file() and cf.name == "index.cnxml"
    ]

    for cnxml_file, metadata_file in module_files:
        cnxml_doc = etree.parse(str(cnxml_file))
        metadata_json = json.load(metadata_file.open())

        filter_accepted_tags(cnxml_doc, METADATA_ACCEPT_TAGS)
        add_metadata_from_json(cnxml_doc, metadata_json, METADATA_ADDED_TAGS_FROM_JSON)

        with open(cnxml_file, "wb") as f:
            cnxml_doc.write(f, encoding="utf-8", xml_declaration=False)


if __name__ == "__main__":
    main()
