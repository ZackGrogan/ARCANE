from setuptools import setup, find_packages

setup(
    name="arcane-backend",
    version="0.7.0-beta",
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask-pymongo',
        'python-dotenv',
        'requests',
    ],
)
