from setuptools import setup, find_packages

setup(
    name = 'mothball',
    version = '0.1',
    packages = find_packages(),
    include_package_data = True,
    data_files=['static/mothball.config', 'mothball.py'],
    install_requires = [ 'sqlalchemy',
                         'boto3',
                         'pyyaml'
                         ]
)