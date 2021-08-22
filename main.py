#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#goal:  copy new file and new directory to destpath,
#goal:  delete old file and old directory in destpath,
#goal:  ignore the same file and same directory
import shutil

#you should change the following path parameter
import os
from os import walk

#please change the source path
sourcePath = "D:/Books"
#please change the destination path
destPath = "D:/Books1"


sourcePath = sourcePath.replace('\\', '/')
destPath = destPath.replace('\\', '/')

def GetSubDirAndSubFiles(path):
    subDirDic = {}
    subFileDic = {}
    for (dirpath, dirnames, filenames) in walk(path):
        key = dirpath.replace('\\', '/')
        subFileDic[key] = filenames
        subDirDic[key] = dirnames
    return subDirDic, subFileDic


sourceDirDic, souceFileDic = GetSubDirAndSubFiles(sourcePath)
destDirDic, destFileDic = GetSubDirAndSubFiles(destPath)

#delete old directory in destpath
for destKey in destDirDic:
    if sourcePath == destKey or destPath == destKey:
        continue
    sourceKey = destKey.replace(destPath, sourcePath)
    if sourceKey in sourceDirDic:
        continue

    # removing the file using the os.remove() method
    if os.path.exists(destKey):
        print("delete Directory: " + destKey)
        shutil.rmtree(destKey)

#refresh dest info
destDirDic, destFileDic = GetSubDirAndSubFiles(destPath)

#delete old file in destPath
for destKey in destFileDic:
    sourceKey = destKey.replace(destPath, sourcePath)
    for subDestKey in destFileDic[destKey]:  #所有文件的list
        if subDestKey in souceFileDic[sourceKey]:
            continue
        curFilePath = destKey + "/" + subDestKey
        print("delete File: " + curFilePath)
        os.remove(curFilePath)

destDirDic, destFileDic = GetSubDirAndSubFiles(destPath)

#copy new directory to destPath
for sourceKey in sourceDirDic:
    if sourcePath == sourceKey or destPath == sourceKey:
        continue
    destKey = sourceKey.replace(sourcePath, destPath)
    if destKey in destDirDic:
        continue
    if os.path.exists(destKey):
        continue
    #parentIndex = key.rfind('/')
    #parentPath = key[:parentIndex]
    #subDirectoryName = key[parentIndex + 1:]
    #destDicPath = os.path.join(parentPath, subDirectoryName)
    print("copy Directory from: " + sourceKey + " to: " + destKey)
    shutil.copytree(sourceKey, destKey, False, None)

destDirDic, destFileDic = GetSubDirAndSubFiles(destPath)

#copy new file to destPath
for sourceKey in souceFileDic:
    destKey = sourceKey.replace(sourcePath, destPath)
    for subSourceKey in souceFileDic[sourceKey]:
        if subSourceKey in destFileDic[destKey]:
            continue
        destFilePath = destKey + "/" + subSourceKey
        sourceFilePath = sourceKey + "/" + subSourceKey
        print("copy File from: " + sourceFilePath + " to: " + destFilePath)
        shutil.copy2(sourceFilePath, destFilePath)

print("copy ends-----------")