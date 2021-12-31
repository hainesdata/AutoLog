py2applet --make-setup AutoLog.py
rm -rf build dist
python3 setup.py py2app -A
