from setuptools import find_packages, setup


setup(
    name='ybs_task',
    version='0.1.0',
    author='Mikheychev Igor',
    author_email='igor_m_87@mail.ru',
    description='Yandex Backend School task',
    packages=find_packages(),
    install_requires=['django==4.0.5']
)
