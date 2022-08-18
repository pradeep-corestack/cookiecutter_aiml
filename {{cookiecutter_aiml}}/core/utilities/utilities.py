import base64
import functools
import json
from itertools import chain
from itertools import zip_longest
from typing import Dict
from typing import List

import numpy as np
import pandas as pd
from core.utilities.consts import ModelEnum
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import modes
from kats.consts import ModelEnum
from kats.consts import TimeSeriesData

# from kats.models.metalearner.get_metadata import GetMetaData
from statsmodels.tsa.stattools import adfuller


class AESCipher:
    def __init__(self, crypt_key="C0r3&t@ck"):
        self.crypt_key = crypt_key
        self.BLOCK_SIZE = 16
        self.padding = "{"

    def decrypt(self, cipher_text: str) -> str:

        cipher = self.__get_cipher()

        # get the decryptor object
        decryptor = cipher.decryptor()

        # get the base64 decoded text
        base64_decoded = self.__decode(cipher_text)

        # decyrpt to plain text
        plain_text = decryptor.update(base64_decoded) + decryptor.finalize()

        # decode bytes to str and strip the padded text if present
        return plain_text.decode("utf-8").rstrip(self.padding)

    def encrypt(self, plain_text: str) -> str:
        cipher = self.__get_cipher()

        # get the encryptor object
        encryptor = cipher.encryptor()

        # pad text to block size
        padded_text = self.__pad(plain_text)

        # encrypt the padded text and finalize
        cipher_text = encryptor.update(padded_text.encode("utf-8"))

        # return the cipher text encoded in base64 format
        return self.__encode(cipher_text)

    def __encode(self, text: bytes) -> str:
        """base 64 encoding"""
        return base64.b64encode(text).decode("utf-8")

    def __decode(self, text: str) -> bytes:
        """base 64 decode"""
        return base64.b64decode(text)

    @functools.lru_cache
    def __get_cipher(self) -> Cipher:
        reverse_key = zip_longest(self.crypt_key, self.crypt_key[::-1], fillvalue="")
        key = "".join(chain.from_iterable(reverse_key))[0:16][::-1]

        # form the cipher object to combine AES algorithm and mode
        # TODO {neelabalan.n}: move to Fernet cipher or CBC mode in AES
        return Cipher(algorithms.AES(key.encode("utf-8")), modes.ECB())

    def __pad(self, plain_text: str) -> str:
        return plain_text + (self.BLOCK_SIZE - len(plain_text) % self.BLOCK_SIZE) * self.padding


class DfUtils:
    @staticmethod
    def rename_columns(df: pd.DataFrame, old_col_names: list, new_column_names: list):
        col_rename_dict = {i: j for i, j in zip(old_col_names, new_column_names)}
        df.rename(columns=col_rename_dict, inplace=True)

    @staticmethod
    # TODO: {neelabalan.n} set format arg
    def convert_date_time_columns(df: pd.DataFrame, columns: list):
        df[columns].apply(pd.to_datetime, infer_datetime_format=True)
        return

    def convert_date_time_string(df: pd.DataFrame, column: str, format: str):
        df[column] = df[column].dt.strftime(format)
        return

    @staticmethod
    def drop_columns(df: pd.DataFrame, column_list: list):
        df.drop(column_list, axis="columns", inplace=True, errors="ignore")
        return

    @staticmethod
    def to_json(df: pd.DataFrame, orient: str = "records"):
        return df.to_json(orient=orient, default_handler=str)

    @staticmethod
    def to_dict(df: pd.DataFrame, orient: str = "records"):
        return df.to_dict(orient=orient)

    @staticmethod
    def sort_values(df: pd.DataFrame, columns: List, ascending=False, inplace=True):
        return df.sort_values(columns, ascending=ascending, inplace=inplace)


def adfuller_test(val: pd.Series):
    result = adfuller(val)
    pValue = result[1]
    print(f"ADF Statistic: {result[0]}")
    print(f"p-Value:\n{result[1]}\n".format(result[1]))
    print("Critical Values:")
    for key, value in result[4].items():
        print(f"{key}: {value}")
    if pValue >= 0.1:
        print("Null Hypothesis cannot be rejected. The time series is non-stationary")
    else:
        print("Null hypothesis is rejected at significance level a = {pValue}")


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


class ModelFactory:
    @staticmethod
    def get(time_series_data: TimeSeriesData, model: ModelEnum, params: Dict):
        param_class, model_class = ModelEnum.model_class(model)
        param_obj = param_class(**params)
        return model_class(time_series_data, param_obj)


def get_df_time_range(df, upper_bound, lower_bound):
    lval = df.loc[df["time"] <= upper_bound]
    return lval.loc[lval["time"] >= lower_bound]
