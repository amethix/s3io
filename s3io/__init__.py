#####################################
# Copyright 2017 Francesco Gadaleta #
#####################################
try:
    from Connector import Connector 
except ImportError:
    from s3io.Connector import Connector 

#try:
   #from . import Connector
   #import Connector 
#except ImportError:
   #from Connector import Connector 
