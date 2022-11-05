# RISC-V LLVM Compiler Toolchain

'Pure' LLVM Toolchian for RISC-V.

## Prerequisites
It is well tested on Ubuntu-20.04 AMD64, I'm not sure about the other platfoms.

On Ubuntu, executing the following command should suffice:

`sudo apt-get install automake curl wget python3 libmpc-dev gawk build-essential bison flex texinfo gperf pkg-config libtool patchutils bc zlib1g-dev libexpat-dev`

## Usage
### Bare-metal Toolcahin
Change the `CLANG_INSTALL` into your **PREFIX**, then run

```
cd $PROJ_ROOT
bash riscv64-elf.sh
```

you will get `riscv64-elf` toochain, including `clang`, `lld`, `newlib`, `compiler-rt`.

### Linux Musl Toolcahin
Change the `CLANG_INSTALL` into your **PREFIX**, then run

```
cd $PROJ_ROOT
bash riscv64-linux-musl.sh
```

you will get `riscv64-linux-musl` toochain, including `clang`, `lld`, `musl`, `compiler-rt`.

### Re-build
If you can re-build it, just remove the `$PROJ_ROOT/build-*` directory.

### Download Sources by Hand
If you wanna download the sources by yourself, the tree should looks like:

```
├── build-elf
│   ├── clang
│   ├── compiler-rt
│   └── newlib
├── build-musl
│   ├── clang
│   ├── compiler-rt
│   ├── musl
│   └── musl-headers
├── patches
│   └── newlib-4.2.0.20211231-C99-build.diff
├── rv-musl.sh
├── rv-newlib.sh
├── src
│   ├── linux-6.0.7
│   ├── llvm-project
│   ├── musl-1.2.3
│   └── newlib-4.2.0.20211231
├── stamps
│   ├── newlib_src_patched
│   ├── src_downloaded
│   └── src_extracted
└── tarballs
    ├── linux-6.0.7.tar.xz
    ├── musl-1.2.3.tar.gz
    ├── newlib-4.2.0.20211231.tar.gz
    └── qemu-7.1.0.tar.xz
```

## Test
When you built the bare-metal toolcahin, you can test it on **QEMU**.

```
$CLANG_INSTALL/bin/clang --sysroot=$NEWLIB_SYSROOT -fuse-ld=lld hello.c
qemu-riscv64 -L $NEWLIB_SYSROOT -cpu rv64 a.out
```

It will be OK.

If you wanna test the linux-musl toolcahin, you can try

```
$CLANG_INSTALL/bin/clang --sysroot=$MUSL_SYSROOT -fuse-ld=lld hello.c
qemu-riscv64 -L $MUSL_SYSROOT -cpu rv64 a.out
```

It still can compile, but qemu will get a error msg like:

`qemu-riscv64: Could not open '/lib/ld-musl-riscv64.so.1': No such file or directory`

## Ask for HELP
* cross compile libunwind/libcxx/libcxxabi.
* Fix musl loader problem.
* Better stamp support.
* MinGW cross compile.
* glibc toolchain.
* Anyone please summit a C99 build patch to newlib?  I'm tired with mailinglist.
* Multi-libc toolchain.

For I know almost nothing about coding, if you're good at shell-script/Makefile/CMakeLIsts.txt, don't be shy, contact me.
I'm open to new ideas.  And, BTW. Chinese is OK to me if you are Chinese, for I know over 2000 Chinese characters than 20 English letters.

I don't use Windows, if you wanna ship a toolchian to Win users, maybe you can help on MinGW cross cimpiling.
