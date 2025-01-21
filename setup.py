from setuptools import setup, find_packages

setup(
    name="link_counter",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "selenium>=4.15.0"
    ],
)