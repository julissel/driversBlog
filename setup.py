import os
from setuptools import setup, find_packages
with open(os.path.join(os.path.dirname(__file__), "README.md")) as read_me_file:
    read_me_description = read_me_file.read()

setup(
    name="driversBlog",
    version="0.1",
    license='GNU General Public License v3.0',
    author="julissel",
    author_email="julissel@yandex.ru",
    description="This is a simple blog",
    long_description=read_me_description,
    long_description_content_type="text/markdown",
    url="https://github.com/julissel/driversBlog",
    packages=find_packages(),
    include_package_data=True,
    keywords=["blog", "cars"],
    classifiers=[],
    python_requires=">=3.8",
    install_requires=["pytest", "SQLAlchemy"],
)