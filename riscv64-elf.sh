#!/bin/bash

export TOP=$PWD
export JOBS=-j32

export CLANG_INSTALL=/home/liujia/riscv-elf-clang
export PATH=$CLANG_INSTALL/bin:$PATH

export TARGET_TRIPLE=riscv64-unknown-elf
export NEWLIB_SYSROOT=$CLANG_INSTALL/$TARGET_TRIPLE

export SUFFIX_LZ=tar.lz
export SUFFIX_XZ=tar.xz
export SUFFIX_BZ=tar.bz2
export SUFFIX_GZ=tar.gz
export LINUX_VER=6.0.7
export LINUX_TARBALL=linux-$LINUX_VER.$SUFFIX_XZ
export MUSL_VER=1.2.3
export MUSL_TARBALL=musl-$MUSL_VER.$SUFFIX_GZ
export NEWLIB_VER=4.2.0.20211231
export NEWLIB_TARBALL=newlib-$NEWLIB_VER.$SUFFIX_GZ

export TARGET_CLANG_CFLAGS="--target=$TARGET_TRIPLE --sysroot=$NEWLIB_SYSROOT"
export TARGET_CLANG_CXXFLAGS=$TARGET_CLANG_CFLAGS
export TARGET_CLANG_LDFLAGS="-fuse-ld=lld"

export TOOLS_TO_BUILD="clang;lld"
export TARGETS_TO_BUILD="RISCV"
export BUILE_TYPE=Release

export TARBALL_ROOT=$TOP/tarballs
export STAMPS_ROOT=$TOP/stamps
export PATCH_ROOT=$TOP/patches

export NEWLIB_PATCH=$PATCH_ROOT/newlib-4.2.0.20211231-C99-build.diff

export SRC_ROOT=$TOP/src
export SRC_NEWLIB=$SRC_ROOT/newlib-$NEWLIB_VER
export LLVM_SRC_ROOT=$SRC_ROOT/llvm-project
export SRC_LLVM=$LLVM_SRC_ROOT/llvm
export SRC_COMPILER_RT=$LLVM_SRC_ROOT/compiler-rt

export BUILD_ROOT=$TOP/build-elf
export BUILD_CLANG=$BUILD_ROOT/clang
export BUILD_COMPILER_RT=$BUILD_ROOT/compiler-rt
export BUILD_NEWLIB=$BUILD_ROOT/newlib

mkdir -p $SRC_ROOT
mkdir -p $BUILD_ROOT
mkdir -p $TARBALL_ROOT
mkdir -p $STAMPS_ROOT

download_src()
{
  cd $SRC_ROOT;
  echo "Geting LLVM..."
  if [ ! -d "llvm-project" ]; then
    git clone https://github.com/llvm/llvm-project.git
  fi

  cd $TARBALL_ROOT;
  echo "Geting $LINUX_TARBALL..."
  if [ ! -f $LINUX_TARBALL ]; then
    curl -O https://cdn.kernel.org/pub/linux/kernel/v6.x/$LINUX_TARBALL
  fi

  echo "Geting $NEWLIB_TARBALL..."
  if [ ! -f $NEWLIB_TARBALL ]; then
    curl -O ftp://sourceware.org/pub/newlib/$NEWLIB_TARBALL
  fi

  echo "Geting $MUSL_TARBALL..."
  if [ ! -f $MUSL_TARBALL ]; then
    curl -O https://musl.libc.org/releases/$MUSL_TARBALL
  fi

  return 0
}

if [ ! -f $STAMPS_ROOT/src_downloaded ]; then
  echo "Download start"
  download_src
fi

if [ $? = 0 ]; then
  echo "Download finish"
  touch $STAMPS_ROOT/src_downloaded
else
   echo "Something wrong when download sources"
fi

extract_src()
{
  cd $SRC_ROOT;
  echo "Extracting linux..."
  if [ ! -d linux-$LINUX_VER ]; then
    tar xf $TARBALL_ROOT/$LINUX_TARBALL
  fi
  echo "Extracting newlib..."
  if [ ! -d newlib-$NEWLIB_VER ]; then
    tar xf $TARBALL_ROOT/$NEWLIB_TARBALL
  fi
  echo "Extracting musl..."
  if [ ! -d musl-$MUSL_VER ]; then
    tar xf $TARBALL_ROOT/$MUSL_TARBALL
  fi
}

if [ ! -f $STAMPS_ROOT/src_extracted ]; then
  echo "Extraction start"
  extract_src
fi

if [ $? = 0 ]; then
  echo "Extraction finish"
  touch $STAMPS_ROOT/src_extracted
else
   echo "Something wrong when extract sources"
fi

patch_src()
{
  cd $SRC_NEWLIB;
  echo "Patching newlib..."
  patch -p1 < $NEWLIB_PATCH
}

if [ ! -f $STAMPS_ROOT/newlib_src_patched ]; then
  echo "Patch start"
  patch_src
fi

if [ $? = 0 ]; then
  echo "Patch finish"
  touch $STAMPS_ROOT/newlib_src_patched
else
   echo "Something wrong when patch sources"
fi

mkdir -p $BUILD_CLANG
cd $BUILD_CLANG
cmake \
-G Ninja \
-DLLVM_ENABLE_PROJECTS=$TOOLS_TO_BUILD \
-DCMAKE_BUILD_TYPE=$BUILE_TYPE \
-DCMAKE_INSTALL_PREFIX=$CLANG_INSTALL \
-DLLVM_TARGETS_TO_BUILD=$TARGETS_TO_BUILD \
-DLLVM_DEFAULT_TARGET_TRIPLE=$TARGET_TRIPLE \
-DLLVM_BUILD_EXAMPLES=OFF \
-DLLVM_INCLUDE_EXAMPLES=OFF \
-DBUILD_SHARED_LIBS=OFF \
-DLLVM_OPTIMIZED_TABLEGEN=ON \
-DLLVM_ENABLE_LIBXML2=OFF \
-DCLANG_ENABLE_ARCMT=OFF \
-DCLANG_ENABLE_STATIC_ANALYZER=OFF \
-DCLANG_DEFAULT_RTLIB=compiler-rt \
-DCLANG_DEFAULT_UNWINDLIB=libunwind \
-DCLANG_DEFAULT_CXX_STDLIB=libc++ \
$SRC_LLVM
ninja
ninja install
cd $BUILD_ROOT

ARG_HOLDER='"$@"'
echo "$CLANG_INSTALL/bin/clang $TARGET_CLANG_CFLAGS -Wno-unused-command-line-argument $ARG_HOLDER" > $CLANG_INSTALL/bin/$TARGET_TRIPLE-clang
echo "$CLANG_INSTALL/bin/clang++ $TARGET_CLANG_CFLAGS -Wno-unused-command-line-argument $ARG_HOLDER" > $CLANG_INSTALL/bin/$TARGET_TRIPLE-clang++
chmod +x $CLANG_INSTALL/bin/$TARGET_TRIPLE-clang
chmod +x $CLANG_INSTALL/bin/$TARGET_TRIPLE-clang++
cd $CLANG_INSTALL/bin
ln -s $TARGET_TRIPLE-clang $TARGET_TRIPLE-gcc
ln -s $TARGET_TRIPLE-clang++ $TARGET_TRIPLE-g++
ln -s lld $TARGET_TRIPLE-ld
ln -s lld $TARGET_TRIPLE-ld.lld
ln -s lld $TARGET_TRIPLE-ld64.lld
for i in ar nm objcopy objdump ranlib strip;do
  ln -s llvm-$i $TARGET_TRIPLE-$i
done
cd $BUILD_ROOT

mkdir -p $BUILD_NEWLIB
cd $BUILD_NEWLIB
export CFLAGS_FOR_TARGET=" -Wno-int-conversion -g -gdwarf-3 -gstrict-dwarf -O2 -ffunction-sections -fdata-sections "
export CC_FOR_TARGET=$TARGET_TRIPLE-clang
export AS_FOR_TARGET=$TARGET_TRIPLE-clang
export LD_FOR_TARGET=lld
export CXX_FOR_TARGET=$TARGET_TRIPLE-clang++
export AR_FOR_TARGET=llvm-ar
export NM_FOR_TARGET=llvm-nm
export RANLIB_FOR_TARGET=llvm-ranlib
export OBJCOPY_FOR_TARGET=llvm-objcopy
export OBJDUMP_FOR_TARGET=llvm-objdump
export READELF_FOR_TARGET=llvm-readelf
export STRIP_FOR_TARGET=llvm-strip
export LIPO_FOR_TARGET=llvm-lipo
export DLLTOOL_FOR_TARGET=llvm-dlltool
$SRC_NEWLIB/configure \
--prefix=$CLANG_INSTALL \
--target=$TARGET_TRIPLE \
--enable-newlib-io-long-double \
--enable-newlib-io-long-long \
--enable-newlib-io-c99-formats \
--enable-newlib-register-fini \
--disable-multilib \
--disable-nls
make $JOBS all
make install
cd $BUILD_ROOT

mkdir -p $BUILD_COMPILER_RT
cd $BUILD_COMPILER_RT
export LLVM_VERSION=`clang -dumpversion`
export LLVM_RESOURCEDIR=lib/clang/$LLVM_VERSION
export COMPILER_RT_INSTALL=$CLANG_INSTALL/$LLVM_RESOURCEDIR
cmake \
-G Ninja \
-DCMAKE_INSTALL_PREFIX=$COMPILER_RT_INSTALL \
-DCMAKE_BUILD_TYPE=$BUILE_TYPE \
-DCMAKE_TRY_COMPILE_TARGET_TYPE=STATIC_LIBRARY \
-DCMAKE_CROSSCOMPILING=True \
-DCMAKE_SYSTEM_NAME=Linux \
-DCOMPILER_RT_BUILD_BUILTINS=ON \
-DCOMPILER_RT_INCLUDE_TESTS=OFF \
-DCOMPILER_RT_BUILD_CRT=ON \
-DCOMPILER_RT_BUILD_SANITIZERS=OFF \
-DCOMPILER_RT_BUILD_XRAY=OFF \
-DCOMPILER_RT_BUILD_LIBFUZZER=OFF \
-DCOMPILER_RT_BUILD_PROFILE=OFF \
-DCOMPILER_RT_BUILD_MEMPROF=OFF \
-DCOMPILER_RT_BUILD_ORC=OFF \
-DCOMPILER_RT_DEFAULT_TARGET_ONLY=ON \
-DCOMPILER_RT_BUILD_XRAY_NO_PREINIT=OFF \
-DCOMPILER_RT_SANITIZERS_TO_BUILD=none \
-DCOMPILER_RT_BAREMETAL_BUILD=ON \
-DCOMPILER_RT_OS_DIR="" \
-DCMAKE_ASM_COMPILER=clang \
-DCMAKE_C_COMPILER=clang \
-DCMAKE_CXX_COMPILER=clang++ \
-DCMAKE_ASM_COMPILER_TARGET=$TARGET_TRIPLE \
-DCMAKE_C_COMPILER_TARGET=$TARGET_TRIPLE \
-DCMAKE_CXX_COMPILER_TARGET=$TARGET_TRIPLE \
-DCMAKE_SYSROOT=$NEWLIB_SYSROOT \
$SRC_COMPILER_RT
ninja
ninja install
