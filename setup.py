from setuptools import setup
from .robot_math import __version__ as version


setup(
    name='robotframework-calculator',
    version=version,
    packages=['robot_math', 'robot_math.types'],
    install_requires=[
        'robotframework>3.2.1'
    ],
    url='https://github.com/doguz2509/robotframework-calculator',
    license='MIT',
    author='Dmitry Oguz',
    author_email='doguz2509@gmail.com',
    description=''
)
