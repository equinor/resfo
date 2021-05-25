from pathlib import Path

from setuptools import find_packages, setup


def get_long_description() -> str:
    return Path("README").read_text(encoding="utf8")


setup(
    name="ecl-data-io",
    author="Equinor",
    author_email="fg_sib-scout@equinor.com",
    description="parsing library for ecl  data files.",
    use_scm_version=True,
    url="https://github.com/equinor/ecl_data_io",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "ecl_data_io=ecl_data_io.__main__:main",
        ],
    },
    platforms="any",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    setup_requires=["setuptools_scm"],
    include_package_data=True,
)
