"""
Module to count the number of lines of code in a given directory tree.
Currently works for Python, CPP, C, JavaScript
By default the search for files is fully recursive in the given tree, which
means all subdirectories will also be searched for matching file types.
if you want to include only files directly under the given directory, specify
'single' as the last argument for this python script

Usage:
C:/> python CountLOC.py <directory> <file type: py, src, hdr, all> <single>

Author: Vishal Sapre
"""
#!c:\Python24\

import sys
import os
import os.path
import fnmatch

##srcEndings = (";", ")", "}", "||", "|", "&&", "&", "\\", ",")
##srcBegins  = (
##    "#", "typedef", "union", "struct", "class", "extern", "enum",
##    "{", "(", "else"
##)

class LOCCounter:
    """
    Class containing methods for counting lines of code
	in a code file directory tree
	"""
    def __init__(self, rootPath=''):
        self.RootPath = rootPath
        self.scloc = 0
        self.ssloc = 0
        self.hsloc = 0
        self.hcloc = 0
        self.CMNTS = 0
        self.CntAllSrcFiles = 0
          # number of files, currently in the file list
        self.FlCnt = 0
          # current list of files to be analyzed
        self.FLst = []
        self.slevel = False

    def SetRootPath(self, rootPath=''):
        self.RootPath = rootPath

    def SetCurFileName(self, filename=''):
        self.CurfileName = self.RootPath + '\\' + filename

    def all_files(self, root, patterns, single_level=False, yield_folders=False):
        # Expand patterns from semicolon-separated string to list
        patterns = patterns.split(';')
        for path, subdirs, files in os.walk(root):
            if yield_folders:
                files.extend(subdirs)
            files.sort( )
            for name in files:
                for pattern in patterns:
                    if name.endswith(pattern):
                        self.FLst.append(os.path.join(path, name))
                        break

            if single_level:
                break

    def GetAllPySrcFiles(self):
        self.FLst = []
        self.all_files(self.RootPath, '.py', self.slevel)
        self.FlCnt = len(self.FLst)

    def GetPyFileLOC(self, filename=''):
        cloc = 0
        sloc = 0
        noloc = 0
        fl = open(filename, 'rU')
        lines = fl.readlines()
        for line in lines:
            line = line.strip("\r\t\n ")

            if not line:
                noloc += 1
            else:
##                # leave lines which are commented out
##                if (line.startswith("##")):
##                    cloc = cloc + 1
##                    continue
                # Get lines that are comments
                if (line.startswith("#")):
                    cloc += 1
                # if its not empty and not comment, then it must be code
                else:
                    sloc += 1
        fl.close()
        self.LOC = sloc + cloc
        return sloc,cloc,noloc

    def GetTotalPyLOC(self):
        self.FLst = []
        self.GetAllPySrcFiles()
        #FlstLen = len(self.FLst)
        Scloc = Ssloc = Snoloc = 0
        if(self.FlCnt == 0):
            print ("No Python files found in this directory tree")
        else:
            for fls in self.FLst:
                ssloc,scloc, noloc = self.GetPyFileLOC(fls)
                print("%s, Source: %s, Comments: %s" % (fls, ssloc, scloc))
                Ssloc += ssloc
                Scloc += scloc

        print("\nTotal number of Python source files in this directory tree: %d" %self.FlCnt)
        print("Total comment lines in this tree: %d" % Scloc)
        print("Total source lines in this tree: %d" % Ssloc)
        print("Total empty lines in this directory tree: %d" % Snoloc)
        print("Total lines for Python code in this directory tree: %d" %(Ssloc + Scloc + Snoloc))


    def GetSrcFiles(self, Path):
        self.FLst = []
        self.all_files(Path,'.cpp;.c;.js', self.slevel)
        self.FlCnt = len(self.FLst)

    def GetHdrFiles(self, Path):
        self.FLst = []
        self.all_files(Path, '.h;.hpp', self.slevel)
        self.FlCnt = len(self.FLst)

    def GetFileLOC(self, filename=''):
        cloc = 0
        sloc = 0
        noloc = 0
        multiLineComment = False
        fl = open(filename, 'rU')
        lines = fl.readlines()
        for line in lines:
            line = line.strip("\n\r\t ")
            # Get lines which are commented. only '//' comments are supported.
            # for /**/ we need to have a state machine approach...much more complicated
            if not line:
                noloc += 1
            else:
                # this condition needs to be checked first,otherwise...once
                # multilinecomment is True,it will never we false again.
                if(line.endswith("*/")):
                    cloc = cloc + 1
                    multiLineComment = False

                elif(line.startswith("/*")):
                    cloc = cloc + 1
                    multiLineComment = not (line.endswith("*/"))

                elif(multiLineComment == True):
                    cloc = cloc + 1;

                elif(line.startswith("//")):
                    cloc = cloc + 1

                # if its neither empty nor a comment, then its code !!
                else:
                    sloc = sloc + 1

        fl.close()
        self.LOC = sloc + cloc
        return sloc,cloc, noloc

    def GetSrcFilesLOC(self):
        Ssloc = 0
        Scloc = 0
        Snoloc = 0
        self.GetSrcFiles(self.RootPath)
        if(self.FlCnt == 0):
            print ("No Source files found in this directory tree")
        else:
            largestFileName = max([len(os.path.basename(fl)) for fl in self.FLst])
            print("\nLines of Code in Source Files")
            for fls in self.FLst:
                ssloc,scloc,snoloc = self.GetFileLOC(fls)
                flbase = os.path.basename(fls).ljust(largestFileName)
                ssloc_str = ("%s"%ssloc).ljust(7)
                scloc_str = ("%s"%scloc).ljust(7)
                snoloc_str = ("%s"%snoloc).ljust(7)
                print(''.join((flbase, ":  Source: ", ssloc_str, "Comments: ", scloc_str, "EmptyLines: ", snoloc_str)))
                Ssloc += ssloc
                Scloc += scloc
                Snoloc += snoloc

        print("\nTotal number of source files in this directory tree: %d" %self.FlCnt)
        print("Total source lines in this directory tree: %d" % Ssloc)
        print("Total comment lines in this directory tree: %d" % Scloc)
        print("Total empty lines in this directory tree: %d" % Snoloc)
        print("Total lines in this directory tree: %d\n" %(Ssloc + Scloc + Snoloc))

    def GetHdrFilesLOC(self):
        Hsloc = 0
        Hcloc = 0
        Hnoloc = 0
        self.GetHdrFiles(self.RootPath)

        if(self.FlCnt == 0):
            print ("No Header files found in this directory tree")
        else:
            largestFileName = max([len(os.path.basename(fl)) for fl in self.FLst])
            print("\nLines of Code in Header Files")
            for fls in self.FLst:
                hsloc,hcloc,hnoloc = self.GetFileLOC(fls)
                flbase = os.path.basename(fls).ljust(largestFileName)
                hsloc_str  = ("%s"%hsloc).ljust(7)
                hcloc_str  = ("%s"%hcloc).ljust(7)
                hnoloc_str = ("%s"%hnoloc).ljust(7)
                print(''.join((flbase, ":  Source: ", hsloc_str, "Comments: ", hcloc_str, "EmptyLines: ", hnoloc_str)))
                Hsloc += hsloc
                Hcloc += hcloc
                Hnoloc += hnoloc

        print("\nTotal number of header files in this directory tree: %d" %self.FlCnt)
        print("Total source lines in this directory tree: %d" % Hsloc)
        print("Total comment lines in this directory tree: %d" % Hcloc)
        print("Total empty lines in this directory tree: %d" % Hnoloc)
        print("Total lines in this directory tree: %d\n" % (Hsloc + Hcloc + Hnoloc))

    def GetTotalLOC(self):
        self.GetSrcFilesLOC()
        self.GetHdrFilesLOC()

if __name__ == '__main__':
    print("number of arguments: %d" % len(sys.argv))

    for i in (sys.argv):
        print i

    if (len(sys.argv) < 2):
        print("\nRequired arguments Missing")
        print("Required arguments: RootPath, FileType(src, hdr, all, py)")
        sys.exit(2)

    # instantiate the line counter object
    if (sys.argv[1].endswith(('.cpp','.c','.h','.hpp','.py'))):
        singlefile = True
    else:
        singlefile = False

    lctr = LOCCounter(sys.argv[1])

    # if file search should be limited to the provided directory only
    # and not be recursive into the directory tree.
    if((len(sys.argv) > 3) and (sys.argv[3] == 'single')):
        lctr.slevel = True

    if(sys.argv[2] == 'py'):
        if not (singlefile):
            lctr.GetTotalPyLOC()
        else:
            s,c = lctr.GetPyFileLOC(sys.argv[1])
            print("File name: %s" %(os.path.basename(sys.argv[1])))
            print("Total lines: %s\nSource lines: %s\nComment lines: %s" % ((s+c), s, c))
        sys.exit(0)

    elif (sys.argv[2] == 'src'):
        lctr.GetSrcFilesLOC()

    elif (sys.argv[2] == 'hdr'):
        lctr.GetHdrFilesLOC()

    elif (sys.argv[2] == 'all'):
        lctr.GetTotalLOC()

    else:
        print("Error: invalid FileType specifier (%s)" % (sys.argv[2]))
        sys.exit(2)

    sys.exit(0)
