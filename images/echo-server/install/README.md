pip3 install pip-tools
pip-compile --generate-hashes --output-file=install/requirements.txt --strip-extras install/requirements.in
pip3 install --require-hashes -r requirements.txt