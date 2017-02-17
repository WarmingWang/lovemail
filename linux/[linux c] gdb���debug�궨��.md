#[linux c] gdb如何debug宏定义
 本文阐述如何在gdb调试下查看宏定义的值及其原理。
 
###宏定义
宏定义是C语言提供的三种预处理功能中的一种。在**预编译**时将宏定义的字符串作简单的替换，并不参与计算。此过程在**编译**处理之前。故用*参数-g*不会生成debug信息。*（宏定义有优点也有缺点，注意使用。）*

###示例代码
 
	 //hello.c 
     #include <stdio.h>
     #define XX 11
     int main()
     {
	     int x = 1;
	     int y = XX;
	     printf("hello , world!\n%d\n%d\n",x,y);
	 }

###gcc编译参数解释
####-g
![Alt text](./1486717946336.png) 
参数**-g**可在操作系统中生成以本地格式（stabs,  COFF, XCOFF, or DWARF2）的调试信息，可用于gdb调试。换句话说，如果要使用gdb调试你的代码，你需要在gcc编译命令上加上**-g**参数。

使用 如下命令进行编译并生成debug信息。

    gcc -g hello.c -o hello

用*p XX*命令查看宏定义信息，出现如下错误：
![Alt text](./1486834887840.png)


####-glevel
 ![Alt text](./1486720608780.png)
 参数**-g3**会将扩展的debug信息编译进二进制文件里面，其中程序中存在的所有宏定义也包括在里面。
 
使用 如下命令进行编译并生成debug信息。

    gcc -g3 hello.c -o hello

用*p XX*命令查看宏定义信息，打印宏定义的debug信息。
![Alt text](./1486835771208.png)

 
 查看宏定义是如何展开的，使用命令***macro expand*** *macro_name*
![Alt text](./1486836012127.png)

**由此可见，如果需要在debug的时候查看宏定义信息，编译时需要加上参数*-g3* **