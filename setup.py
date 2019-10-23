from distutils.core import setup
setup(
  name="PythonDNS",
  packages=["PythonDNS"],
  version="0.1",
  license="MIT",
  description="Python-based DNS Interception and Proxy",
  author="Daniel Robertson",
  author_email="",
  url="https://github.com/endail/PythonDNS",
  download_url="",
  keywords=["python", "dns"],
  install_requires=[
          "dnslib"
      ],
  classifiers=[
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Build Tools",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3"
  ],
)