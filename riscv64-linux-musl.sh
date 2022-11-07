#!/bin/bash

export TOP=$PWD
export JOBS=-j32

export CLANG_INSTALL=/home/liujia/riscv-linux-musl-clang
export PATH=$CLANG_INSTALL/bin:$PATH
export MUSL_SYSROOT=$CLANG_INSTALL/sysroot

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

export TARGET_TRIPLE=riscv64-unknown-linux-musl
export TARGET_CLANG_CFLAGS="--target=$TARGET_TRIPLE --sysroot=$MUSL_SYSROOT"
export TARGET_CLANG_CXXFLAGS=$TARGET_CLANG_CFLAGS
export TARGET_CLANG_LDFLAGS="-fuse-ld=lld"

export TOOLS_TO_BUILD="clang;lld"
export TARGETS_TO_BUILD="RISCV"
export BUILE_TYPE=Release

export TARBALL_ROOT=$TOP/tarballs
export STAMPS_ROOT=$TOP/stamps

export SRC_ROOT=$TOP/src
export SRC_MUSL=$SRC_ROOT/musl-$MUSL_VER
export SRC_LINUX=$SRC_ROOT/linux-$LINUX_VER
export LLVM_SRC_ROOT=$SRC_ROOT/llvm-project
export SRC_LLVM=$LLVM_SRC_ROOT/llvm
export SRC_COMPILER_RT=$LLVM_SRC_ROOT/compiler-rt
export SRC_LIBUNWIND=$LLVM_SRC_ROOT/libunwind
export SRC_LIBCXX=$LLVM_SRC_ROOT/libcxx
export SRC_LIBCXXABI=$LLVM_SRC_ROOT/libcxxabi

export BUILD_ROOT=$TOP/build-musl
export BUILD_MUSL_HEADERS=$BUILD_ROOT/musl-headers
export BUILD_MUSL=$BUILD_ROOT/musl
export BUILD_CLANG=$BUILD_ROOT/clang
export BUILD_COMPILER_RT=$BUILD_ROOT/compiler-rt
export BUILD_LIBUNWIND=$BUILD_ROOT/libunwind
export BUILD_LIBCXX=$BUILD_ROOT/libcxx
export BUILD_LIBCXXABI=$BUILD_ROOT/libcxxabi

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

cd $SRC_LINUX
make ARCH=riscv CROSS_COMPILE=$TARGET_TRIPLE- defconfig
make ARCH=riscv INSTALL_HDR_PATH=$MUSL_SYSROOT/usr headers_install
cd $BUILD_ROOT

mkdir -p $BUILD_MUSL_HEADERS
cd $BUILD_MUSL_HEADERS
CC=$TARGET_TRIPLE-clang \
$SRC_MUSL/configure \
--host=$TARGET_TRIPLE \
--prefix=$MUSL_SYSROOT/usr \
--enable-shared \
--with-headers=$MUSL_SYSROOT/usr/include \
--disable-multilib \
--enable-kernel=3.0.0
make install-headers
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
-DCOMPILER_RT_BAREMETAL_BUILD=OFF \
-DCOMPILER_RT_OS_DIR="linux" \
-DCMAKE_ASM_COMPILER=clang \
-DCMAKE_C_COMPILER=clang \
-DCMAKE_CXX_COMPILER=clang++ \
-DCMAKE_ASM_COMPILER_TARGET=$TARGET_TRIPLE \
-DCMAKE_C_COMPILER_TARGET=$TARGET_TRIPLE \
-DCMAKE_CXX_COMPILER_TARGET=$TARGET_TRIPLE \
-DCMAKE_SYSROOT=$MUSL_SYSROOT \
$SRC_COMPILER_RT
ninja
ninja install
cd $BUILD_ROOT

# export LLVM_VERSION=`clang -dumpversion`
# export LLVM_RESOURCEDIR=lib/clang/$LLVM_VERSION
# export COMPILER_RT_INSTALL=$CLANG_INSTALL/$LLVM_RESOURCEDIR
mkdir -p $BUILD_MUSL
cd $BUILD_MUSL
CC=$TARGET_TRIPLE-clang \
CXX=$TARGET_TRIPLE-clang++ \
CFLAGS="$TARGET_CLANG_CFLAGS -g -O2" \
CXXFLAGS=" $TARGET_CLANG_CXXFLAGS -g -O2" \
ASFLAGS=$TARGET_CLANG_CFLAGS \
CROSS_COMPILE=$CLANG_INSTALL/bin/$TARGET_TRIPLE- \
LIBCC=$COMPILER_RT_INSTALL/lib/linux/libclang_rt.builtins-riscv64.a \
$SRC_MUSL/configure \
--host=$TARGET_TRIPLE \
--prefix=$MUSL_SYSROOT \
--disable-werror \
--enable-shared
make $JOBS
DESTDIR=/ make install
cd $BUILD_ROOT

# mkdir -p $BUILD_LIBUNWIND
# cd $BUILD_LIBUNWIND
# cmake \
# -G Ninja \
# -DLIBUNWIND_USE_COMPILER_RT=ON \
# -DCMAKE_ASM_COMPILER=$CLANG_INSTALL/bin/clang \
# -DCMAKE_C_COMPILER=$CLANG_INSTALL/bin/clang \
# -DCMAKE_CXX_COMPILER=$CLANG_INSTALL/bin/clang++ \
# -DCMAKE_ASM_COMPILER_TARGET=$TARGET_TRIPLE \
# -DCMAKE_C_COMPILER_TARGET=$TARGET_TRIPLE \
# -DCMAKE_CXX_COMPILER_TARGET=$TARGET_TRIPLE \
# -DCMAKE_C_FLAGS=$TARGET_CLANG_CFLAGS \
# -DCMAKE_CXX_FLAGS=$TARGET_CLANG_CXXFLAGS \
# -DCMAKE_ASM_FLAGS=$TARGET_CLANG_CFLAGS \
# -DCMAKE_SHARED_LINKER_FLAGS=$TARGET_CLANG_LDFLAGS \
# -DCMAKE_SYSROOT=$MUSL_SYSROOT \
# -DCMAKE_INSTALL_PREFIX=$MUSL_SYSROOT \
# $SRC_LIBUNWIND
#-DCMAKE_SHARED_LINKER_FLAGS="$TARGET_CLANG_LDFLAGS -unwindlib=none" \
# ninja
# ninja install
# cd $BUILD_ROOT

# mkdir -p $BUILD_LIBCXX
# cd $BUILD_LIBCXX
# cmake ../ -G Ninja \
# -DLIBCXXABI_USE_LLVM_UNWINDER=ON \
# -DLIBCXX_HAS_MUSL_LIBC=ON \
# -DCMAKE_C_COMPILER=$CLANG_INSTALL/bin/clang \
# -DCMAKE_CXX_COMPILER=$CLANG_INSTALL/bin/clang++ \
# -DCMAKE_C_COMPILER_TARGET=$TARGET_TRIPLE \
# -DCMAKE_CXX_COMPILER_TARGET=$TARGET_TRIPLE \
# -DCMAKE_C_FLAGS=$TARGET_CLANG_CFLAGS \
# -DCMAKE_CXX_FLAGS=$TARGET_CLANG_CXXFLAGS \
# -DCMAKE_SYSROOT=$MUSL_SYSROOT \
# -DCMAKE_INSTALL_PREFIX=$MUSL_SYSROOT \
# $SRC_LIBCXX
# ninja
# ninja install
# cd $BUILD_ROOT

# mkdir -p $BUILD_LIBCXXABI
# cd $BUILD_LIBCXXABI
# cmake \
# -G Ninja \
# -DLIBCXXABI_USE_LLVM_UNWINDER=ON \
# -DCMAKE_C_COMPILER=$CLANG_INSTALL/bin/clang \
# -DCMAKE_CXX_COMPILER=$CLANG_INSTALL/bin/clang++ \
# -DCMAKE_C_COMPILER_TARGET=$TARGET_TRIPLE \
# -DCMAKE_CXX_COMPILER_TARGET=$TARGET_TRIPLE \
# -DCMAKE_C_FLAGS=$TARGET_CLANG_CFLAGS \
# -DCMAKE_CXX_FLAGS=$TARGET_CLANG_CXXFLAGS \
# -DCMAKE_SYSROOT=$MUSL_SYSROOT \
# -DCMAKE_INSTALL_PREFIX=$MUSL_SYSROOT \
# $SRC_LIBCXXABI
# ninja
# ninja install
# cd $BUILD_ROOT
