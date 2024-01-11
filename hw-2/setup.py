from setuptools import setup, find_namespace_packages

setup(
    name="user_assistant",
    version="1",
    description="User assistant",
    url="https://github.com/rusetskiy1974/-CorePython-command-project",
    author="PYTHON DEVELOPERS",
    author_email="flyingcircus@example.com",
    license="MIT",
    packages=find_namespace_packages(),
    include_package_data=True,
    install_requires=["rich"],
    entry_points={"console_scripts": ["user_assistant = user_assistant.main:main"]},
)
