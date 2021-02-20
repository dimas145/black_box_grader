from io import BytesIO
import base64
import tarfile
import os


# data + studentId + projectId
PREFIX_FOLDER = "data/13517089/1234"


def changeRootFolder(filename):
    folderlist = filename.split("/")
    return "/".join([PREFIX_FOLDER] + folderlist[1:])


def extractTarGz(tarGzBase64):
    targzBin = base64.b64decode(tarGzBase64)
    tf = tarfile.open(fileobj=BytesIO(targzBin))
    print(tf.getmembers())

    for member in tf.getmembers():
        print(member.path)
        if member.isdir():
            os.makedirs(changeRootFolder(member.path))
        else:
            with open(changeRootFolder(member.path), "wb") as fout:
                fout.write(tarfile.ExFileObject(tf, member).read())


tarGzBase64 = "H4sIAAAAAAAAA+3W3WrCMBQH8F73KQKDYS90JibpHPQZ9ggSm0TL7AdpCt3bL7rBmJsfE0XE/+8mbZNycjg9oY3qZ4tVPVer2dIobVx0fuNASrkZg+0xTPKI8jGd8DTlIg3PKRdMRosL7OWXrvXKhZCurv2+dYfmt5O7EYKRvC5LU/lMWM3UXOR2bngqn4WUUzVVhko7pVxTrqTNrRY2vvae4Xy8af1wWddvw1K13rjhsV/B0/Ex1v2QpmJ3/4frn/3PGJMsEpdL+9ud9//p9S9VUY2a9yNifJ7/fGf9Kafb9Z8IEdZfPPvo7uv/sD7+m5Xxhvhl0RLbVbkv6iqOY20sKdpXrQd98hKTwBnfuYr05JFQkmWEhlU9yUhR+UFRNZ0fJEncuM3t14vJtROEvU7vfxd+F0szKvXBGIf6/4/zn49Ziv4HAAAAAAAAAAAAAAAAAPiHDxzfOpkAKAAA"

extractTarGz(tarGzBase64)
