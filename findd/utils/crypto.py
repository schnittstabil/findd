import hashlib


def hashfile(path, blocksize=65536):
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha224 = hashlib.sha224()
    sha256 = hashlib.sha256()
    sha384 = hashlib.sha384()
    sha512 = hashlib.sha512()

    with open(path, 'rb') as afile:
        buf = afile.read(blocksize)

        while len(buf) > 0:
            md5.update(buf)
            sha1.update(buf)
            sha224.update(buf)
            sha256.update(buf)
            sha384.update(buf)
            sha512.update(buf)
            buf = afile.read(blocksize)

    return {
        'md5': md5.hexdigest(),
        'sha1': sha1.hexdigest(),
        'sha224': sha224.hexdigest(),
        'sha256': sha256.hexdigest(),
        'sha384': sha384.hexdigest(),
        'sha512': sha512.hexdigest(),
    }
