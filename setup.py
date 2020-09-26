import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="structured_log",
    version="0.1.1",
    author="Gregory Zhizhilkin",
    author_email="gregory@stopdesign.ru",
    description="Google Cloud structured log formater for Django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stopdesign/django-structured-log",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
