from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='axi_plot',
    version='0.0.1',
    description='A CLI interface to work with your AxiDraw.',
    long_description=readme,
    author='Geoffrey Bradway',
    author_email='geoff.bradway@gmail.com',
    url='https://github.com/zoso95/axi_plot',
    license=license,
    packages=find_packages(exclude=('tests', 'examples')),
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        draw=axi_plot.draw:draw
        return_home=axi_plot.draw:return_home
        resume=axi_plot.draw:resume
    '''
)
