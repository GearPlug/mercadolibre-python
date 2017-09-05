from setuptools import setup

setup(name='mercadolibre',
      version='0.1',
      description='API wrapper for MercadoLibre written in Python',
      url='https://github.com/GearPlug/mercadolibre-python',
      author='Miguel Ferrer',
      author_email='ingferrermiguel@gmail.com',
      license='GPL',
      packages=['mercadolibre'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
