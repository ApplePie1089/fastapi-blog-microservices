#!/bin/bash
sed -i -E "s/^import (.+)_pb2/from api_specs.python_lib import \1_pb2/" api_specs/python_lib/*.py