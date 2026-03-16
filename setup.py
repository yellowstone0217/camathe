from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="camathe",
    version="0.0.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="一个对卡牌游戏非常良心的计算库 - 快速计算卡牌游戏中的各种数字",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/camathe",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment :: Board Games",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.19.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.9",
        ],
    },
)