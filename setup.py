"""
Setup file for Yelp Analytics pipeline.
"""
from setuptools import setup, find_packages

setup(
    name='yelp-analytics',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pyspark',
        'google-cloud-bigquery>=3.11.0',
        'google-cloud-storage>=2.10.0',
        'pytest',
        'pytest-spark',
    ],
    python_requires='>=3.8',
) 