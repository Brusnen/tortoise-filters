from setuptools import setup, find_packages

setup(
    name='tortoise-filters',
    version='0.3',
    packages=find_packages(),
    install_requires=['tortoise-orm==0.21.5', 'fastapi==0.112.0'],
    description='A filtering library with automatical documentation for tortoise orm',
    url='https://github.com/Brusnen/tortoise-filters',
    author='Sergey Brusnov',
    author_email='sergey.brusnov1900@gmail.com',
    license='MIT',
)