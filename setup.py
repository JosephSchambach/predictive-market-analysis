from setuptools import setup, find_packages

setup(
    name="predictive_ma",
    version="0.0.6",
    packages=find_packages(where='predictive_ma',exclude=['analysis_main_flow', 'analysis_main_flow.*']),
    package_dir={'': 'predictive_ma'},
)
