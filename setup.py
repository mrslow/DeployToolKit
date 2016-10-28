from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='deploytoolkit',
    version='0.1',
    description='Tool for easy deploying.',
    long_description=readme,
    author='Anton Shchetikhin',
    author_email='animal2k@gmail.com',
    packages = ['deploytoolkit'],
    url='https://github.com/mrslow/DeployToolKit',
    license=license
)

