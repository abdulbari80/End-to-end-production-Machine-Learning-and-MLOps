import setuptools

# Read long description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

__version__ = "0.0.2"

# Project metadata
AUTHOR_NAME = "Abdul Bari"
AUTHOR_EMAIL = "bari.a.au@gmail.com"
SRC_REPO = "mlproject"
AUTHOR_USER_NAME = "abdulbari80"
REPO_NAME = "End-to-end-production-Machine-Learning-and-MLflow"

setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_NAME,  # ✅ fixed (was 'author_name')
    author_email=AUTHOR_EMAIL,  # ✅ fixed (was 'author_email')
    description="A Python package for machine learning based web app",
    long_description=long_description,
    long_description_content_type="text/markdown",  # ✅ fixed (was 'long_description_content')
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.12",
)