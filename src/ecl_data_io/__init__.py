from pkg_resources import DistributionNotFound, get_distribution

__author__ = """Equinor"""
__email__ = "fg_sib-scout@equinor.com"

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __version__ = "0.0.0"
