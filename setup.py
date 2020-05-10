import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='PySynt',
     version='0.1',
     author="Some people",
     description="A python syntax tester who's gonna work, I think (not sure of that)",
     author_email='plop@plop.fr',
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="too add",
     packages=['src.main', 'src.parser', 'src.tokenizer'],
     classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
     python_requires='>=3.6',
     entry_points={
        "console_scripts": [
            "pySynt = src.main.main:pySynt",
        ],
    }
 )
