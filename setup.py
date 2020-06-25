from setuptools import setup
from .rf_calculator import __version__ as version


setup(
    name='robotframework-calculator',
    version=version,
    packages=['rf_calculator', 'rf_calculator.libs'],
    url='https://github.com/doguz2509/robotframework-calculator',
    license='MIT',
    author='Dmitry Oguz',
    author_email='doguz2509@gmail.com',
    description=''
)
