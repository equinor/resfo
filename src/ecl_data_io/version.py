from importlib.metadata import version, PackageNotFoundError

try:
    version = version("ecl-data-io")
except PackageNotFoundError:
    version = "0.0.0"
