"""Tests for Python scripts used for syncing content"""

import hashlib
import consolidate_media


def test_consolidate_media(tmp_path, mocker):
    """Test consolidate-media script"""

    # Scenarios to test using three modules:
    # - same filename used across modules with no sha differences
    # - same filename used across modules with all three different shas
    # - same filename with 2 modules using sha A and 1 module using sha B
    # - module unique file media file
    # - module with an unused media file

    def _create_module(module_name):
        module_dir = modules_dir / module_name
        module_dir.mkdir()
        module_cnxml = module_dir / "index.cnxml"
        module_cnxml_content = f"""
        <document xmlns="http://cnx.rice.edu/cnxml">
            <content>
                <image src="image1.jpg"/>
                <image src="image2.jpg"/>
                <image src="image3.jpg"/>
                <image src="{module_name}.jpg"/>
            </content>
        </document>
        """
        module_cnxml.write_text(module_cnxml_content)

    def _generate_sha_suffix(image_content):
        sha1 = hashlib.sha1()
        sha1.update(image_content)
        return sha1.hexdigest()[0:consolidate_media.SHA_SUFFIX_LENGTH]

    modules_dir = tmp_path / "modules"
    modules_dir.mkdir()
    media_dir = tmp_path / "media"
    media_dir.mkdir()

    module1_name = "m00001"
    module2_name = "m00002"
    module3_name = "m00003"

    _create_module(module1_name)
    _create_module(module2_name)
    _create_module(module3_name)

    (modules_dir / module1_name / f"{module1_name}.jpg").write_text(
        f"{module1_name} image"
    )
    (modules_dir / module2_name / f"{module2_name}.jpg").write_text(
        f"{module2_name} image"
    )
    (modules_dir / module3_name / f"{module3_name}.jpg").write_text(
        f"{module3_name} image"
    )

    image2_1_content = b"image2 image1"
    image2_2_content = b"image2 image2"
    image2_3_content = b"image2 image3"
    image3_1_content = b"image3 image1"
    image3_2_content = b"image3 image2"

    (modules_dir / module1_name / "image1.jpg").write_bytes(b"image1 image")
    (modules_dir / module2_name / "image1.jpg").write_bytes(b"image1 image")
    (modules_dir / module3_name / "image1.jpg").write_bytes(b"image1 image")
    (modules_dir / module1_name / "image2.jpg").write_bytes(image2_1_content)
    (modules_dir / module2_name / "image2.jpg").write_bytes(image2_2_content)
    (modules_dir / module3_name / "image2.jpg").write_bytes(image2_3_content)
    (modules_dir / module1_name / "image3.jpg").write_bytes(image3_1_content)
    (modules_dir / module2_name / "image3.jpg").write_bytes(image3_1_content)
    (modules_dir / module3_name / "image3.jpg").write_bytes(image3_2_content)
    (modules_dir / module3_name / "unused.jpg").write_bytes(b"unused")

    mocker.patch(
        "sys.argv",
        ["", modules_dir, media_dir]
    )
    consolidate_media.main()

    # All image files should be gone from modules_dir
    for mf in modules_dir.glob("**/*"):
        if mf.is_file():
            assert mf.name == "index.cnxml"

    # Confirm expected files in media dir
    assert len(list(media_dir.glob("*"))) == 10
    assert (media_dir / f"{module1_name}.jpg").exists()
    assert (media_dir / f"{module2_name}.jpg").exists()
    assert (media_dir / f"{module3_name}.jpg").exists()
    assert (media_dir / "image1.jpg").exists()
    assert not (media_dir / "image2.jpg").exists()
    assert not (media_dir / "image3.jpg").exists()
    image2_1_suffix = _generate_sha_suffix(image2_1_content)
    image2_1_name = f"image2-{image2_1_suffix}.jpg"
    image2_2_suffix = _generate_sha_suffix(image2_2_content)
    image2_2_name = f"image2-{image2_2_suffix}.jpg"
    image2_3_suffix = _generate_sha_suffix(image2_3_content)
    image2_3_name = f"image2-{image2_3_suffix}.jpg"
    image3_1_suffix = _generate_sha_suffix(image3_1_content)
    image3_1_name = f"image3-{image3_1_suffix}.jpg"
    image3_2_suffix = _generate_sha_suffix(image3_2_content)
    image3_2_name = f"image3-{image3_2_suffix}.jpg"
    assert (media_dir / image2_1_name).exists()
    assert (media_dir / image2_2_name).exists()
    assert (media_dir / image2_3_name).exists()
    assert (media_dir / image3_1_name).exists()
    assert (media_dir / image3_2_name).exists()
    assert (media_dir / "unused.jpg").exists()

    # Confirm expected CNXML content after updates
    assert (modules_dir / module1_name / "index.cnxml").read_text() == f"""
        <document xmlns="http://cnx.rice.edu/cnxml">
            <content>
                <image src="image1.jpg"/>
                <image src="{image2_1_name}"/>
                <image src="{image3_1_name}"/>
                <image src="{module1_name}.jpg"/>
            </content>
        </document>
    """.strip()

    assert (modules_dir / module2_name / "index.cnxml").read_text() == f"""
        <document xmlns="http://cnx.rice.edu/cnxml">
            <content>
                <image src="image1.jpg"/>
                <image src="{image2_2_name}"/>
                <image src="{image3_1_name}"/>
                <image src="{module2_name}.jpg"/>
            </content>
        </document>
    """.strip()

    assert (modules_dir / module3_name / "index.cnxml").read_text() == f"""
        <document xmlns="http://cnx.rice.edu/cnxml">
            <content>
                <image src="image1.jpg"/>
                <image src="{image2_3_name}"/>
                <image src="{image3_2_name}"/>
                <image src="{module3_name}.jpg"/>
            </content>
        </document>
    """.strip()
