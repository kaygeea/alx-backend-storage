#!/usr/bin/env python3
"""Define a function that lists all documents in a collection"""

def list_all(mongo_collection):
    """
    List all documents in a MongoDB collection

    Arg:
        mongo_collection: Incoming argument for a pymongo collection object.

    Returns:
        A list of all documents in mongo_collection or
        an empty list if there is no document in mongo_collection.
    """
    return [docs for docs in mongo_collection.find()]
