# coding: utf-8

from setuptools import setup, find_packages


if __name__ == '__main__':
    NAME = "swagger_server"
    VERSION = "1.0.0"

    # To install the library, run the following
    #
    # python setup.py install
    #
    # prerequisite: setuptools
    # http://pypi.python.org/pypi/setuptools
    
    REQUIRES = ["connexion"]
    setup(
        name=NAME,
        version=VERSION,
        description="ResMon - distributed resources monitoring",
        author_email="mad.fis.agh@gmail.com",
        url="",
        keywords=["Swagger", "ResMon - distributed resources monitoring"],
        install_requires=REQUIRES,
        packages=find_packages(),
        package_data={"": ["swagger/swagger.yaml"]},
        include_package_data=True,
        entry_points={
            "console_scripts": ["swagger_server=swagger_server.__main__:main"]
            },
        long_description="""\
        This is simple resource monitor which allows to view how much are
        used all resources on all monitored hosts. Note that we use token
        authorization with JWT so you need to provide &#x60;Authorization&#x60;
        header with &#x60;Bearer [TOKEN]&#x60; value on each request. You will
        receive token from auth server on successful sign-in or sign-on action.
        Make sure monitor uses selected auth server. Monitor should handle CORS
        with pre-flight, allowing query each path by OPTIONS to get CORS headers.
        """,
    )
