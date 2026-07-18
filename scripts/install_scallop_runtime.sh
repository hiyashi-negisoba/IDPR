#!/usr/bin/env bash
set -euo pipefail

VERSION="0.2.4"
ASSET="scli-${VERSION}-linux-x86_64"
URL="https://github.com/scallop-lang/scallop/releases/download/${VERSION}/${ASSET}"
SHA256="8c5ec86fcdb0dbd55698eff7570ac7396d0b0878e601207f868d61f9d6482b9a"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_DIR="${PROJECT_ROOT}/tools/scallop"
TARGET="${TARGET_DIR}/${ASSET}"

mkdir -p "${TARGET_DIR}"
curl --fail --location --retry 3 --output "${TARGET}.download" "${URL}"
printf '%s  %s\n' "${SHA256}" "${TARGET}.download" | sha256sum --check --status
mv "${TARGET}.download" "${TARGET}"
chmod 0755 "${TARGET}"
"${TARGET}" --version
