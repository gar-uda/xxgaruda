from setuptools import setup

setup(
    name="xxgaruda",
    version="3.0",
    description="XXGARUDA — The Annihilator. The Deadliest Attacker on Earth. 50+ attack modules, auto-exploit, auto-crack, auto-pwn, global proxy rotation.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="gar-uda",
    author_email="endeavoradekanlevictor@gmail.com",
    py_modules=["xxgaruda"],
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "xxgaruda=xxgaruda:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
