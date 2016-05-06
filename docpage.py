# -*- coding: utf-8 -*-

import hashlib
import os
import os.path
import subprocess
import threading
import errno
from settings import CONVERT_CMD, COMPARE_CMD


def _mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def _ensureConverted(src, img):
    if not os.path.exists(img):
        imgpath = os.path.dirname(img)
        if not os.path.exists(imgpath):
            _mkdir_p(imgpath)
        if subprocess.call(CONVERT_CMD + [src, img]) != 0:
            print("error converting " + src + " to " + img)
            return False
    return True


class DocPage:

    afterDir = ""
    beforeDir = ""
    cacheDir = ""

    def __init__(self, key, originalFile, diff, status=None, comment=None):
        self.key = key
        self.originalName = originalFile
        self.difference = diff
        self.status = status
        self.comment = comment
        self.lock = threading.RLock()
        self.id = hashlib.md5(self.key).hexdigest()


    @classmethod
    def initDirs(cls, afterDir, beforeDir, cacheDir ):
        cls.afterDir = afterDir
        cls.beforeDir = beforeDir
        cls.cacheDir = cacheDir

    def isCompared(self):
        return os.path.exists(self.imgDiffFilename())

    def srcBeforeFilename(self):
        return DocPage.beforeDir + "/convertedPdfFiles/" + self.key

    def srcAfterFilename(self):
        return DocPage.afterDir + "/convertedPdfFiles/" + self.key

    def imgAfterFilename(self):
        return DocPage.afterDir + "/convertedPngFiles/" + self.key + ".png"

    def imgBeforeFilename(self):
        return DocPage.beforeDir + "/convertedPngFiles/" + self.key + ".png"

    def imgDiffFilename(self):
        return DocPage.cacheDir + "/" + self.id + ".png"

    def ensureCompared(self):
        with self.lock:
            if not _ensureConverted(self.srcAfterFilename(), self.imgAfterFilename()):
                return False
            if not _ensureConverted(self.srcBeforeFilename(), self.imgBeforeFilename()):
                return False
            if not os.path.exists(self.imgDiffFilename()):
                if subprocess.call(COMPARE_CMD + [self.imgAfterFilename(), self.imgBeforeFilename(), self.imgDiffFilename()]) != 0:
                    open(self.imgDiffFilename(), 'a').close()
                    return False
        return True