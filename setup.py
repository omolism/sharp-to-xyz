from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sharp-to-xyz",
    version="1.0.0",
    author="DanciShen",
    author_email="dancishen@gmail.com",
    description="Convert Apple SHARP 3DGS PLY files to XYZ point cloud format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/omolism/sharp-to-xyz",
    py_modules=["sharp_to_xyz"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "sharp-to-xyz=sharp_to_xyz:main",
        ],
    },
    keywords="3dgs gaussian-splatting point-cloud ply xyz sharp apple",
    project_urls={
        "Bug Reports": "https://github.com/omolism/sharp-to-xyz/issues",
        "Source": "https://github.com/omolism/sharp-to-xyz",
    },
)
