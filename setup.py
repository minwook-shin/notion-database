import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="notion-database",
    version="2.0.dev0",
    author="minwook-shin",
    author_email="minwook0106@gmail.com",
    description=" Python bindings for Notion Database API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/minwook-shin/notion-database",
    project_urls={
        "Bug Tracker": "https://github.com/minwook-shin/notion-database/issues",
    },
    install_requires=[
        "requests==2.32.3",
        "urllib3<2.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Development Status :: 5 - Production/Stable'
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.9",
)
