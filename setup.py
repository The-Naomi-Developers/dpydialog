from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="dpydialog",
    version="1.0.0",
    author="The-Naomi-Developers",
    author_email="starrysparklez@naomi.win", 
    description="A simple, typed library for creating components and interactive dialogs based on discord.py.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/The-Naomi-Developers/dpydialog",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
    
    packages=find_packages(
        include=["dpydialog", "dpydialog.*"]
    ), 
    install_requires=requirements,
    python_requires=">=3.7",

    include_package_data=False,

    keywords="discord, dialogue, discord.py, ui, gui",
    license="MIT",
    zip_safe=False,
)