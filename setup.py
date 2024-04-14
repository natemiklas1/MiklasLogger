import setuptools

try:
    with open('README.md', 'r', encoding='utf-8') as fh:
        long_description = fh.read()
except TypeError:
    # if we cant use encoding becuase of < python3, lets just do this
    with open('README.md', 'r') as fh:
        long_description = fh.read()

setuptools.setup(
    name='EasyLogger',
    version='1.0.0',
    author='Nathaniel Miklas',
    author_email='natemiklas1@gmail.com',
    description='Custom logging class because I got tired of rewriting one for each project',
    long_description='',
    long_description_content_type='text/markdown',
    url='https://github.com/natemiklas1/MiklasLogger.git',
    project_urls={
        # "Bug Tracker": "https://github.com/mike-huls/toolbox/issues"
    },
    license='LICENSE',
    packages=['EasyLogger'],
    install_requires=['logging >= 0.4.9.6'],
)
