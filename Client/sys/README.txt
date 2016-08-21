These files need to be installed on the Raspberry Pi

1. The inittab file is used at system startup.  It 
is located in /etc.  It should only be edited to 
match the line for tty1.

2. The .bashrc is located in the pi's home directory.  
It is run when bash is run as in interactive shell, 
which is after a normal login.    Only the last
line of this one needs changeing to automatallicaly
start the attendance reader.

3. The 'start' file.  It does the actual starting
of the reader if the login and terminal is on tty1.
tty1 is the main screen for the pi.

