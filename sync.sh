#!/usr/bin/env bash
set -xeo pipefail
rm -f module-ids canonical-modules
while read slug collid
do
  rm -rf ./"$slug"
  neb get -r -d $slug staging $collid latest
  echo "--- $slug" >> module-ids
  find "./$slug/" -maxdepth 1 -mindepth 1 -type d | xargs -I{} basename {}  >> module-ids
done < archive-syncfile
python find-module-canonical.py > canonical-modules
rm -rf modules collections metadata
mkdir modules collections metadata
cat canonical-modules | awk '{ print "cp -r "$1"/"$2" modules/"; }' | xargs -I {} bash -c '{}'
while read slug collid
do
  mv "$slug/collection.xml" "collections/$slug.collection.xml"
  mv "$slug/metadata.json" "metadata/$slug.metadata.json"
  rm -rf ./"$slug"
done < archive-syncfile
echo 'Done.'