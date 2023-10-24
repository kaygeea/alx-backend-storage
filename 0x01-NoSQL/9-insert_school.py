#!/usr/bin/env python3
"""Create a function that inserts a new document into a collection"""

def insert_school(mongo_collection, **kwargs):
    """
    Insert a new document into a collection

    Args:
        mongo_collection - incoming argument for a pymongo collection object.
        kwargs - incoming keyword argument for content of document to be added
    
    Returns:
        The '_id' of the newly added document
    """
    
    new_document = {key:value for (key, value) in kwargs.items()}
    updated_collection = mongo_collection.insert_one(new_document)

    return updated_collection.inserted_id
