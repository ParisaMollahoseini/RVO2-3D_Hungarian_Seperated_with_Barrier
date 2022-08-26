#!/bin/bash

pip3 install -r requirements.txt

rm -rf ./Release

mkdir ./Release

cd ./Release

cmake -DCMAKE_BUILD_TYPE=Release ..

make

cp -r ../after_create_release/* ./examples

python3 ./examples/get_input/app.py 
