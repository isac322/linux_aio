#!/bin/bash
set -e -x

# Compile wheels
for PYBIN in /opt/python/cp37-cp37m/bin /opt/python/cp36-cp36m/bin; do
    "${PYBIN}/pip" install -r /io/requirements.txt
    "${PYBIN}/pip" wheel /io/ -w wheelhouse/ --no-deps
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
    auditwheel repair "$whl" -w /io/wheelhouse/
done

# Install packages and test
for PYBIN in /opt/python/cp37-cp37m/bin /opt/python/cp36-cp36m/bin; do
    "${PYBIN}/pip" install linux_aio --no-index -f /io/wheelhouse
done
