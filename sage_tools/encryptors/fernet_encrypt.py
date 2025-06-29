from typing import Union

from .base import Encryptor

try:
    from cryptography.fernet import Fernet, InvalidToken
except ImportError as e:
    raise ImportError(
        "Install `cryptography` package. Run `pip install cryptography`."
    ) from e


class FernetEncryptor(Encryptor):
    """Fernet encryption class.

    This class uses the Fernet symmetric encryption method provided by the `cryptography` package to encrypt and decrypt data.

    Parameters
    ----------
    secret_key : str
        The secret key used for encryption and decryption. Must be a URL-safe base64-encoded 32-byte key.

    Methods
    -------
    encrypt(data: str) -> str
        Encrypts the given data using Fernet encryption.
    decrypt(data: str) -> str
        Decrypts the given data using Fernet encryption.

    Examples
    --------
    >>> secret_key = Fernet.generate_key()
    >>> encryptor = FernetEncryptor(secret_key)
    >>> encrypted_data = encryptor.encrypt("Hello, World!")
    >>> decrypted_data = encryptor.decrypt(encrypted_data)
    >>> decrypted_data
    'Hello, World!'

    """

    def __init__(self, secret_key: Union[str, bytes]):
        """Initialize the Fernet encryptor with a secret key.

        Args:
            secret_key: A URL-safe base64-encoded 32-byte key for encryption.
                       Can be string or bytes.

        Raises:
            ValueError: If the secret key is invalid.
        """
        try:
            if isinstance(secret_key, str):
                secret_key = secret_key.encode("utf-8")
            self.fernet = Fernet(secret_key)
        except Exception as e:
            raise ValueError(f"Invalid secret key provided: {e}") from e

    def encrypt(self, data: str) -> str:
        """Encrypts the given data using Fernet encryption.

        Parameters
        ----------
        data : str
            The data to be encrypted.

        Returns
        -------
        str
            The encrypted data.

        """
        self._validate_data(data)
        data = self._encode_data(data)
        encrypted_value = self.fernet.encrypt(data)
        return encrypted_value.decode("utf-8")

    def decrypt(self, data: str) -> str:
        """Decrypts the given data using Fernet encryption.

        Parameters
        ----------
        data : str
            The data to be decrypted.

        Returns
        -------
        str
            The decrypted data.

        Raises
        ------
        ValueError
            If the data cannot be decrypted (invalid token).

        """
        self._validate_data(data)
        data = self._encode_data(data)
        try:
            return self.fernet.decrypt(data).decode("utf-8")
        except InvalidToken as e:
            raise ValueError(
                "Unable to decrypt data. Invalid token or corrupted data."
            ) from e
        except Exception as e:
            raise ValueError(f"Decryption failed: {e}") from e

    def _validate_data(self, data):
        """Validates the data to ensure it is either a string or bytes.

        Parameters
        ----------
        data : str or bytes
            The data to be validated.

        Raises
        ------
        TypeError
            If the data is not a string or bytes.

        """
        if not isinstance(data, (str, bytes)):
            raise TypeError(
                "FernetEncryptor only supports string or bytes data types for encryption."
            )

    def _encode_data(self, data):
        """Encodes the data to bytes if it is a string.

        Parameters
        ----------
        data : str or bytes
            The data to be encoded.

        Returns
        -------
        bytes
            The encoded data.

        """
        if isinstance(data, str):
            data = data.encode("utf-8")
        return data
