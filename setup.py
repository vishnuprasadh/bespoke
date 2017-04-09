from setuptools import setup

setup(author="Vishnu Prasad Hari",
    author_email="vishnuprasadh@gmail.com",
    version="0.1",
    description="This will be used to process products, orders and customer information and provide recommendations for the same",
    download_url="",
    py_modules=["productprocessor","productlabelencoder","avroutility","configuration"],
    license="MIT, provide credit for the author when using it for commercial purposes",
    keywords="recommendations, recommendationengine, recommendation engine, bespoke, python recommendations, suggestions, vishnu,hari",
    name="bespoke",
    install_requires=['numpy','scipy','avro','pandas','kafka','logging','sklearn','cassandra-driver']
)
