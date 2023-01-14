import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='BBData',
    version='0.0.1',
    author='Max Fieschko',
    author_email='fieschkom@msoe.edu',
    description='Datatypes used to communicate data between BlackBoxr and extensions.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/fieschkon/BlackBoxr-Datatypes',
    project_urls = {
        "Bug Tracker": "https://github.com/fieschkon/BlackBoxr-Datatypes/issues"
    },
    license='MIT',
    packages=['BBData'],
    install_requires=['requests'],
)