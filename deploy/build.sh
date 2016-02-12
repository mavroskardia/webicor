rm -f webicor.gz
pushd .
cd ..
tar cfz deploy/webicor.gz webicor/
popd

pushd .
cd base
docker build -t webicorbase .
popd

docker build -t webicor .

echo "All built. Now execute run.sh"
