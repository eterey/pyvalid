from pyvalid import version
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def main():
    # Describe installer
    setup(
        name='pyvalid',
        version=version,
        author='Maxim Grischuk',
        author_email='uzumaxy@gmail.com',
        maintainer='Maxim Grischuk',
        maintainer_email='uzumaxy@gmail.com',
        packages=['pyvalid'],
        url='http://uzumaxy.github.io/pyvalid/',
        download_url='https://github.com/uzumaxy/pyvalid/releases',
        bugtrack_url='https://github.com/uzumaxy/pyvalid/issues',
        license='BSD',
        description='pyvalid is a Python validation tool for checking of input function parameters and return values.',
        long_description=open('README.rst').read(),
        install_requires=[],
        keywords=[
            'pyvalid', 'valid',
            'validation', 'type',
            'checking', 'check',
            'decorator'
        ],
        platforms='Platform Independent',
        package_data={
            'pyspectator': ['LICENSE', 'README.rst']
        },
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Intended Audience :: Information Technology',
            'License :: OSI Approved :: BSD License',
            'Natural Language :: English',
            'Operating System :: MacOS',
            'Operating System :: Microsoft :: Windows :: Windows 7',
            'Operating System :: Microsoft :: Windows :: Windows NT/2000',
            'Operating System :: Microsoft :: Windows :: Windows Server 2003',
            'Operating System :: Microsoft :: Windows :: Windows Server 2008',
            'Operating System :: Microsoft :: Windows :: Windows Vista',
            'Operating System :: Microsoft :: Windows :: Windows XP',
            'Operating System :: Microsoft',
            'Operating System :: OS Independent',
            'Operating System :: POSIX :: BSD :: FreeBSD',
            'Operating System :: POSIX :: Linux',
            'Operating System :: POSIX :: SunOS/Solaris',
            'Operating System :: POSIX',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.0',
            'Programming Language :: Python :: 3.1',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: Implementation',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python',
            'Topic :: Software Development :: Debuggers',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Testing'
        ],
    )


if __name__ == '__main__':
    main()
