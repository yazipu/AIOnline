%~d0
cd /d "%~dp0"

pip --default-timeout=600 install okx
pip --default-timeout=600 install python-okx
pip --default-timeout=600 install python-binance
pip --default-timeout=600 install python-bitget

pause