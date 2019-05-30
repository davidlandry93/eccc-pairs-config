
# ECCC/PAIRS Query

This is a small utility to query Environment and Climate Change Canada (ECCC) data from an IBM PAIRS instance.

## Getting started

### Installation

To use this utility, you need the `ibmpairs` Python package on your system.
Visit the [project page](https://github.com/IBM/ibmpairs) for installation instructions.

### Usage

Once this dependency is installed, you can use this utility by simply calling the module:
```python
pairs_query.py query_file.json
```
The module reads `query_file.json` for instructions on what to fetch from the server.
This file also contains your login information to the server.
There is an example of valid query file in `examples/tt_query.json`.
To run this query, you first need to input your username and password to the API.

## Next steps

This utility is more of a proof of concept than a full featured product.
Feel free to modify it to suit your needs.
Notably, the `ID_OF_FIELD` dictionary does not contain the full list of fields available on the PAIRS platform.
You can find IDs to add to this dictionary yourself by visiting the platform directly at https://pairs-eccc.mybluemix.net/ .
