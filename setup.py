from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='s3io',
      version='0.1a',
      description='Amazon S3 bucket utilities',
      long_description=readme(),
      classifiers=[
        'Development Status :: 1 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Semantics :: Linguistic :: Graph Database',
      ],
      url='http://datascienceathome.com',
      author='Francesco <frag> Gadaleta',
      author_email='francesco@amethix.com',
      license='MIT',
      test_suite='nose.collector',
      tests_require=['nose'],
      packages=['s3io'],
      install_requires=[
		'boto', 
		'FileChunkIO',
      ],
      zip_safe=False)
