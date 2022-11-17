#!/usr/bin/env zsh

set_custom_env() {
  export CLANG_PREFIX=<PREFIX>
  export BUILD_TYPE=Release
  export WITH_MUSL=ON
  export WITH_NEWLIB=ON
  export WITH_QEMU=ON
}

set_env() {
  export TOP=`pwd`
  export JOBS="-j32"
  export SRC_ROOT=${TOP}/src
  export BUILD_ROOT=${TOP}/build
  export PATCH_ROOT=${TOP}/patch
  export TARBALL_ROOT=${TOP}/tarball

  export CLANG_BIN=${CLANG_PREFIX}/bin
  export PATH=${CLANG_BIN}:$PATH

  export MUSL_TRIPLE="riscv64-unknown-linux-musl"
  export NEWLIB_TRIPLE="riscv64-unknown-elf"

  export NEWLIB_SYSROOT=${CLANG_PREFIX}/${NEWLIB_TRIPLE}
  export MUSL_SYSROOT=${CLANG_PREFIX}/sysroot

  export TOOLS_TO_BUILD="clang;lld"
  export RUNTIMES_TO_BUILD="libcxx;libcxxabi;libunwind"
  export TARGETS_TO_BUILD="RISCV"

  if [[ `uname` == "Darwin" ]] {
    export QEMU_TARGET="riscv64-softmmu"
  } elif [[ `uname` == "Linux" ]] {
    export QEMU_TARGET="riscv64-softmmu,riscv64-linux-user"
  } else {
    export QEMU_TARGET="riscv64-softmmu"
  }

  export MUSL_FLAGS="--target=${MUSL_TRIPLE} --sysroot=${MUSL_SYSROOT}"
  export NEWLIB_FLAGS="--target=${NEWLIB_TRIPLE} --sysroot=${NEWLIB_SYSROOT}"
  export RUNTIMES_FLAGS="-ffunction-sections -fdata-sections -fno-ident"
  export MUSL_RUNTIMES_FLAGS="${MUSL_FLAGS} ${RUNTIMES_FLAGS}"
  export NEWLIB_RUNTIMES_FLAGS="${NEWLIB_FLAGS} ${RUNTIMES_FLAGS}"
  export CLANG_LDFLAGS="-fuse-ld=lld"
  export GNU_C89_FLAG="-Wno-unused-command-line-argument"
  export CROSS_MUSL_FLAGS="${MUSL_FLAGS} ${GNU_C89_FLAG}"
  export CROSS_NEWLIB_FLAGS="${NEWLIB_FLAGS} ${GNU_C89_FLAG}"

  export NEWLIB_VER="4.2.0.20211231"
  export MUSL_VER="1.2.3"
  export QEMU_VER="7.1.0"

  export SUFFIX_XZ="tar.xz"
  export SUFFIX_GZ="tar.gz"

  export NEWLIB_TARBALL=newlib-${NEWLIB_VER}.${SUFFIX_GZ}
  export MUSL_TARBALL=musl-${MUSL_VER}.${SUFFIX_GZ}
  export QEMU_TARBALL=qemu-${QEMU_VER}.${SUFFIX_XZ}

  export MUSL_SITE="https://musl.libc.org/releases/"
  export MUSL_URL=${MUSL_SITE}${MUSL_TARBALL}
  export NEWLIB_SITE="http://sourceware.org/pub/newlib/"
  export NEWLIB_URL=${NEWLIB_SITE}${NEWLIB_TARBALL}
  export QEMU_SITE="https://download.qemu.org/"
  export QEMU_URL=${QEMU_SITE}${QEMU_TARBALL}
  export LLVM_GIT_URL="https://github.com/llvm/llvm-project.git"

  export LIBCXX_MATH_PATCH=llvm-HEAD.patch
  export LIBCXX_PATCH=${PATCH_ROOT}/${LIBCXX_MATH_PATCH}
  export NEWLIB_C99_PATCH=newlib-4.2.0.20211231-C99-build.diff
  export NEWLIB_PATCH=${PATCH_ROOT}/${NEWLIB_C99_PATCH}

  export LIBCXX_PATCH_FLAG=${SRC_ROOT}/libcxx_patched
  export NEWLIB_PATCH_FLAG=${SRC_ROOT}/newlib_patched

  export LLVM_PROJ_ROOT=${SRC_ROOT}/llvm-project
  export SRC_LLVM=${LLVM_PROJ_ROOT}/llvm
  export SRC_COMPILER_RT=${LLVM_PROJ_ROOT}/compiler-rt
  export SRC_RUNTIMES=${LLVM_PROJ_ROOT}/runtimes
  export SRC_LINUX_HEADER=${SRC_ROOT}/linux-headers
  export SRC_MUSL=${SRC_ROOT}/musl-${MUSL_VER}
  export SRC_NEWLIB=${SRC_ROOT}/newlib-${NEWLIB_VER}
  export SRC_QEMU=${SRC_ROOT}/qemu-${QEMU_VER}

  export BUILD_CLANG=${BUILD_ROOT}/clang
  export BUILD_MUSL_HEADER=${BUILD_ROOT}/musl-header
  export BUILD_NEWLIB=${BUILD_ROOT}/newlib
  export BUILD_COMPILER_RT_NEWLIB=${BUILD_ROOT}/compiler-rt-newlib
  export BUILD_COMPILER_RT_MUSL=${BUILD_ROOT}/compiler-rt-musl
  export BUILD_MUSL=${BUILD_ROOT}/musl
  export BUILD_RUNTIMES_NEWLIB=${BUILD_ROOT}/runtimes-newlib
  export BUILD_RUNTIMES_MUSL=${BUILD_ROOT}/runtimes-musl
  export BUILD_QEMU=${BUILD_ROOT}/qemu
}

makedir() {
  if [[ -d ${BUILD_ROOT} ]] {
    echo -e "I: ${BUILD_ROOT} already exist"
  } else {
    mkdir -p ${BUILD_ROOT}
  }

  if [[ -d ${TARBALL_ROOT} ]] {
    echo -e "I: ${TARBALL_ROOT} already exist"
  } else {
    mkdir -p ${TARBALL_ROOT}
  }
}

download() {
  cd ${TARBALL_ROOT}
  if [[ -f ${MUSL_TARBALL} ]] {
    echo -e "I: ${MUSL_TARBALL} already downloaded"
  } else {
    curl -O ${MUSL_URL}
  }

  if [[ -f ${NEWLIB_TARBALL} ]] {
    echo -e "I: ${NEWLIB_TARBALL} already downloaded"
  } else {
    curl -O ${NEWLIB_URL}
  }

  if [[ -f ${QEMU_TARBALL} ]] {
    echo -e "I: ${QEMU_TARBALL} already downloaded"
  } else {
    curl -O ${QEMU_URL}
  }

  if [[ -e ${LLVM_PROJ_ROOT} ]] {
    echo -e "I: ${LLVM_PROJ_ROOT} already downloaded"
  } else {
    cd ${SRC_ROOT}
    git clone ${LLVM_GIT_URL}
  }
}

unpack() {
  cd ${SRC_ROOT}
  if [[ -d ${SRC_MUSL} ]] {
    echo -e "I: ${SRC_MUSL} already exist"
  } else {
    tar xf ${TARBALL_ROOT}/${MUSL_TARBALL}
  }

  if [[ -d ${SRC_NEWLIB} ]] {
    echo -e "I: ${SRC_NEWLIB} already exist"
  } else {
    tar xf ${TARBALL_ROOT}/${NEWLIB_TARBALL}
  }

  if [[ -d ${SRC_QEMU} ]] {
    echo -e "I: ${SRC_QEMU} already exist"
  } else {
    tar xf ${TARBALL_ROOT}/${QEMU_TARBALL}
  }
}

patch_src() {
  if [[ -e ${LIBCXX_PATCH_FLAG} ]] {
    echo -e "I: libcxx already patched"
  } else {
    cd ${LLVM_PROJ_ROOT}
    patch -p1 < ${LIBCXX_PATCH}
    touch ${LIBCXX_PATCH_FLAG}
  }
}

process_clang() {
  if [[ -d ${BUILD_CLANG} ]] {
    echo -e "I: ${BUILD_CLANG} already exist"
  } else {
    mkdir -p ${BUILD_CLANG}
  }
  cd ${BUILD_CLANG}
  cmake \
  -G Ninja \
  -DLLVM_ENABLE_PROJECTS=${TOOLS_TO_BUILD} \
  -DCMAKE_BUILD_TYPE=${BUILD_TYPE} \
  -DCMAKE_INSTALL_PREFIX=${CLANG_PREFIX} \
  -DLLVM_TARGETS_TO_BUILD=${TARGETS_TO_BUILD} \
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
}

post_process_clang_musl() {
  cd ${CLANG_BIN}
  ARG='"$@"'
  echo "${CLANG_BIN}/clang ${CROSS_MUSL_FLAGS} ${ARG}" > ${MUSL_TRIPLE}-clang
  echo "${CLANG_BIN}/clang++ ${CROSS_MUSL_FLAGS} ${ARG}" > ${MUSL_TRIPLE}-clang++
  chmod +x ${MUSL_TRIPLE}-clang
  chmod +x ${MUSL_TRIPLE}-clang++
  ln -s ${MUSL_TRIPLE}-clang ${MUSL_TRIPLE}-gcc
  ln -s ${MUSL_TRIPLE}-clang++ ${MUSL_TRIPLE}-g++
  ln -s lld ${MUSL_TRIPLE}-ld
  ln -s lld ${MUSL_TRIPLE}-ld.lld
  ln -s lld ${MUSL_TRIPLE}-ld64.lld
  for i (ar nm objcopy objdump ranlib strip) {
    ln -s llvm-$i ${MUSL_TRIPLE}-$i
  }
}

post_process_clang_newlib() {
  cd ${CLANG_BIN}
  ARG='"$@"'
  echo "${CLANG_BIN}/clang ${CROSS_NEWLIB_FLAGS} ${ARG}" > ${NEWLIB_TRIPLE}-clang
  echo "${CLANG_BIN}/clang++ ${CROSS_NEWLIB_FLAGS} ${ARG}" > ${NEWLIB_TRIPLE}-clang++
  chmod +x ${NEWLIB_TRIPLE}-clang
  chmod +x ${NEWLIB_TRIPLE}-clang++
  ln -s ${NEWLIB_TRIPLE}-clang ${NEWLIB_TRIPLE}-gcc
  ln -s ${NEWLIB_TRIPLE}-clang++ ${NEWLIB_TRIPLE}-g++
  ln -s lld ${NEWLIB_TRIPLE}-ld
  ln -s lld ${NEWLIB_TRIPLE}-ld.lld
  ln -s lld ${NEWLIB_TRIPLE}-ld64.lld
  for i (ar nm objcopy objdump ranlib strip) {
    ln -s llvm-$i ${NEWLIB_TRIPLE}-$i
  }
}

process_linux_header() {
  cd ${SRC_LINUX_HEADER}
  mkdir -p ${MUSL_SYSROOT}/usr/
  cp -r include ${MUSL_SYSROOT}/usr/
}

process_musl_header() {
  if [[ -d ${BUILD_MUSL_HEADER} ]] {
    echo -e "I: ${BUILD_MUSL_HEADER} already exist"
  } else {
    mkdir -p ${BUILD_MUSL_HEADER}
  }
  cd ${BUILD_MUSL_HEADER}
  $SRC_MUSL/configure \
  --host=${MUSL_TRIPLE} \
  --prefix=${MUSL_SYSROOT}/usr \
  --enable-shared \
  --with-headers=${MUSL_SYSROOT}/usr/include \
  --disable-multilib \
  --enable-kernel=3.0.0
  make install-headers
}

process_newlib () {
  if [[ -d ${BUILD_NEWLIB} ]] {
    echo -e "I: ${BUILD_NEWLIB} already exist"
  } else {
    mkdir -p ${BUILD_NEWLIB}
  }
  cd ${BUILD_NEWLIB}
  export CFLAGS_FOR_TARGET=" -Wno-int-conversion -g -gdwarf-3 -gstrict-dwarf -O2 -ffunction-sections -fdata-sections "
  export CC_FOR_TARGET=${NEWLIB_TRIPLE}-clang
  export AS_FOR_TARGET=${NEWLIB_TRIPLE}-clang
  export LD_FOR_TARGET=lld
  export CXX_FOR_TARGET=${NEWLIB_TRIPLE}-clang++
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
  CFLAGS=-D_GNU_SOURCE='' \
  --prefix=${CLANG_PREFIX} \
  --target=${NEWLIB_TRIPLE} \
  --enable-newlib-io-long-double \
  --enable-newlib-io-long-long \
  --enable-newlib-io-c99-formats \
  --enable-newlib-register-fini \
  --disable-multilib \
  --disable-nls
  make ${JOBS} all
  make install
}

set_compiler_rt_prefix() {
  export LLVM_VERSION=`clang -dumpversion`
  export LLVM_RESOURCEDIR=lib/clang/${LLVM_VERSION}
  export COMPILER_RT_INSTALL=${CLANG_PREFIX}/${LLVM_RESOURCEDIR}
}

process_compiler_rt_musl() {
  if [[ -d ${BUILD_COMPILER_RT_MUSL} ]] {
    echo -e "I: ${BUILD_COMPILER_RT_MUSL} already exist"
  } else {
    mkdir -p ${BUILD_COMPILER_RT_MUSL}
  }
  cd ${BUILD_COMPILER_RT_MUSL}
  set_compiler_rt_prefix
  cmake \
  -G Ninja \
  -DCMAKE_AR=${CLANG_BIN}/llvm-ar \
  -DCMAKE_ASM_COMPILER_TARGET=${MUSL_TRIPLE} \
  -DCMAKE_ASM_FLAGS=${MUSL_RUNTIMES_FLAGS} \
  -DCMAKE_CXX_COMPILER=${CLANG_BIN}/clang++ \
  -DCMAKE_CXX_COMPILER_TARGET=${MUSL_TRIPLE} \
  -DCMAKE_CXX_FLAGS=${MUSL_RUNTIMES_FLAGS} \
  -DCMAKE_C_COMPILER=${CLANG_BIN}/clang \
  -DCMAKE_C_COMPILER_TARGET=${MUSL_TRIPLE} \
  -DCMAKE_C_FLAGS=${MUSL_RUNTIMES_FLAGS} \
  -DCMAKE_EXE_LINKER_FLAGS=${CLANG_LDFLAGS} \
  -DCMAKE_NM=${CLANG_BIN}/llvm-nm \
  -DCMAKE_RANLIB=${CLANG_BIN}/llvm-ranlib \
  -DLLVM_CONFIG_PATH=${CLANG_BIN}/llvm-config \
  -DCMAKE_SYSROOT=${MUSL_SYSROOT} \
  -DCMAKE_INSTALL_PREFIX=${COMPILER_RT_INSTALL} \
  -DCMAKE_BUILD_TYPE=${BUILD_TYPE} \
  -DCMAKE_TRY_COMPILE_TARGET_TYPE=STATIC_LIBRARY \
  -DCMAKE_CROSSCOMPILING=True \
  -DCMAKE_SYSTEM_NAME=Linux \
  -DCOMPILER_RT_BUILD_BUILTINS=ON \
  -DCOMPILER_RT_INCLUDE_TESTS=OFF \
  -DCOMPILER_RT_BUILD_CRT=ON \
  -DCOMPILER_RT_BUILD_SANITIZERS=OFF \
  -DCOMPILER_RT_BUILD_XRAY=OFF \
  -DCOMPILER_RT_BUILD_LIBFUZZER=OFF \
  -DCOMPILER_RT_BUILD_PROFILE=ON \
  -DCOMPILER_RT_BUILD_MEMPROF=OFF \
  -DCOMPILER_RT_BUILD_ORC=OFF \
  -DCOMPILER_RT_DEFAULT_TARGET_ONLY=ON \
  -DCOMPILER_RT_BUILD_XRAY_NO_PREINIT=OFF \
  -DCOMPILER_RT_SANITIZERS_TO_BUILD=none \
  -DCOMPILER_RT_BAREMETAL_BUILD=OFF \
  -DCOMPILER_RT_OS_DIR="linux" \
  ${SRC_COMPILER_RT}
  ninja
  ninja install
}

process_compiler_rt_newlib() {
  if [[ -d ${BUILD_COMPILER_RT_NEWLIB} ]] {
    echo -e "I: ${BUILD_COMPILER_RT_NEWLIB} already exist"
  } else {
    mkdir -p ${BUILD_COMPILER_RT_NEWLIB}
  }
  cd ${BUILD_COMPILER_RT_NEWLIB}
  set_compiler_rt_prefix
  cmake \
  -G Ninja \
  -DCMAKE_AR=${CLANG_BIN}/llvm-ar \
  -DCMAKE_ASM_COMPILER_TARGET=${NEWLIB_TRIPLE} \
  -DCMAKE_ASM_FLAGS=${NEWLIB_RUNTIMES_FLAGS} \
  -DCMAKE_CXX_COMPILER=${CLANG_BIN}/clang++ \
  -DCMAKE_CXX_COMPILER_TARGET=${NEWLIB_TRIPLE} \
  -DCMAKE_CXX_FLAGS=${NEWLIB_RUNTIMES_FLAGS} \
  -DCMAKE_C_COMPILER=${CLANG_BIN}/clang \
  -DCMAKE_C_COMPILER_TARGET=${NEWLIB_TRIPLE} \
  -DCMAKE_C_FLAGS=${NEWLIB_RUNTIMES_FLAGS} \
  -DCMAKE_EXE_LINKER_FLAGS=${CLANG_LDFLAGS} \
  -DCMAKE_NM=${CLANG_BIN}/llvm-nm \
  -DCMAKE_RANLIB=${CLANG_BIN}/llvm-ranlib \
  -DLLVM_CONFIG_PATH=${CLANG_BIN}/llvm-config \
  -DCMAKE_SYSROOT=${NEWLIB_SYSROOT} \
  -DCMAKE_INSTALL_PREFIX=${COMPILER_RT_INSTALL} \
  -DCMAKE_BUILD_TYPE=${BUILD_TYPE} \
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
  ${SRC_COMPILER_RT}
  ninja
  ninja install
}

process_musl() {
  if [[ -d ${BUILD_MUSL} ]] {
    echo -e "I: ${BUILD_MUSL} already exist"
  } else {
    mkdir -p ${BUILD_MUSL}
  }
  cd ${BUILD_MUSL}
  set_compiler_rt_prefix
  CC=clang \
  CXX=clang++ \
  CFLAGS=${MUSL_FLAGS} \
  CXXFLAGS=${MUSL_FLAGS} \
  ASFLAGS=${MUSL_FLAGS} \
  CROSS_COMPILE=clang \
  LIBCC=${COMPILER_RT_INSTALL}/lib/linux/libclang_rt.builtins-riscv64.a
  $SRC_MUSL/configure \
  --target=${MUSL_TRIPLE} \
  --host=${MUSL_TRIPLE} \
  --prefix=${MUSL_SYSROOT} \
  --syslibdir=${MUSL_SYSROOT}/lib \
  --disable-werror \
  --enable-shared
  make ${JOBS}
  make install
}

process_runtimes_musl() {
  if [[ -d ${BUILD_RUNTIMES_MUSL} ]] {
    echo -e "I: ${BUILD_RUNTIMES_MUSL} already exist"
  } else {
    mkdir -p ${BUILD_RUNTIMES_MUSL}
  }
  cd ${BUILD_RUNTIMES_MUSL}
  cmake \
  -G Ninja \
  -DCMAKE_AR=${CLANG_BIN}/llvm-ar \
  -DCMAKE_ASM_FLAGS=${MUSL_RUNTIMES_FLAGS} \
  -DCMAKE_BUILD_TYPE=${BUILD_TYPE} \
  -DCMAKE_CXX_COMPILER=${CLANG_BIN}/clang++ \
  -DCMAKE_CXX_COMPILER_TARGET=${MUSL_TRIPLE} \
  -DCMAKE_CXX_FLAGS=${MUSL_RUNTIMES_FLAGS} \
  -DCMAKE_C_COMPILER=${CLANG_BIN}/clang \
  -DCMAKE_C_COMPILER_TARGET=${MUSL_TRIPLE} \
  -DCMAKE_C_FLAGS=${MUSL_RUNTIMES_FLAGS} \
  -DCMAKE_EXE_LINKER_FLAGS=${CLANG_LDFLAGS} \
  -DCMAKE_INSTALL_PREFIX=${MUSL_SYSROOT} \
  -DCMAKE_NM=${CLANG_BIN}/llvm-nm \
  -DCMAKE_RANLIB=${CLANG_BIN}/llvm-ranlib \
  -DCMAKE_TRY_COMPILE_TARGET_TYPE=STATIC_LIBRARY \
  -DLIBCXXABI_BAREMETAL=OFF \
  -DLIBCXXABI_ENABLE_ASSERTIONS=OFF \
  -DLIBCXXABI_ENABLE_SHARED=OFF \
  -DLIBCXXABI_ENABLE_STATIC=ON \
  -DLIBCXXABI_LIBCXX_INCLUDES=${MUSL_SYSROOT}/include/c++/v1 \
  -DLIBCXXABI_USE_COMPILER_RT=ON \
  -DLIBCXXABI_USE_LLVM_UNWINDER=OFF \
  -DLIBCXX_CXX_ABI=libcxxabi \
  -DLIBCXX_ENABLE_DEBUG_MODE_SUPPORT=OFF \
  -DLIBCXX_ENABLE_FILESYSTEM=OFF \
  -DLIBCXX_ENABLE_SHARED=OFF \
  -DLIBCXX_ENABLE_STATIC=ON \
  -DLIBCXX_INCLUDE_BENCHMARKS=OFF \
  -DLIBUNWIND_ENABLE_SHARED=OFF \
  -DLIBUNWIND_ENABLE_STATIC=ON \
  -DLIBUNWIND_IS_BAREMETAL=OFF \
  -DLIBUNWIND_REMEMBER_HEAP_ALLOC=ON \
  -DLIBUNWIND_USE_COMPILER_RT=ON \
  -DLLVM_ENABLE_RUNTIMES=${RUNTIMES_TO_BUILD} \
  -DLIBCXXABI_ENABLE_EXCEPTIONS=OFF \
  -DLIBCXXABI_ENABLE_THREADS=OFF \
  -DLIBCXX_ENABLE_EXCEPTIONS=OFF \
  -DLIBCXX_ENABLE_MONOTONIC_CLOCK=OFF \
  -DLIBCXX_ENABLE_RANDOM_DEVICE=OFF \
  -DLIBCXX_ENABLE_RTTI=OFF \
  -DLIBCXX_ENABLE_THREADS=OFF \
  -DLIBCXX_ENABLE_WIDE_CHARACTERS=ON \
  -DLIBCXX_ENABLE_LOCALIZATION=OFF \
  -DLIBCXX_EXTRA_SITE_DEFINES=_USE_EXTENDED_LOCALES_ \
  -DLIBUNWIND_ENABLE_THREADS=OFF \
  ${SRC_RUNTIMES}
  ninja cxx
  ninja cxxabi
  ninja unwind
  ninja install-cxx
  ninja install-cxxabi
  ninja install-unwind
}

process_runtimes_newlib() {
  if [[ -d ${BUILD_RUNTIMES_NEWLIB} ]] {
    echo -e "I: ${BUILD_RUNTIMES_NEWLIB} already exist"
  } else {
    mkdir -p ${BUILD_RUNTIMES_NEWLIB}
  }
  cd ${BUILD_RUNTIMES_NEWLIB}
  cmake \
  -G Ninja \
  -DCMAKE_AR=${CLANG_BIN}/llvm-ar \
  -DCMAKE_ASM_FLAGS=${NEWLIB_RUNTIMES_FLAGS} \
  -DCMAKE_BUILD_TYPE=${BUILD_TYPE} \
  -DCMAKE_CXX_COMPILER=${CLANG_BIN}/clang++ \
  -DCMAKE_CXX_COMPILER_TARGET=${NEWLIB_TRIPLE} \
  -DCMAKE_CXX_FLAGS=${NEWLIB_RUNTIMES_FLAGS} \
  -DCMAKE_C_COMPILER=${CLANG_BIN}/clang \
  -DCMAKE_C_COMPILER_TARGET=${NEWLIB_TRIPLE} \
  -DCMAKE_C_FLAGS=${NEWLIB_RUNTIMES_FLAGS} \
  -DCMAKE_EXE_LINKER_FLAGS=${CLANG_LDFLAGS} \
  -DCMAKE_INSTALL_PREFIX=${NEWLIB_SYSROOT} \
  -DCMAKE_NM=${CLANG_BIN}/llvm-nm \
  -DCMAKE_RANLIB=${CLANG_BIN}/llvm-ranlib \
  -DCMAKE_TRY_COMPILE_TARGET_TYPE=STATIC_LIBRARY \
  -DLIBCXXABI_BAREMETAL=ON \
  -DLIBCXXABI_ENABLE_ASSERTIONS=OFF \
  -DLIBCXXABI_ENABLE_SHARED=OFF \
  -DLIBCXXABI_ENABLE_STATIC=ON \
  -DLIBCXXABI_LIBCXX_INCLUDES=${NEWLIB_SYSROOT}/include/c++/v1 \
  -DLIBCXXABI_USE_COMPILER_RT=ON \
  -DLIBCXXABI_USE_LLVM_UNWINDER=ON \
  -DLIBCXX_CXX_ABI=libcxxabi \
  -DLIBCXX_ENABLE_DEBUG_MODE_SUPPORT=OFF \
  -DLIBCXX_ENABLE_FILESYSTEM=OFF \
  -DLIBCXX_ENABLE_SHARED=OFF \
  -DLIBCXX_ENABLE_STATIC=ON \
  -DLIBCXX_INCLUDE_BENCHMARKS=OFF \
  -DLIBUNWIND_ENABLE_SHARED=OFF \
  -DLIBUNWIND_ENABLE_STATIC=ON \
  -DLIBUNWIND_IS_BAREMETAL=ON \
  -DLIBUNWIND_REMEMBER_HEAP_ALLOC=ON \
  -DLIBUNWIND_USE_COMPILER_RT=ON \
  -DLLVM_ENABLE_RUNTIMES=${RUNTIMES_TO_BUILD} \
  -DLIBCXXABI_ENABLE_EXCEPTIONS=OFF \
  -DLIBCXXABI_ENABLE_THREADS=OFF \
  -DLIBCXX_ENABLE_EXCEPTIONS=OFF \
  -DLIBCXX_ENABLE_MONOTONIC_CLOCK=OFF \
  -DLIBCXX_ENABLE_RANDOM_DEVICE=OFF \
  -DLIBCXX_ENABLE_RTTI=OFF \
  -DLIBCXX_ENABLE_THREADS=OFF \
  -DLIBCXX_ENABLE_WIDE_CHARACTERS=ON \
  -DLIBCXX_EXTRA_SITE_DEFINES=_LIBCPP_PROVIDES_DEFAULT_RUNE_TABLE \
  -DLIBUNWIND_ENABLE_THREADS=OFF \
  ${SRC_RUNTIMES}
  ninja cxx
  ninja cxxabi
  ninja unwind
  ninja install-cxx
  ninja install-cxxabi
  ninja install-unwind
}

process_qemu() {
  if [[ -d ${BUILD_QEMU} ]] {
    echo -e "I: ${BUILD_QEMU} already exist"
  } else {
    mkdir -p ${BUILD_QEMU}
  }
  cd ${BUILD_QEMU}
  ${SRC_QEMU}/configure \
  --prefix=${CLANG_PREFIX} \
  --target-list=riscv64-softmmu,riscv64-linux-user
  make ${JOBS}
  make install
}

set_custom_env
set_env
makedir
download
unpack
patch_src

process_clang


if [[ ${WITH_MUSL} == "ON" ]] {
  post_process_clang_musl
  process_linux_header
  process_musl_header
  process_compiler_rt_musl
  process_musl
  process_runtimes_musl
}

if [[ ${WITH_PICOLIBC} == "ON" ]] {
  post_process_clang_newlib
  process_newlib
  process_compiler_rt_newlib
  process_runtimes_newlib
}

if [[ ${WITH_QEMU} == "ON" ]] {
  process_qemu
}
