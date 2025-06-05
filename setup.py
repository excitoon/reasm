import os

import setuptools


if 1: # with open(f'{os.path.dirname(os.path.abspath(__file__))}/requirements.txt') as requirements:
    with open(f'{os.path.dirname(os.path.abspath(__file__))}/README.md') as readme:
        setuptools.setup(
            name='reasm',
            version='0.1.0',
            description='Binary tools for various formats (e.g. MZ)',
            long_description=readme.read(),
            long_description_content_type='text/markdown',
            author='Vladimir Chebotarev',
            author_email='vladimir.chebotarev@gmail.com',
            license='MIT',
            classifiers=[
                'Development Status :: 5 - Production/Stable',
                'Environment :: Console',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: MIT License',
                'Operating System :: OS Independent',
                'Programming Language :: Python :: 3 :: Only',
                'Topic :: Software Development',
                'Topic :: Utilities',
            ],
            keywords=['mz', 'executable', 'dos', 'reverse-engineering'],
            project_urls={
                'Documentation': 'https://github.com/excitoon/reasm/blob/master/README.md',
                'Source': 'https://github.com/excitoon/reasm',
                'Tracker': 'https://github.com/excitoon/reasm/issues',
            },
            url='https://github.com/excitoon/reasm',
            packages=['reasm'],
            package_dir={'reasm': ''},
            scripts=['mzinfo', 'mzinfo.cmd', 'mzfix', 'mzfix.cmd'],
            install_requires=[], # requirements.read().splitlines(),
        )
