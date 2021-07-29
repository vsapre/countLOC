# countLOC
Python script to find the count of lines of code for code that uses C / C++ / Python style comments.

CountLOC was written to count the number of lines of code/comments/empty lines that are present in a code file. Currently supported formats are C, C++ and Python. The script expects a root path, and the kind of code that is to be analyzed. It distinguishes languages (.c,.cpp,.h,.py,.pyw) based on the following keys:

src: source files which use C or C++ style comments

hdr: header files which use C or C++ style comments

py: source files which use Python style comments.

all: All of the above.

From the root path it can walk a directory path and all its child directories to get hold of all the above types of source files.

The output consists of a count of Source Lines, Comment Lines and Empty lines for each file found, and a total number of above lines for the entire directory path.

Use Cases:
1. Can be used to showcase the code size of your project.
2. Can be used to figure out how many lines of code, one has been working on which can then be used to judge software productivity. 
3. Can be used to compare the number of code lines required in each language for implementing solutions to a given problem.
