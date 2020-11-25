import os
import optparse
import traceback
#from pathlib import Path

DIRECTORIES = {
    "HTML": [".html5", ".html", ".htm", ".xhtml"],
    "IMAGES": [".jpeg", ".jpg", ".tiff", ".gif", ".bmp", ".png", ".bpg", "svg",
               ".heif", ".psd"],
    "VIDEOS": [".avi", ".flv", ".wmv", ".mov", ".mp4", ".webm", ".vob", ".mng",
               ".qt", ".mpg", ".mpeg", ".3gp", ".mkv"],
    "DOCUMENTS": [".oxps", ".epub", ".pages", ".docx", ".doc", ".fdf", ".ods",
                  ".odt", ".pwi", ".xsn", ".xps", ".dotx", ".docm", ".dox",
                  ".rvg", ".rtf", ".rtfd", ".wpd", ".xls", ".xlsx", ".ppt",
                  "pptx", ".csv"],
    "ARCHIVES": [".a", ".ar", ".cpio", ".iso", ".tar", ".gz", ".rz", ".7z",
                 ".dmg", ".rar", ".xar", ".zip"],
    "AUDIO": [".aac", ".aa", ".aac", ".dvf", ".m4a", ".m4b", ".m4p", ".mp3",
              ".msv", "ogg", "oga", ".raw", ".vox", ".wav", ".wma"],
    "PLAINTEXT": [".txt", ".in", ".out"],
    "PDF": [".pdf"],
    "XML": [".xml"],
    "EXE": [".exe", ".bat"],
    "SHELL": [".sh"]

}

FILES = {file_format:directory for directory, file_formats in DIRECTORIES.items() for file_format in file_formats}

def organize_files():

	for entry in os.scandir():
		if entry.is_dir():
			continue
		file_path = os.abspath(dir)
		print file_path
		file_ft = file_path.suffix.lower()
		if file_ft in FILES:
			directory_path = Path(FILES[file_ft])
			directory_path.mkdir(exist_ok=True)
			file_path.rename(directory_path.joinpath(file_path))
		
	try:
		os.mkdir("Others")
	except:
		pass
	
	for dir in os.scandir():
		try:
			print dir
			if dir.is_dir():
				os.rmdir(dir)
			else:	
				os.rename(os.getcwd() + '/' + str(Path(dir)), os.getcwd() + '/Others/' + str(Path(dir)))
				
		except Exception, err:
			print str(err)
			pass

def usage():
		print 'Organize the directory neatly the way you want and arrange them in decorative folders respectively.'
		print '-d, --dir: Provide to directory where files are to be arranged'
		print '-h, --help: Print the help about the tool.'

def getalldris(dirnm):
	print dirnm
	for root, dirs, files in os.walk(os.path.abspath(dirnm)):
		try:
			for file in files:
				if file == __file__:
					continue
				print os.path.dirname(os.path.join(dirnm, file)), file
				file_ft = '.' + file.split('.')[-1]
				if file_ft in FILES:
					dir_path = FILES[file_ft]
					if not os.path.exists(os.path.join(dirnm, dir_path)):
						os.mkdir(os.path.join(dirnm, dir_path))
					print os.path.join(dirnm, dir_path, file)
					os.rename(os.path.join(dirnm, file), os.path.join(dirnm, dir_path, file))
			
				else:
					if not os.path.exists(os.path.join(dirnm, 'Others')):
						os.mkdir(os.path.join(dirnm, 'Others'))
					os.rename(os.path.join(dirnm, file), os.path.join(dirnm, 'Others', file))
		except Exception, err:
			print str(err)
			traceback.print_exc()
			pass
		break

def main():
	inf_usage = ''' Organize the directory neatly the way you want and arrange them in decorative folders respectively.
					-d, --dir: Provide to directory where files are to be arranged'
					-h, --help: Print the help about the tool.'''
	parser = optparse.OptionParser(inf_usage)
	parser.add_option('-d' , type='string', dest='dirname', help='Provide the target directory.')
	parser.add_option('-H',  action='store_true', dest='help', default = False, help='Gives the help about the tool')
	opts, args = parser.parse_args()
	if opts.help:
		usage()
		exit(0)
	if opts.dirname is None or opts.dirname is '':
		print 'The directory name given is invalid.'
		print 'Please try with a valid directory.'
		usage()
		exit(0)
	
	print os.path.abspath(opts.dirname)
	getalldris(opts.dirname)
	
if __name__ == '__main__':
	main()
