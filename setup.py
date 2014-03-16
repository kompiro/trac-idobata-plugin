from setuptools import find_packages, setup

setup(
    name='IdobataPlugin', version='0.4',
    packages=find_packages(exclude=['*.tests*']),
    author='Hiroki Kondo',
    author_email='kompiro@gmail.com',
    url='https://github.com/kompiro/trac-idobata-plugin',
    description='Trac - Idobata integration',
    platforms='all',
    license='Apache License v2',
    install_requires = ['Trac >= 1.0'],
    entry_points = {
        'trac.plugins': [
            'idobata = idobata.notification',
        ],
    },
)
