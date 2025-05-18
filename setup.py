from setuptools import setup, find_packages

setup(
    name="optimisation_pvc",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'streamlit>=1.28',
        'pandas>=2.0',
        'numpy>=1.24',
        'folium>=0.14'
    ],
)