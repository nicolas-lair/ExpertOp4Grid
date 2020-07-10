import setuptools
from setuptools import setup

pkgs = {
    "required": [
        "atomicwrites>=1.4.0"
        "attrs>=19.3.0"
        "backcall>=0.1.0"
        "certifi>=2020.4.5.1"
        "chardet>=3.0.4"
        "cloudpickle>=1.2.2"
        "colorama>=0.4.3"
        "commonmark>=0.5.4"
        "cycler>=0.10.0"
        "decorator>=4.4.2"
        "docutils>=0.16"
        "graphviz>=0.14"
        "Grid2Op>=1.0.1"
        "gym>=0.12.6"
        "idna>=2.9"
        "importlib-metadata>=1.6.0"
        "ipykernel>=5.3.0"
        "ipython>=7.15.0"
        "ipython-genutils>=0.2.0"
        "jedi>=0.17.0"
        "jupyter-client>=6.1.3"
        "jupyter-core>=4.6.3"
        "kiwisolver>=1.2.0"
        "llvmlite>=0.32.1"
        "matplotlib>=2.2.5"
        "metakernel>=0.24.4"
        "more-itertools>=8.2.0"
        "networkx>=2.4"
        "numba>=0.49.1"
        "numpy>=1.18.4"
        "oct2py>=5.0.4"
        "octave-kernel>=0.32.0"
        "packaging>=20.4"
        "pandapower>=2.2.2"
        "pandas>=1.0.4"
        "parso>=0.7.0"
        "pathlib>=1.0.1"
        "pexpect>=4.8.0"
        "pickleshare>=0.7.5"
        "pluggy>=0.13.1"
        "prompt-toolkit>=3.0.5"
        "ptyprocess>=0.6.0"
        "py>=1.8.1"
        "pydot>=1.4.1"
        "pygame>=1.9.6"
        "pyglet>=2.0.dev0"
        "Pygments>=2.6.1"
        "pyparsing>=2.4.7"
        "pytest>=4.4.2"
        "python-dateutil>=2.8.1"
        "pytz>=2020.1"
        "pywin32>=227"
        "pyyaml>=5.3.1"
        "pyzmq>=19.0.1"
        "recommonmark>=0.4.0"
        "requests>=2.23.0"
        "scipy>=1.4.1"
        "six>=1.15.0"
        "tornado>=6.0.4"
        "tqdm>=4.46.0"
        "traitlets>=4.3.3"
        "urllib3>=1.25.9"
        "wcwidth>=0.2.2"
        "zipp>=3.1.0"
    ],
    "extras": {
        "optional": [
            "pypower>=5.1.4"
            "pypownet>=2.2.0"
        ]
    }
}

setup(name='ExpertOp4Grid',
      version='0.0.1',
      description='Expert analysis algorithm for solving overloads in a powergrid',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
          "Intended Audience :: Developers",
          "Intended Audience :: Education",
          "Intended Audience :: Science/Research",
          "Natural Language :: English"
      ],
      keywords='ML powergrid optmization RL power-systems',
      author='Mario Jothy',
      author_email=' mario.jothy@artelys.com',
      url="https://github.com/mjothy/ExpertOp4Grid",
      license='Mozilla Public License 2.0 (MPL 2.0)',
      packages=setuptools.find_packages(),
      extras_require=pkgs["extras"],
      include_package_data=True,
      install_requires=pkgs["required"],
      zip_safe=False
)