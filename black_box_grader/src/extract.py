from io import BytesIO
import base64
import tarfile
import os
import shutil

# data + studentId + projectId
TMP_PATH = "tmp/"


def changeRootFolder(filename, basePath):
    folderlist = filename.split("/")
    return "/".join([basePath] + folderlist[1:])


def extractTarGz(tarGzBase64, basePath):
    try:
        shutil.rmtree(TMP_PATH)
    except FileNotFoundError:
        pass

    targzBin = base64.b64decode(tarGzBase64)
    tf = tarfile.open(fileobj=BytesIO(targzBin))
    print(tf.getmembers())
    os.makedirs(basePath)
    for member in tf.getmembers():
        print(member.path)
        if member.isdir():
            os.makedirs(changeRootFolder(member.path, basePath))
        else:
            with open(changeRootFolder(member.path, basePath), "wb") as fout:
                fout.write(tarfile.ExFileObject(tf, member).read())
