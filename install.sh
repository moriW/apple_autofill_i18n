#! /bin/bash

echo "安装&下载python所需依赖文件"
pip3 install selenium
curl https://chromedriver.storage.googleapis.com/88.0.4324.96/chromedriver_mac64.zip -o ~/Downloads/chromedriver_mac64.zip
echo "解压驱动"
unzip ~/Downloads/chromedriver_mac64.zip -d ~/Downloads
rm ~/Downloads/chromedriver_mac64.zip
echo "安装驱动"
mv ~/Downloads/chromedriver /usr/local/bin/chromedriver
curl https://raw.githubusercontent.com/moriW/apple_autofill_i18n/master/main.py -o /usr/local/bin/apple_auto_fill
echo "安装自动脚本"
chmod a+x /usr/local/bin/apple_auto_fill
