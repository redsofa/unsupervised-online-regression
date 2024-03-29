from setuptools import setup
import versioneer

requirements = [
    "pandas>=1.5.3",
    "scikit-learn>=1.0.2",
    "numpy>=1.24.1",
    "river>=0.13.0"
]

setup(
    name='fluire',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Incremental Learning Library",
    license="Apache",
    author="Rene Richard",
    author_email='rene.richard@nrc-cnrc.gc.ca',
    url='https://github.com/redsofa/fluire',
    packages=['fluire', 'fluire.util', 'fluire.factories', 'fluire.metrics', 'fluire.models',
             'fluire.settings'],
    entry_points={
        'console_scripts': [
            'fluire=fluire.cli:cli'
        ]
    },
    install_requires=requirements,
    keywords='fluire',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
