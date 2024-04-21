# Satcoin CNF gen n run

## How to use the cnf generator

**Prerequisites:**
- You need to install CBMC on your system. If you plan to use CBMC (and this project) on windows, you need to install Visual Studio too, and use Visual Studio's CMD to run the scripts. Linux users can install cbmc with sudo.
- Installed python on your system.
- On Linux, **requests** python module might not be installed by default (my happen on windows too) if not, install it with pip
- You need a C/C++ compiler on your system. MinGW for windows. Linux users can install with sudo.

**how to run the cnf generator**

- Open up the CMD of your choice
- cd into this projects folder
- run: python create_cnf.py OR python3 create_cnf.py
- Follow the instructions of the program. Blocks will be stored in .txt file, CNF files will be placed into a folder of your choice (inside this projects root dir), you can enter your preferred nonce range for the tests, and if you already have blocks in your txt, you can skip the query blocks part.


## How to use the solver script

/* TODO */

## Credits

The project is based on J. Heusser's concept, as well as the C implementation of the method, he was the first to introduce this SAT solving method for alternative Bitcoin mining in 2013. https://jheusser.github.io/2013/02/03/satcoin.html

The network request to query raw hex data of any block is provided by blockchair.com

The project otherwise is part of my M.Sc. Thesis. I created this cnf file generator + solver script, because I wanted to run hundreds of tests on different blocks, using Heusser's method.

/* TODO  UPDATE THIS PART */