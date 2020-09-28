from pyvalid import version
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def main():
    # Describe installer
    with open('README.rst') as fd:
        long_description = fd.read()
    with open('requirements.txt') as fd:
        requirements = fd.read().splitlines()
    setup(
        name='pyvalid',
        version=version,
        author='Max Hryshchuk',
        author_email='uzumaxy@gmail.com',
        maintainer='Max Hryshchuk',
        maintainer_email='uzumaxy@gmail.com',
        packages=['pyvalid'],
        url='http://uzumaxy.github.io/pyvalid/',
        download_url='https://github.com/uzumaxy/pyvalid/releases',
        license='MIT',
        description='The module, which allows easily validate function\'s '
            + 'input/output values.',
        long_description=long_description,
        install_requires=requirements,
        keywords=[
            'pyvalid', 'valid',
            'validation', 'type',
            'checking', 'check',
            'decorator', 'runtime',
            'debug', 'test'
        ],
        platforms='Platform Independent',
        package_data={
            'pyvalid': ['LICENSE', 'README.rst']
        },
        test_suite='tests',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: Information Technology',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Operating System :: MacOS',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX :: Linux',
            'Operating System :: POSIX',
            'Operating System :: Unix',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.0',
            'Programming Language :: Python :: 3.1',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: Implementation',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python',
            'Topic :: Software Development :: Debuggers',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Testing',
            'Topic :: Utilities'
        ],
    )


if __name__ == '__main__':
    main()
