from importlib.metadata import version, PackageNotFoundError

try:
    version = version("resfo")
except PackageNotFoundError:
    version = "0.0.0"
