slug=$1
meta="./metadata/${slug}.metadata.json"
collection="./collections/${slug}.collection.xml"
version=$(cat "$meta" | jq -r .version)
legacy_id=$(cat "$meta" | jq -r .legacy_id)
cp -r $collection "./modules/collection.xml"
cp -r $meta "./modules/metadata.json"
