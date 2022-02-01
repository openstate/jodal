from datetime import datetime
from setuptools import setup, find_packages

setup(
    name="jodal-sources",
    version=datetime.utcnow().date().isoformat(),
    classifiers=[],
    keywords="",
    packages=find_packages("src"),
    package_dir={"": "src"},
    namespace_packages=[],
    include_package_data=True,
    zip_safe=False,
    install_requires=["memorious", "datafreeze", "newspaper3k"],
    entry_points={"memorious.plugins": ["example = example:init"]},
)
