:: -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
pip config set global.index-url http://mirrors.aliyun.com/pypi/simple/
pip config set install.trusted-host mirrors.aliyun.com

python.exe -m pip install --upgrade pip

::pip --default-timeout=600 install -U pip
pip --default-timeout=600 install redis
pip --default-timeout=600 install pywin32
pip --default-timeout=600 install pandas==2.0.3
pip --default-timeout=600 install easytrader
pip --default-timeout=600 install easyquotation
pip --default-timeout=600 install -U chinesecalendar
pip --default-timeout=600 install pytesseract
pip install numpy==1.26.4

pause
