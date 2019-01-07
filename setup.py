"""Setup configuration."""
import setuptools
from reporeleaser.version import __version__

with open("README.md", "r") as fh:
    LONG = fh.read()
setuptools.setup(
    name="reporeleaser",
    version=__version__,
    author="Joakim Sorensen",
    author_email="ludeeus@gmail.com",
    description="",
    long_description=LONG,
    install_requires=['click', 'PyGithub>=1.43.4'],
    long_description_content_type="text/markdown",
    url="https://github.com/ludeeus/reporeleaser",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    entry_points={
        'console_scripts': [
            'reporeleaser = reporeleaser.cli:cli'
        ]
    }
)
