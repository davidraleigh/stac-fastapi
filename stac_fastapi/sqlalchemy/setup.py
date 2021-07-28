"""stac_fastapi: sqlalchemy module."""

from setuptools import setup

with open("README.md") as f:
    desc = f.read()
install_requires = [
    "fastapi",
    "attrs",
    "pydantic[dotenv]",
    "stac_pydantic==2.0.*",
    "sqlakeyset",
    "geoalchemy2<0.8.0",
    "sqlalchemy==1.3.23",
    "shapely",
    "psycopg2-binary",
    "alembic",
    "fastapi-utils",
    "uvicorn",
    "brotli-asgi",
    "orjson",
    "stac-fastapi.types",
    "stac-fastapi.api",
    "stac-fastapi.extensions",
]

extra_reqs = {
    "dev": [
        "pytest",
        "pytest-cov",
        "pytest-asyncio",
        "pre-commit",
        "requests",
    ],
    "docs": ["mkdocs", "mkdocs-material", "pdocs"],
    "server": ["uvicorn[standard]>=0.12.0,<0.14.0"],
}


setup(
    name="stac-fastapi.sqlalchemy",
    description="An implementation of STAC API based on the FastAPI framework.",
    long_description=desc,
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="STAC FastAPI COG",
    author=u"Arturo Engineering",
    author_email="engineering@arturo.ai",
    url="https://github.com/stac-utils/stac-fastapi",
    license="MIT",
    packages=['stac_fastapi.sqlalchemy',
              'stac_fastapi.sqlalchemy.models',
              'stac_fastapi.sqlalchemy.types'],
    zip_safe=False,
    install_requires=install_requires,
    tests_require=extra_reqs["dev"],
    extras_require=extra_reqs,
    entry_points={
        "console_scripts": ["stac-fastapi-sqlalchemy=stac_fastapi.sqlalchemy.app:run"]
    },
)
