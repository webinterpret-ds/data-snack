import codecs
import os

import setuptools

here = os.path.abspath(os.path.dirname(__file__))


def path_in_project(*path):
    return os.path.join(here, *path)


def read_file(filename):
    with codecs.open(path_in_project(filename)) as f:
        return f.read()


def read_requirements(filename):
    contents = read_file(filename).strip("\n")
    return contents.split("\n") if contents else []


EXTRAS_REQUIRE = {
    "dynamic_entity": ["data_snack_dynamic_entity"],
}


setuptools.setup(
    name="data_snack",
    test_suite="tests",
    install_requires=read_requirements("requirements.txt"),
    extras_require=EXTRAS_REQUIRE,
    entry_points={},
)
