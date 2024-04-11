import setuptools

# try:
#     with open('README.md', 'r', encoding='utf-8') as fh:
#         long_description = fh.read()
# except TypeError:
#     # if we cant use encoding becuase of < python3, lets just do this
#     with open('README.md', 'r') as fh:
#         long_description = fh.read()

setuptools.setup(
    name='MiklasLogger',
    version='0.0.1',
    author='Nathaniel Miklas',
    author_email='natemiklas1@gmail.com',
    description='Loggin',
    long_description='',
    long_description_content_type='text/markdown',
    url='https://github.com/natemiklas1/MiklasLogger.git',
    project_urls={
        # "Bug Tracker": "https://github.com/mike-huls/toolbox/issues"
    },
    license='LICENSE',
    packages=['MiklasLogger'],
    install_requires=[],
)
