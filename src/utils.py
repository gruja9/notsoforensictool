import os
import hashlib
from datetime import datetime
import textwrap

try:
	import PyPDF2
	import psutil
	import platform
	from reportlab.pdfgen import canvas
except ModuleNotFoundError:
	print("Du har inte alla moduler installerade!")
	ask = input("Skulle du vilja installera dem? (y/n): ")
	if ask.lower() == 'y':
		os.system("/usr/bin/pip3 install PyPDF2 psutil reportlab")
		import PyPDF2
		import psutil
		import platform
		from reportlab.pdfgen import canvas
	else:
		exit()


ENCRYPTION_KEY = {
		'a':'P',
		'b':'m',
		'c':'e',
		'd':'!',
		'e':'S',
		'f':'a',
		'g':'X',
		'h':'?',
		'i':'7',
		'j':'w',
		'k':'C',
		'l':'3',
		'm':'G',
		'n':'&',
		'o':'b',
		'p':'d',
		'q':'M',
		'r':'D',
		's':'x',
		't':'9',
		'u':'n',
		'v':'B',
		'w':'g',
		'x':'A',
		'y':'c',
		'z':'E',
		'A':'W',
		'B':'f',
		'C':'L',
		'D':'I',
		'E':'O',
		'F':'q',
		'G':'U',
		'H':'+',
		'I':'h',
		'J':'l',
		'K':'Q',
		'L':'T',
		'M':'0',
		'N':'t',
		'O':'R',
		'P':'2',
		'Q':'j',
		'R':'8',
		'S':'V',
		'T':'r',
		'U':'1',
		'V':'k',
		'X':'v',
		'Y':'z',
		'Z':'4',
		'0':'u',
		'1':'N',
		'2':'o',
		'3':'F',
		'4':'y',
		'5':'K',
		'6':'p',
		'7':'Y',
		'8':'H',
		'9':'s',
		}

def find_all_files(folder):		# Sök efter alla filer i en katalog
	all_files = list()

	for root, dirs, dir_files in os.walk(folder):
		for files in dir_files:
			all_files.append(os.path.join(root, files))

	return all_files

def find_specific_files(folder, extension):		# Sök efter alla filer med viss filändelse i en katalog
	all_specific_files = list()
	all_files = find_all_files(folder)

	for files in all_files:
		if files[-3:] == extension:
			all_specific_files.append(files)

	return all_specific_files

def search_files(folder, extension, keyword):	# Sok efter viss information i en viss filtyp i en katalog
	all_matching_files = list()
	all_files = find_specific_files(folder, extension)

	for files in all_files:

		if extension == 'txt':
			with open(files, 'r') as finput:
				for lines in finput:
					if keyword.lower() in lines.lower():
						all_matching_files.append(files)
						break

		elif extension == 'pdf':
			pdffile = PyPDF2.PdfFileReader(files)
			pdf_pages = pdffile.getNumPages()
			for page in range(0, pdf_pages):
				pdf_page = pdffile.getPage(page)
				pdf_text = pdf_page.extractText()
				if keyword.lower() in pdf_text.lower():
					all_matching_files.append(files)
					break

	return all_matching_files

def find_modified_files(folder, date):		# Sök efter filer modifierade senast ett visst datum
	all_modified_files = list()
	date = datetime.strptime(date, '%Y-%m-%d').date()
	all_files = find_all_files(folder)

	for files in all_files:
		file_timestamp = os.stat(files).st_mtime
		file_date = datetime.fromtimestamp(file_timestamp).date()
		if file_date <= date:
			all_modified_files.append(files)

	return all_modified_files

def encrypt_file(filename):		# Kryptera en fil
	filename_enc = filename + '.enc'
	with open(filename, 'r') as finput:
		with open(filename_enc, 'w') as foutput:
			for line in finput:
				line = line.strip()
				line_enc = ""
				for char in line:
					if char in ENCRYPTION_KEY.keys():
						char_enc = ENCRYPTION_KEY[char]
					line_enc += char_enc 
				foutput.write(line_enc + '\n')
	return filename_enc


def decrypt_file(filename):		# Dekryptera en fil
	filename_dec = filename[:-4]
	with open(filename, 'r') as finput:
		with open(filename_dec, 'w') as foutput:
			for line in finput:
				line = line.strip()
				line_dec = ""
				for char in line:
					for key, value in ENCRYPTION_KEY.items():
						if char == value:
							char_dec = key
							break
					line_dec += char_dec

				foutput.write(line_dec + '\n')
	return filename_dec

def word_difference(filename1, filename2):	# Ta fram skillnad mellan två filer
	file1_set = set()
	file2_set = set()

	with open(filename1, 'r') as file1:
		for line in file1:
			words = line.strip().split()
			for word in words:
				file1_set.add(word)

	with open(filename2, 'r') as file2:
		for line in file2:
			words = line.strip().split()
			for word in words:
				file2_set.add(word)

	file1_unique = file1_set - file2_set
	file2_unique = file2_set - file1_set

	return file1_unique, file2_unique

def get_size(byte):		# Få storleken anpassad för människor
	delimiter = 1024
	for unit in ['', 'K', "M", 'G', 'T']:
		if byte < delimiter:
			return f"{byte:.2f} {unit}B"
		byte /= delimiter

def system_information():
	results = list()

	#System Software Information
	systeminfo = platform.uname()
	names = ['System: ', 'Node: ', 'Release: ', 'Version: ', 'Machine: ', 'Processor: ']
	results.append('='*30 + "System Information" + '='*30)
	for name, info in zip(names, systeminfo):
		results.append(name + info)
	results.append('')

	#CPU Information
	if systeminfo.system.lower() == 'linux':
		cpuinfo_name = ' '.join(os.popen('lscpu | grep "Model name"').read().split()[2:])
	else:
		cpuinfo_name = ''
	cpuinfo_freq = psutil.cpu_freq()
	results.append('='*30 + 'CPU Information' + '='*30)
	results.append("Processor Name: " + cpuinfo_name)
	results.append("Physical Cores: " + str(psutil.cpu_count(logical=False)))
	results.append("Logical Cores: " + str(psutil.cpu_count(logical=True)))
	results.append(f"Min Frequncy: %.2f Mhz" % cpuinfo_freq.min)
	results.append(f"Max Frequncy: %.2f Mhz" % cpuinfo_freq.max)
	results.append(f"Current Frequncy: %.2f Mhz" % cpuinfo_freq.current)
	results.append("CPU Usage Per Cores:")
	for i, perc in enumerate(psutil.cpu_percent(percpu=True)):
		results.append(f"CPU {i+1}: {perc}%")
	results.append("Total Usage: {}%".format(psutil.cpu_percent()))
	results.append('')

	#GPU Information	
	results.append('='*30 + 'GPU Information' +'='*30)
	if systeminfo.system.lower() == 'linux':
		for i, gpu in enumerate(os.popen('lspci | grep VGA | cut -d ":" -f3').read().strip().split('\n')):
			results.append(f"Graphical Adapter Name {i+1}: {gpu.strip()}")
	results.append('')
	
	#Memory Information
	meminfo = psutil.virtual_memory()
	meminfo_swap = psutil.swap_memory()
	results.append('='*30 + 'Memory Information' + '='*30)
	results.append("Total Memory: " + get_size(meminfo.total))
	results.append("Available Memory: " + get_size(meminfo.available))
	results.append("Used Memory: " + get_size(meminfo.used))
	results.append("Percentage Used Memory: {}%".format(meminfo.percent))
	results.append("==== SWAP: ====")
	results.append("Total: " + get_size(meminfo_swap.total))
	results.append("Used: " + get_size(meminfo_swap.used))
	results.append("Free: " + get_size(meminfo_swap.free))
	results.append("Percentage Used: {}%".format(meminfo_swap.percent))
	results.append('')

	#Disk Information
	diskinfo_partitions = psutil.disk_partitions()
	results.append('='*30 + "Disk Information" + '='*30)
	for partition in diskinfo_partitions:
		results.append(f"==== Device: {partition.device} ====")
		results.append("Mountpoint: " + partition.mountpoint)
		results.append("Filesystem: " + partition.fstype)
		results.append("Options: " + partition.opts)
		diskinfo_usage = psutil.disk_usage(partition.mountpoint)
		results.append("Total Size: " + get_size(diskinfo_usage.total))
		results.append("Used: " + get_size(diskinfo_usage.used))
		results.append("Available: " + get_size(diskinfo_usage.free))
		results.append("Percentage Used: {}%".format(diskinfo_usage.percent))
		results.append('')
	diskinfo_io = psutil.disk_io_counters()
	results.append("Total Read: " + get_size(diskinfo_io.read_bytes))
	results.append("Total Write: " + get_size(diskinfo_io.write_bytes))
	results.append('')

	#Network Information
	netinfo_addrs = psutil.net_if_addrs()
	results.append('='*30 + "Network Information" + '='*30)
	for int_name, int_addr in netinfo_addrs.items():
		results.append(f"==== Interface: {int_name} ====")
		for addr in int_addr:
			if str(addr.family) == "AddressFamily.AF_INET": # IPv4
				results.append("IPv4 Address: " + str(addr.address))
				results.append("Netmask: " + str(addr.netmask))
				results.append("Broadcast Address: " + str(addr.broadcast))
				results.append('')
			elif str(addr.family) == "AddressFamily.AF_INET6": # IPv6
				results.append("IPv6 Address: " + str(addr.address))
				results.append("Netmask: " + str(addr.netmask))
				results.append("Broadcast Address: " + str(addr.broadcast))
				results.append('')
			elif str(addr.family) == "AddressFamily.AF_PACKET": # MAC
				results.append("MAC Address: " + str(addr.address))
				results.append('')
	netinfo_io = psutil.net_io_counters()
	results.append("Total Bytes Sent: " + get_size(netinfo_io.bytes_sent))
	results.append("Total Bytes Received: " + get_size(netinfo_io.bytes_recv))

	return results


def hasher_md5(filename):
	hsh = hashlib.md5()
	with open(filename, "rb") as hashfile:
		buffr = hashfile.read()
		hsh.update(buffr)
		f_hash = hsh.hexdigest()
	return f_hash


def hasher_sha256(filename):
	hsh = hashlib.sha256()
	with open(filename, "rb") as hashfile:
		buffr = hashfile.read()
		hsh.update(buffr)
		f_hash = hsh.hexdigest()
	return f_hash

def compare_hashes(hsh):
	if len(hsh) == 32: 
		hashset_md5 = open("hashset/hashset_md5", "r")
		for hash_ in hashset_md5:
			hash_ = hash_.strip()
			if hsh == hash_:
				return hash_
	if len(hsh) == 64:
		hashset_sha256 = open("hashset/hashset_sha256","r")
		for hash_ in hashset_sha256:
			hash_ = hash_.strip()
			if hsh == hash_:
				return hash_

def verify_files(path):		# Path = lista av filer
	f = path				# Att inte ändra det som vi redan haft
	hashlist = []
	for item in f: 
		_hash_md5 = hasher_md5(item)
		_hash_sha = hasher_sha256(item)

		compare = compare_hashes(_hash_md5)
		if compare != None: 
			h = ("Hash duplicate found : {} : md5: {} ".format(item, compare))
			hashlist.append(h)
			print("\033[91mHash duplicate found\033[0m : \033[93m{}\033[0m : md5: {} ".format(item, compare))

		compare = compare_hashes(_hash_sha)
		if compare != None:
			h = ("Hash duplicate found : {} : sha256: {}".format(item, compare))
			hashlist.append(h)
			print("\033[91mHash duplicate found\033[0m : \033[93m{}\033[0m : sha256: {} ".format(item, compare))

	return hashlist                

def gen_report(dictionary):

	#Base settings
	#Header font: Helvetica-Bold
	#Header fontsize: 12
	#Normal font: Helvetica
	#Normal fontsize: 10

	x = 40; y = 11 * 72        
	c = canvas.Canvas("report.pdf") 
	c.setFont('Helvetica-Bold', 22)
	c.drawString(250,y,"Report")
	y -= 30

	for key, value in dictionary.items():
		if key == 'sys':
			c.setFont('Helvetica-Bold', 22)
			c.drawString(x,y, "System Information:")
			y = y - 30
			c.setFont('Helvetica', 10)
			for item in value:
				if y <= 50:
					c.showPage()
					c.setFont('Helvetica', 10)
					y = 11 * 72
				if len(item) > 110: 
					wrap_text = textwrap.wrap(item, width=110)
					c.drawString(x,y, wrap_text[0])
					y = y - 15
					c.drawString(x,y, wrap_text[1])
				else:
					c.drawString(x,y,item)
					y = y - 15
			y -= 30

		elif key == 'hashset':
			if value:
				c.setFont('Helvetica-Bold', 22)
				c.drawString(x,y,"Hashset:")
				y = y - 30
				c.setFont('Helvetica', 10)
				for item in value:
					if y <= 50:
						c.showPage()
						c.setFont('Helvetica', 10)
						y = 11 * 72
					if len(item) > 110:
						wrap_text = textwrap.wrap(item, width=110)
						c.drawString(x,y, wrap_text[0])
						y = y - 15
						c.drawString(x,y, wrap_text[1])
						y = y - 15
					else:
						c.drawString(x,y,item)
						y = y - 15
				y -= 30

		elif key == 'allfiles':
			for mapp, filer in value.items():
				c.setFont('Helvetica-Bold', 22)
				c.drawString(x,y,'All files in ' + mapp)
				y = y - 30
				c.setFont('Helvetica', 10)
				for item in filer:
					if y <= 50:
						c.showPage()
						c.setFont('Helvetica', 10)
						y = 11 * 72
					if len(item) > 110:
						wrap_text = textwrap.wrap(item, width=110)
						c.drawString(x,y, wrap_text[0])
						y = y - 15
						c.drawString(x,y, wrap_text[1])
					else:
						c.drawString(x,y,item)
						y = y - 15
				y -= 30


		elif key == 'extfiles': 
			for ext, filer in value.items():
				c.setFont('Helvetica-Bold', 22)
				c.drawString(x,y,'All files with ' + ext + " extension")
				y = y - 30
				c.setFont('Helvetica', 10)
				for item in filer:
					if y <= 50:
						c.showPage()
						c.setFont('Helvetica', 10)
						y = 11 * 72
					if len(item) > 110:
						wrap_text = textwrap.wrap(item, width=110)
						c.drawString(x,y, wrap_text[0])
						y = y - 15
						c.drawString(x,y, wrap_text[1])
					else:
						c.drawString(x,y,item)
						y = y - 15
				y -= 30

		elif key == 'infofiles':
			for info, filer in value.items():
				c.setFont('Helvetica-Bold', 22)
				c.drawString(x,y,'Files that contain ' + info )
				y = y - 30
				c.setFont('Helvetica', 10)
				for item in filer:
					if y <= 50:
						c.showPage()
						c.setFont('Helvetica', 10)
						y = 11 * 72
					if len(item) > 110:
						wrap_text = textwrap.wrap(item, width=110)
						c.drawString(x,y, wrap_text[0])
						y = y - 15
						c.drawString(x,y, wrap_text[1])
					else:
						c.drawString(x,y,item)
						y = y- 15
				y -= 30

		elif key == 'datefiles':
			for date, filer in value.items():
				c.setFont('Helvetica-Bold', 22)
				c.drawString(x,y,'Files modified up to ' + date)
				y = y - 30
				c.setFont('Helvetica', 10)
				for item in filer:
					if y <= 50:
						c.showPage()
						c.setFont('Helvetica', 10)
						y = 11 * 72
					if len(item) > 110:
						wrap_text = textwrap.wrap(item, width=110)
						c.drawString(x,y, wrap_text[0])
						y = y - 15
						c.drawString(x,y, wrap_text[1])
					else:
						c.drawString(x,y,item)
						y = y - 15
				y -= 30

	c.save()

def create_dict(key, dictionary, results):	# Skapa en jävligt stor dictionary för rapportgenerering
	if key not in dictionary:
		dictionary[key] = results
	else:
		for item in results:
			if item not in dictionary[key]:
				dictionary[key].append(item)


if __name__ == '__main__':
	print('Detta är en modul och ska inte köras självständigt!')
	exit()
