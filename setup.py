from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='matrix_traversal',
    version='0.0.1',
    author='Cotang01',
    author_email='example@gmail.com',
    description='Package for traversing matrix from provided urls.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/Cotang01/python-trainee-assignment',
    packages=find_packages(where='.', exclude='tests'),
    install_requires=['aiohttp>=3.9.5'],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    project_urls={
        'GitHub': 'https://github.com/Cotang01/python-trainee-assignment'
    },
    python_requires='>=3.11'
)
