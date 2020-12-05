from setuptools import setup
from os import path
import re

package_name = "pyjpboatrace"
root_dir = path.abspath(path.dirname(__file__))

with open(path.join(package_name, '__init__.py')) as f:
    init_text = f.read()

    version = re.search(
        r'__version__\s*=\s*[\'\"](.+?)[\'\"]',
        init_text
    ).group(1)

    license = re.search(
        r'__license__\s*=\s*[\'\"](.+?)[\'\"]',
        init_text
    ).group(1)

    author = re.search(
        r'__author__\s*=\s*[\'\"](.+?)[\'\"]',
        init_text
    ).group(1)

    author_email = re.search(
        r'__author_email__\s*=\s*[\'\"](.+?)[\'\"]',
        init_text
    ).group(1)

    url = re.search(
        r'__url__\s*=\s*[\'\"](.+?)[\'\"]',
        init_text
    ).group(1)

assert version
assert license
assert author
assert author_email
assert url

with open(path.join(root_dir, 'requirements.txt')) as f:
    install_requires = [name.rstrip() for name in f.readlines()]

with open(path.join(root_dir, 'test-requirements.txt')) as f:
    tests_require = [name.rstrip() for name in f.readlines()]

with open('README.md', 'r', encoding='utf-8') as f:
    README = f.read()

setup(
    name=package_name,
    packages=[
        package_name+p
        for p in ['', '.parsers', '.requestors', '.utils']
    ],

    version=version,
    license=license,
    author=author,
    author_email=author_email,
    url=url,

    install_requires=install_requires,
    tests_require=tests_require,

    description='PyJPBoatrace: Python-based Japanese boatrace tools',
    long_description=README,
    long_description_content_type='text/markdown',
    keywords=u'競艇, boatrace, data analysis',

    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
