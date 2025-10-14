import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

__version__ = "0.0.1"

AUTHOR_NAME = "Abdul Bari"
AUTHOR_EMAIL = "bari.a.au@gmail.com"
SRC_REPO = "mlproject"
AUTHOR_USER_NAME = "abdulbari80"
REPO_NAME = "Production-Machine-Learning-with-MLflow"

setuptools.setup(
    name = SRC_REPO,
    version=__version__,
    author_name = AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    author_user_name = AUTHOR_USER_NAME,
    description="A python package for machine learning web app",
    long_description=long_description,
    long_description_content="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src")
)