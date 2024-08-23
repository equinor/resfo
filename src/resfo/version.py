from importlib.metadata import PackageNotFoundError, version

try:
    version = version("resfo")
except PackageNotFoundError:
    version = "0.0.0"
