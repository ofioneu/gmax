call python-3.7.3-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

call py -m venv venv
cd venv/Scripts/
call activate.bat
cd ..
cd ..

call py get-pip.py

call pip install -r requiriments.txt

call py install.py