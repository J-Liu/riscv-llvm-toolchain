# RISC-V LLVM Compiler Toolchain

**A Multi-libc LLVM Toolchain for RISC-V with QEMU.**

**Components:**
* Clang/LLVM
* lld
* compiler-rt
* Newlib
* Musl-libc
* QEMU

**TODO/Status/Ask For Help:**
* **libcxx/libcxxabi/libunwind** cross compile.

## Prerequisites
### Ubuntu

On Ubuntu, executing the following command should suffice:

`sudo apt-get install automake curl wget python3 libmpc-dev gawk build-essential bison flex texinfo gperf pkg-config libtool patchutils bc zlib1g-dev libexpat-dev ninja-build`


### macOS
**Make sure your filesystem is 'APFS Case Sensitive'**

Install [***homebrew***](https://brew.sh) first, and then executing the following command:

```
brew install cmake ninja python libtool pkg-config glib zlib
```


## Usage
Change the **PREFIX** in **set_custom_env** first, and you can switch the other options.


```
set_custom_env() {
  export CLANG_PREFIX=<PREFIX>
  export BUILD_TYPE=Release
  export WITH_MUSL=ON
  export WITH_NEWLIB=ON
  export WITH_QEMU=ON
}
```

Then, we can run it by

```
bash rv64.sh
```

If the *bash script* failed, try *zsh script*.  Every single step is right,
but it seem lead a wrong path sometimes.

```
zsh rv64-zsh.sh
```


### Re-build
If you can re-build it, remove the **$PROJ_ROOT/build/$XXX** directory.

### Download Sources by Hand
If you wanna download the sources by yourself, the tree should looks like:

```
├── build
│   ├── clang
│   ├── compiler-rt-musl
│   ├── compiler-rt-newlib
│   ├── musl
│   ├── musl-header
│   ├── newlib
│   ├── qemu
│   ├── runtimes-musl
│   └── runtimes-newlib
├── patch
│   └── newlib-4.2.0.20211231-C99-build.diff
├── rv64.sh
├── src
│   ├── linux-headers
│   ├── llvm-project
│   ├── musl-1.2.3
│   ├── newlib-4.2.0.20211231
│   ├── newlib_patched
│   └── qemu-7.1.0
└── tarball
    ├── linux-headers.tar.bz2
    ├── musl-1.2.3.tar.gz
    ├── newlib-4.2.0.20211231.tar.gz
    └── qemu-7.1.0.tar.xz
```

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

It is my first time to write bash, for I know almost nothing about coding,
if you're good at **meson**, please help.  This kind of task is better to be
done by build system.

And, BTW. Chinese is OK to me if you are Chinese, for I know over 2000 Chinese
characters than 20 English letters.

I don't use Windows, if you wanna ship a toolchian to Win users,
maybe you can help on MinGW cross compiling.
