#!/usr/bin/env python3
"""Create a class for caching with Redis"""
from functools import wraps
import redis
from typing import Callable, Union
import uuid


def count_calls(method: Callable) -> Callable:
    """
    Count number of calls to a method and store the count in Redis.

    This decorator attempts to create and return a function that increments
    the count for a given key everytime the method is called. It also returns
    the value returned by the original method.
    """
    @wraps(method)
    def wrapper_count_calls(self, *args, **kwargs):
        """Wrap the method and increment the call count."""
        method_val = method(self, *args, **kwargs)
        self._redis.incr(method.__qualname__, 1)
        return method_val
    return wrapper_count_calls

def call_history(method: Callable) -> Callable:
    """
    Store history of inputs and outputs for a particular function
    """
    @wraps(method)
    def wrapper_call_history(self, *args, **kwargs):
        """Wrap the method and store its input & output in respective lists"""
        
        # Create the respective keys for the I & O lists
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        # Create & append data into the lists
        self._redis.rpush(input_key, str(args))
        func_output = method(self, *args, **kwargs)  # Get function output
        self._redis.rpush(output_key, func_output)
        return func_output
    return wrapper_call_history


class Cache:
    """
    A simple Redis cache implementation for storing and retrieving data.

    This class provides basic caching functionality using a Redis database.
    It allows storing various data types (strings, bytes, integers, floats)
    under unique keys generated using UUIDs.

    Attributes:
        _redis (redis.Redis): A connection to the Redis server.

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

    @count_calls
    @call_history
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
