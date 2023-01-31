import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="need-pubsub",
    version="0.0.2",
    author="Kyumin Park",
    author_email="kyuminpa@andrew.cmu.edu",
    description="Google Pub/Sub wrapper with encryption",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CMU-studio-project/need-pubsub",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "google-cloud-pubsub"
    ],
    # py_modules=["need_pubsub/publish", "need_pubsub/subscribe"]
)