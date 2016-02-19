echo -n "Removing old app zip..."
rm -f webicor.gz
echo "done"

echo -n "Removing generated data..."
pushd . > /dev/null
cd ..
find -type d -iname node_modules -exec rm -rf {} \; 2>&1 > /dev/null
find -type d -iname bower_components -exec rm -rf {} \; 2>&1 > /dev/null
rm -rf webicor/static/ 2>&1 > /dev/null
echo "done"
echo -n "Compressing webicor..."
tar cfz deploy/webicor.gz webicor/
popd > /dev/null
echo "done"

echo -n "Removing old/building new webicorbase..."
pushd . > /dev/null
cd base
docker rmi webicorbase 2>&1 > /dev/null
docker build -t webicorbase . > /dev/null
popd > /dev/null
echo "done"

echo -n "Removing old/building new webicor..."
docker rmi webicor 2>&1 > /dev/null
docker build -t webicor . > /dev/null
echo "done"

echo "All built. Now execute run.sh"
