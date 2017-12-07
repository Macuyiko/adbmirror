import subprocess

ADBBIN = 'adb.exe'

def run_adb(arguments, clean=False, as_str=False, print_out=False, out_file=None):
	if type(arguments) == str:
		arguments = arguments.split(' ')
	result = subprocess.run([ADBBIN] + arguments, stdout=subprocess.PIPE)
	stdout = result.stdout
	if clean:
		stdout = stdout.replace(b'\r\n', b'\n')
	if as_str:
		stdout = stdout.decode("utf-8")
	if print_out:
		print(stdout)
	if out_file:
		mode = 'w' if as_str else 'wb'
		with open(out_file, mode) as file:
			file.write(stdout)
	return stdout

