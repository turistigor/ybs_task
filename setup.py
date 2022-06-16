from setuptools import find_packages, setup
from pkg_resources import parse_requirements


def load_requirements(fname: str) -> list:
    requirements = []
    with open(fname, 'r') as fp:
        for req in parse_requirements(fp.read()):
            extras = '[{}]'.format(','.join(req.extras)) if req.extras else ''
            requirements.append(
                '{}{}{}'.format(req.name, extras, req.specifier)
            )
    return requirements


setup(
    name='ybs_task',
    version='0.1.0',
    author='Mikheychev Igor',
    author_email='igor_m_87@mail.ru',
    description='Yandex Backend School task',
    packages=find_packages(),
    install_requires=load_requirements('requirements.txt'),
    scripts=['manage.py']
)
