# coding:utf-8
import os
import sys
import getopt

# /Users/Chiang/Desktop/Uhomebk_module/UhomebkResource/UhomebkResource/Resources/UhomebkSDK_Assistant.bundle
# /Users/Chiang/Desktop/Uhomebk_module/UhomebkResource/UhomebkResource/Resources/UhomebkCommon_iOS.bundle
# /Users/Chiang/Desktop/Uhomebk_module/UhomebkResource/UhomebkResource/Resources/UhomebkSDK_SEGI.bundle

projectPath = '/Users/Chiang/Desktop/Uhomebk_module'
whiteSuffixs = ['.m', '.xib', '.storyboard']

def getInputParams():
    opts, args = getopt.getopt(sys.argv[1:], '-p:')
    for key, value in opts:
        if key == '-p':
            path = value

    if not os.path.exists(path):
        print("\033[0;31;40m\t输入的文件路径不存在\033[0m")
        exit(1)
    return path


def getImageName(path):
    nameSet = set()
    pathSet = set()
    for root, dirs, files in os.walk(path):
        for name in files:
            filePath = os.path.join(root, name)
            pathSet.add(filePath)

            fileName, fileSuffix = os.path.splitext(name)
            fileName = fileName.split('@')[0]
            nameSet.add(fileName)

    return nameSet, pathSet

def findImageInDirs(imageName, projectPath):
    searchName = '\"' + imageName + '\"'
    for root, dirs, files in os.walk(projectPath):
        for file in files:
            fileName, fileSuffix = os.path.splitext(file)
            if fileSuffix in whiteSuffixs:
                filePath = os.path.join(root, file)
                filetext = open(filePath)
                for line in filetext:
                    if searchName in line:
                        print(searchName + ' is found')
                        return True
                filetext.close()


def findImageNameInProject(imageNames, projectPath):
    imageNamesCopy = set(imageNames)
    for imageName in imageNames:
        isFind = findImageInDirs(imageName, projectPath)
        if isFind:
            imageNamesCopy.remove(imageName)
        else:
            print(imageName + ' is not used')
    return imageNamesCopy


def getTotalImageSize(paths):
    fileSize = 0
    for path in paths:
        fileSize = fileSize + os.path.getsize(path)
    return transformUnit(fileSize)


def transformUnit(sizeStr):
    size = int(sizeStr)
    unit = "B"
    if (size > 1000):
        size = size / 1000
        unit = "KB"
        if size > 1000:
            size = size / 1000;
            unit = "M"
    return ('%d%s' % (size, unit))


def getUnusedImagePaths(unusedImageNames, allPaths):
    unusedImagePaths = set()
    for name in unusedImageNames:
        for path in allPaths:
            fileName = path.split('/')[-1].split('@')[0]
            if name == fileName:
                unusedImagePaths.add(path)
    return unusedImagePaths


if __name__ == '__main__':
    path = getInputParams()
    # /获取所有图片名称和路径
    names, paths = getImageName(path)
    totalImageSize = getTotalImageSize(paths)
    print('一共找到【%d】张图片，大小总共【%s】' % (len(paths), totalImageSize))
    # 获取所有未使用的图片路径
    unusedImageNames = findImageNameInProject(names, projectPath)

    unusedImagePaths = getUnusedImagePaths(unusedImageNames, paths)
    totalSize = getTotalImageSize(unusedImagePaths)
    print('发现【%d】个没有使用的图片，大小总共【%s】' % (len(unusedImagePaths), totalSize))
    # # print(unusedImagePaths)
    print(unusedImageNames)
