import setuptools

setuptools.setup(
    name="wiring896",
    version="0.1.0",
    author_email="kuangwj@sjtu.edu.cn",
    python_requires=">=3.6",
    install_requires=[
        "matplotlib",
        "numpy",
        "pandas",
        "xlrd",
        "openpyxl",
        "gdspy",
    ],
    packages=setuptools.find_packages(),
)
