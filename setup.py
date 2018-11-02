import setuptools

with open('requirements.txt') as f:
    required = f.read().splitlines()


setuptools.setup(
    name="grdateparser",
    version="0.0.1",
    author="Gokulraj Ramdass",
    author_email="gokulraj.ramdass@sap.com",
    description="GRNLP for Text Classification",
    long_description="GRNLP for DATE PARSER",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)