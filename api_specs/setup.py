from setuptools import setup, find_packages

setup(
    name='api-specs',
    version='0.1.0',
    packages=find_packages(),
    package_data={package: ["*.pyi", "**/*.pyi"] for package in find_packages()},
    install_requires=[
        'grpcio>=1.50.0',
        'grpcio-tools>=1.50.0',
        'protobuf>=4.21.0',
    ],
    author="FastAPI Blog Backend",
    description="gRPC API specifications for blog microservices"
)