import setuptools

setuptools.setup(
    name="pyxtm",
    version="0.9.3",
    author="tkato",
    author_email="takatsugu-kato@outlook.jp",
    description="pyxtm module handles xtm.",
    long_description="pyxtm module handles xtm.",
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.10.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests'
    ]
)
