from setuptools import setup, find_packages

setup(
    name = 'mothball',
    version = '0.1',
    packages = find_packages(where='src'),
    package_dir = {"": "src"},
    include_package_data = True,
    data_files=['static/mothball.config', 'scripts/mothball.py'],
    install_requires = [ 'sqlalchemy',
                         'boto3',
                         'pyyaml',
                         'PyMySQL',
                         'pymysql-sa'
                         ]
)