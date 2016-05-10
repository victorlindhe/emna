
batch.py
--------
```
python batch.py /path/to/directory /path/to/library.lib
```
Runs `emna` on all problems in a directory. Useful for building a .lib file, or for evaluating how emna performs. Outputs useful information for each problem into `./batch.log`.



Choose induction variables by machine learning
----------------------------------------------
When you have a .lib file that you want to use in order to make predictions of induction variables, run:

1. extractFeatures
2. learn

Subsequent invocations of `emna` will use the generated classifier to choose induction order.


#### extractFeatures.hs
```
extractFeatures /path/to/library.lib depth feature-extraction-schemes
```
Extracts features from the given library into the PostgreSQL database. Will wipe the database beforehand, so use with care!

Looks for the environment variables `HS_DB_NAME`, `HS_DB_HOST`, `HS_DB_USERNAME` and `HS_DB_PASSWORD`.

#### learn.py
```
python learn.py [/path/to/data]
```
Creates `classifier.pkl` from the data currently in the PostgreSQL database. 

#### classify.py
_Used only internally by HipSpec, there should be no need to call this directly._
```
python classify.py stringifiedFeatures [/path/to/data]
```
Reads `classifier.pkl` and classifies `stringifiedFeatures` by it, returning the most probable classes on stdout.


Evaluating feature extraction schemes
-------------------------------------
TODO
#### validation.py

#### unsupervised.py

Other files
-----------
#### db.py
_Used only internally by other scripts, there should be no need to call this directly._

Connects to the local PostgreSQL database, and supplies utility functions for reading lemmas/classes/features from it.

#### tables.sql
Contains definitions of PostgreSQL tables.
