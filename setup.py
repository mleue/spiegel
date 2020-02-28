from setuptools import setup, find_packages

setup(
    name="spiegel",
    version="0.1.2",
    description="A server/client architecture for remote python objects.",
    license="MIT",
    packages=find_packages(exclude=["tests"]),
    install_requires=["fastAPI", "requests", "uvicorn"],
    extras_require={"dev": ["pytest"]},
)
