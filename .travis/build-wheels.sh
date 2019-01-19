#!/bin/bash
set -e -x

py_vers=(37)

# Compile wheels
for ver in "${py_vers[@]}"; do
	PYBIN="/opt/python/cp${ver}-cp${ver}m/bin"
    "${PYBIN}/pip" install -r /io/requirements.txt
    "${PYBIN}/pip" wheel /io/ -w wheelhouse/ --no-deps
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
    auditwheel repair "$whl" -w /io/wheelhouse/
done

# Install packages and test
for ver in "${py_vers[@]}"; do
	PYBIN="/opt/python/cp${ver}-cp${ver}m/bin"
    "${PYBIN}/pip" install linux_aio --no-index -f /io/wheelhouse
done
