# setup.py
"""
Script de instalação
"""
from setuptools import setup, find_packages

setup(
    name="rook",
    version="3.0.0",
    description="Ferramenta simples e eficiente para otimização do Windows",
    author="rook",
    packages=find_packages(),
    install_requires=[
        "PySide6>=6.5.0",
        "psutil>=5.9.0",
    ],
    entry_points={
        "console_scripts": [
            "rook=main:main",
        ],
    },
)