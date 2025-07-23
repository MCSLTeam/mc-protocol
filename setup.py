from setuptools import setup, find_packages
setup(
    name="mc_protocol",
    version="1.0.01-SNAPSHOT",
    author="c2yz",
    author_email="c2yzawa@outlook.com",
    description="A Minecraft protocol library for Python",
    long_description="""
    Lightweight, easy, and quick Minecraft protocol library for Python
    """,
    packages=find_packages(),
    install_requires=[],
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)