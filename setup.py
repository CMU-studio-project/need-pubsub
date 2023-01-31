import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="need-pubsub",
    version="0.0.1",
    author="Kyumin Park",
    author_email="kyuminpa@andrew.cmu.edu",
    description="Google Pub/Sub wrapper with encryption",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CMU-studio-project/need-pubsub",
    project_urls={
        "Bug Tracker": "https://github.com/CMU-studio-project/need-pubsub/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "need_pubsub"},
    packages=setuptools.find_packages(where="need_pubsub"),
    python_requires=">=3.6",
    install_requires=[
        "google-cloud-pubsub",
        "rsa~=4.9"
    ]
)