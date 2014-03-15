from setuptools import find_packages, setup

setup(
    name='IdobataPlugin', version='0.2',
    packages=find_packages(exclude=['*.tests*']),
    author='Hiroki Kondo',
    author_email='kompiro@gmail.com',
    url='https://github.com/kompiro/trac-idobata-plugin',
    description='Trac - Idobata integration',
    platforms='all',
    license='Apache License v2',
    entry_points = {
        'trac.plugins': [
            'idobata = idobata.notification',
        ],
    },
)
