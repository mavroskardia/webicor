rm -f webicor.gz
pushd .
cd ..
find -type d -iname node_modules -exec rm -rf {} \;
find -type d -iname bower_components -exec rm -rf {} \;
rm -rf webicor/static/
tar cfz deploy/webicor.gz webicor/
popd

pushd .
cd base
docker build -t webicorbase .
popd

docker build -t webicor .

echo "All built. Now execute run.sh"
