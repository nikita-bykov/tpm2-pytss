#!/usr/bin/env bash
# SPDX-License-Identifier: BSD-2-Clause

set -exo pipefail

export TPM2_TSS_VERSION=${TPM2_TSS_VERSION:-"3.0.3"}

#
# Get dependencies for building and install tpm2-tss and abrmd projects
#
export DEBIAN_FRONTEND=noninteractive
sudo apt-get update
sudo apt-get install -y \
    autoconf-archive \
    curl \
    libcmocka0 \
    libcmocka-dev \
    net-tools \
    build-essential \
    git \
    pkg-config \
    gcc \
    g++ \
    m4 \
    libtool \
    automake \
    libgcrypt20-dev \
    libssl-dev \
    autoconf \
    gnulib \
    wget \
    doxygen \
    lcov \
    libcurl4-openssl-dev \
    expect \
    gawk \
    libjson-c-dev \
    uuid-dev \
    gnutls-bin \
    acl \
    libtasn1-6-dev \
    socat \
    libseccomp-dev \
    libjson-glib-dev
#
# Get a simulator
#

# libtpms
if ! pkg-config libtpms; then 
  git -C /tmp clone --depth=1 https://github.com/stefanberger/libtpms.git
  pushd /tmp/libtpms
  ./autogen.sh --prefix=/usr --with-openssl --with-tpm2
  make -j$(nproc)
  sudo make install
  popd
  rm -fr /tmp/libtpms
  sudo ldconfig
fi

# swtpm
if ! command -v swtpm; then
  git -C /tmp clone --depth=1 https://github.com/stefanberger/swtpm.git
  pushd /tmp/swtpm
  ./autogen.sh --prefix=/usr
  make -j$(nproc)
  sudo make install
  popd
  rm -fr /tmp/swtpm
fi

#
# Install tpm2-tss
#
if ! pkg-config tss2-sys; then
  # for git describe to work, one needs either a tag or a deep clone of master.
  if [ "${TPM2_TSS_VERSION}" != "master" ]; then
    extra_git_flags="--depth 1"
  fi
  git -C /tmp clone ${extra_git_flags} \
    --branch "${TPM2_TSS_VERSION}" https://github.com/tpm2-software/tpm2-tss.git
  pushd /tmp/tpm2-tss
  ./bootstrap
  ./configure --sysconfdir=/etc CFLAGS=-g
  make -j4
  sudo make install
  sudo ldconfig
  popd
fi

#
# Install Python Development Dependencies
#
python -m pip install --ignore-installed pip==21.2.4 --disable-pip-version-check --no-warn-script-location
python3 -m pip install --user -e .[dev]

exit 0
