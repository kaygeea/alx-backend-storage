#!/usr/bin/env python3
"""Create a class for caching with Redis"""
import redis
from typing import Callable, Union
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
        self._redis = redis.Redis()
        self._redis.flushdb()

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
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Callable[[bytes], Union[str, int]] = None
            ) -> Union[Union[str, int], bytes, None]:
        """
        Convert data back to desired format.

        This method attempts to retrieve data from the Redis store using the
        given key. It retrieves the data as a `bytes` format and converts it
        to the desired format.

        Args:
            key (str): The key with which the data is associated and to be
                       retrieved with.
            fn (callable): An optional callable that implements the conversion
                           of the retrieved data

        Raises:
            Raises an error based on the default `Redis.get` behaviour if the
            key does not exist.

        Returns:
            Union[str, int, bytes, None]: The data in the desired format or
                                          The data as `bytes`, if no fn or
                                          None if the key does not exist.
        """
        data = self._redis.get(key)
        if callable(fn):
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Parametrize `Cache.get()` with a string conversion function.

        This method attempts to apply a conversion function to convert
        `data` to a string.

        Arg:
            key (str): The associated key of the data to be retrieved.

        Raises:
            Raises an error based on the default `Redis.get` behaviour if the
            key does not exist.

        Returns:
            str: The data in string format.
        """
        return self.get(key, fn=str)

    def get_int(self, key: str) -> int:
        """
        Parametrize `Cache.get()` with an integer conversion function.

        This method attempts to apply a conversion function to convert
        `data` to an integer.

        Arg:
            key (str): The associated key of the data to be retrieved.

        Raises:
            Raises an error based on the default `Redis.get` behaviour if the
            key does not exist.

        Returns:
            int: The data as an int.
        """
        return self.get(key, fn=int)
