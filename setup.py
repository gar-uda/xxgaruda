from setuptools import setup

setup(
    name="xxgaruda",
    version="2.0",
    description="XXGARUDA — The Ultimate Tool. Better than Nmap, Hydra, SQLMap, John, Metasploit, Burp, Wireshark, Aircrack, SET — ALL COMBINED.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="gar-uda",
    author_email="your-email@example.com",
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
