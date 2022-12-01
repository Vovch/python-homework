from setuptools import setup

setup(
    name='tagcounter',
    version='1.1',
    author='Vladimir_Mironov2',
    packages=['tagcounter'],
    description='Description',
    package_data={'': ['*.txt']},
    install_requires=['requests'],
    entry_points={'console_scripts': ['tagcounter = tagcounter.tagcounter:main']},
)
