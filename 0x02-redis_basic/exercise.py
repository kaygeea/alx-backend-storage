#!/usr/bin/env python3
"""Create a class for caching with Redis"""
import redis
from typing import Union
import uuid


class Cache:
    """
    A simple Redis cache implementation for storing and retrieving data.

    This class provides basic caching functionality using a Redis database.
    It allows storing various data types (strings, bytes, integers, floats)
    under unique keys generated using UUIDs.

    Attributes:
        __redis (redis.Redis): A connection to the Redis server.

    Methods:
        __init__() -> None:
            Initializes the cache and flushes the Redis database.

        store(data: Union[str, bytes, int, float]) -> str:
            Stores the provided data in Redis and returns the associated key.
    """
    def __init__(self) -> None:
        """
        Initialize a Cache object

        This method creates a connection to the Redis server and flushes any
        exising data in the Redis database.
        """
        self.__redis = redis.Redis()
        self.__redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store input data in the Redis cache and returns the associated key.

        This method attempts to store the given `data` in the underlying Redis
        database. It generates a unique key using `uuid.uuid4()` to associate
        with the data for future retrieval.

        Arg:
            data (Union[str, bytes, int, float]): The data to be cached.
            Supported data types include strings, bytes, integers, and floats.

        Returns:
            str: The unique gen'd key to which the stored data is associated.
        """
        key = str(uuid.uuid4())  # Redis keys can ONLY be of type str
        self.__redis.set(key, data)
        return key
