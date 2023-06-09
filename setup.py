from setuptools import setup, find_packages

# README.mdまたはREADME.rstファイルの内容を読み込む
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pytale',
    version='0.1.3',
    packages=find_packages(),

    long_description=long_description,
    long_description_content_type="text/markdown",
)