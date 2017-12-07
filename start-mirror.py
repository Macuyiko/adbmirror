import subprocess
import re
from time import time
from PIL import ImageTk, Image
from io import BytesIO
from os.path import isfile
from os import remove, mkdir
from shutil import copyfile, rmtree, copy
from adb import *


if __name__ == '__main__':
	abi = run_adb('shell getprop ro.product.cpu.abi', as_str=True).strip()
	sdk = run_adb('shell getprop ro.build.version.sdk', as_str=True).strip()
	rel = run_adb('shell getprop ro.build.version.release', as_str=True).strip()
	dev_size = run_adb('shell wm size', as_str=True).strip()
	mtch = re.search(r"(\d+x\d+)", dev_size)
	dev_size = mtch.group(1)

	print('Device info:', abi, sdk, rel, dev_size)

	dev_dir = '/data/local/tmp/adbmirror/'

	minicap = 'bin/minicap/{}/minicap'.format(abi)
	minitouch = 'bin/minitouch/{}/minitouch'.format(abi)
	minicap_shared = 'bin/minicap-shared/android-{}/{}/minicap.so'.format(rel, abi)
	if not isfile(minicap_shared):
		minicap_shared = 'bin/minicap-shared/android-{}/{}/minicap.so'.format(sdk, abi)

	print('Now pushing files')
	run_adb('push {} {}'.format(minicap, dev_dir), as_str=True, print_out=True)
	run_adb('push {} {}'.format(minitouch, dev_dir), as_str=True, print_out=True)
	run_adb('push {} {}'.format(minicap_shared, dev_dir), as_str=True, print_out=True)

	run_adb('shell chmod 0777 {}*'.format(dev_dir), as_str=True, print_out=True)

	run_adb('forward tcp:1313 localabstract:minicap', as_str=True, print_out=True)
	run_adb('forward tcp:1111 localabstract:minitouch', as_str=True, print_out=True)

	print('Now ready to start GUI, press ENTER when done for cleanup')
	print('Example command:')
	print('python gui.py {} {} {}'.format('540x960', dev_size, dev_dir))
	input()

	run_adb('shell killall minicap', as_str=True, print_out=True)
	run_adb('shell killall minitouch', as_str=True, print_out=True)
	run_adb('shell rm {}*'.format(dev_dir), as_str=True, print_out=True)
