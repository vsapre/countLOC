# countLOC
Python script to find the count of lines of code for C/C++/Python code.

CountLOC was written to count the number of lines of code/comments/empty lines that are present in a code file. Currently supported formats are C, C++ and Python. The script expects a root path, and the kind of code that is to be analyzed. It distinguishes languages (.c,.cpp,.h,.py,.pyw) based on the following keys:
src: C or C++ code file
hdr: C or C++ header file
py: Python source file
all: All of the above.

From the root path it can walk a directory path and all its child directories to get hold of all the above types of source files.

The output consists of a listing of Source Lines, Comment Lines and Empty lines for each file found, and a total number of above lines for the entire directory path.
