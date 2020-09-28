slug=$1
meta="metadata/${slug}.metadata.json"
collection="collections/${slug}.collection.xml"
version=$(cat "$meta" | jq -r .version)
legacy_id=$(cat "$meta" | jq -r .legacy_id)
parent_dir="/tmp/ce-git-storage-spike/${legacy_id}/fetched-book/${legacy_id}"
approved_slugs="https://raw.githubusercontent.com/openstax/content-manager-approved-books/master/book-slugs.json"
out_dir="${parent_dir}/raw"
mkdir -p "$out_dir"
wget $approved_slugs -O "${parent_dir}/book-slugs.json"
cp -r "$(pwd)/$collection" "${out_dir}/collection.xml"
cp -r "$(pwd)/$meta" "${out_dir}/metadata.json"
for module in $(find ./modules/ -mindepth 1 -maxdepth 1); do
  cp -r "$(pwd)/${module#./}" "$out_dir/$(basename $module)"
done
