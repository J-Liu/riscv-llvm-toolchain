# RISC-V LLVM Compiler Toolchain

'Pure' LLVM Toolchian with Multi-libc for RISC-V.

## Prerequisites
It is well tested on Ubuntu-20.04 AMD64, I'm not sure about the other platfoms.

On Ubuntu, executing the following command should suffice:

`sudo apt-get install automake curl wget python3 libmpc-dev gawk build-essential bison flex texinfo gperf pkg-config libtool patchutils bc zlib1g-dev libexpat-dev ninja-build`

For we have `python3`, we can get a virtual environment, so we can install `virtualenv` by

`pip install virtualenv` or `pip3 install virtualenv`

## Usage
We should install our python virtual environment at the first time.

```
cd $PROJ_ROOT
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then, we can run it by

```
python main.py
```

It will ask you some simple question, when it got your choices, you may get a LLVM Toolchain with multi-libc.

### Re-build
If you can re-build it, remove the `$PROJ_ROOT/build/$XXX` directory, and change the `config` `build` `install` options into `false` in the `step.json`.

If you wanna change the version of software or something, I put all the configuration in `$PROJ_ROOT/conf/conf.py` and `$PROJ_ROOT/conf/environment.py`.


### Download Sources by Hand
If you wanna download the sources by yourself, the tree should looks like:

```
├── build
│   ├── clang
│   ├── compiler-rt-elf
│   ├── compiler-rt-musl
│   ├── musl
│   ├── musl-headers
│   └── newlib
├── common
├── conf
├── conf.json
├── main.py
├── patches
├── preparation
├── process
├── README.md
├── requirements.txt
├── resources
├── src
│   ├── linux-6.0.7
│   ├── llvm-project
│   ├── musl-1.2.3
│   └── newlib-4.2.0.20211231
├── step.json
├── tarballs
│   ├── linux-6.0.7.tar.xz
│   ├── musl-1.2.3.tar.gz
│   ├── newlib-4.2.0.20211231.tar.gz
│   └── qemu-7.1.0.tar.xz
├── utils
└── venv
```

Don't forget change the `download` options into `true` in the `step.json`.

## Test
You can test it on **QEMU**.

This is an example of elf toochain.
```
$PREFIX/bin/clang --target=$NEWLIB_TRIPLE --sysroot=$PREFIX/$NEWLIB_TRIPLE -fuse-ld=lld hello.c
$PREFIX/bin/qemu-riscv64 -L $PREFIX/$NEWLIB_TRIPLE -cpu rv64 a.out
```

This is another example of linux-musl toochain.
```
$PREFIX/bin/clang --target=$MUSL_TRIPLE --sysroot=$PREFIX/sysroot -fuse-ld=lld hello.c
$PREFIX/bin/qemu-riscv64 -L $PREFIX/sysroot -cpu rv64 a.out
```

## Ask for HELP
* cross compile libunwind/libcxx/libcxxabi.
* MinGW cross compile.
* glibc toolchain.
* Anyone please summit a C99 build patch to newlib?  I'm tired with mailinglist.

For I know almost nothing about coding, if you're good at it, don't be shy, contact me.
I'm open to new ideas.  And, BTW. Chinese is OK to me if you are Chinese, for I know over 2000 Chinese characters than 20 English letters.

I don't use Windows, if you wanna ship a toolchian to Win users, maybe you can help on MinGW cross compiling.

### Code Style
If you wanna work together, Change your `PyCharm`'s' `Hard wrap at` and `Visual guides` into `80` columns.  You can find them in `Preferences->Editor->Code Style`, let `PyCharm` check your code so you can fix all the warnings, and `PyCharm` can format your code perfectly.  It is FREE, maybe you can try it.

No abbreviation, keep UTF-8, no windows stuff, no Java style please.
