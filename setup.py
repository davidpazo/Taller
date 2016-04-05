#importamos herramienta para generar ejecutables del programa


import sys
import os
from distutils.core import setup
from cx_Freeze import setup, Executable
"""
Este metodo se ha creado para realizar la generacion del exe para windows
o tar.gz para ubuntu, utilizando el repositorio indicado que bien puede ser
distutils, setuptools, y py2exe(aunque este ultimo no es compatible con python 3.5)
"""
setup(name="Taller clientes",
      version="1.0",
      description="Aplicacion para la gestion de un taller",
      author="David Pazo",
      author_email="dpazolopez@danielcastelo.org",
      url="http://mundopython.org/proyecto-python/",
      license="GPL",
      scripts=["Login.py","Taller.py","Generarpdf.py"],
      console=["Login.py"],
      options={"py2exe": {"bundle_files": 1}},
      zipfile=None
)