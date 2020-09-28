slug=$1
meta="metadata/${slug}.metadata.json"
collection="collections/${slug}.collection.xml"
version=$(cat "$meta" | jq -r .version)
legacy_id=$(cat "$meta" | jq -r .legacy_id)
out_dir="${legacy_id}_1.${version}"
mkdir "$out_dir"
cp -r "$(pwd)/$collection" "${out_dir}/collection.xml"
cp -r "$(pwd)/$meta" "${out_dir}/metadata.json"
for module in $(find ./modules/ -mindepth 1 -maxdepth 1); do
  cp -r "$(pwd)/${module#./}" "$out_dir/$(basename $module)"
done
