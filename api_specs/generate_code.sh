#!/bin/bash
# Generate code for proto files
python3 -m grpc_tools.protoc -I protobufs --python_out=api_specs/python_lib/ --pyi_out=api_specs/python_lib/ --grpc_python_out=api_specs/python_lib/ protobufs/*.proto
/bin/bash fix_imports.sh