from setuptools import setup
import sys


setup(
    name='witchytwigs',
    version='0.0.1',
    maintainer='Steve Cook',
    maintainer_email='witchytwigs@snarkout.org',
    license='MIT',
    #url='',
    platforms=['any'],
    description='A bespoke static-site generator',
    packages=['witchytwigs'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Development Status :: 3 - Alpha'
    ],
    entry_points={
        'console_scripts': [
            'witchytwigs = witchytwigs.cli:main'
        ]
    }
)
