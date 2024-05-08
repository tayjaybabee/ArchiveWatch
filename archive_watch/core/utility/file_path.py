"""

Since: v1.0.0

This module provides utility functions for handling file paths and extensions.

It includes functions to check if a path exists, provision a path by expanding and resolving it, preparing a path by
converting, provisioning, and checking its existence, checking if a path leads to a file or directory, checking if a
file has a valid extension, and retrieving the extension from a file path.

Example:
    >>> from pathlib import Path
    >>> from archive_watch.core.utility.file_path import (
    ...     check_path_exists,
    ...     provision_path,
    ...     prepare_path,
    ...     check_file,
    ...     check_dir,
    ...     check_extension,
    ...     get_extension,
    ... )

    # Check if a path exists
    >>> check_path_exists(Path('example.txt'))
    False

    # Provision a path
    >>> provision_path(Path('~/Documents/file.txt'), do_not_expand=True)
    PosixPath('~/Documents/file.txt')

    # Prepare a path
    >>> prepare_path('~/Documents/file.txt', do_not_expand=True)
    PosixPath('~/Documents/file.txt')

    # Check if a path leads to a file
    >>> check_file(Path('example.txt'))
    False

    # Check if a path leads to a directory
    >>> check_dir(Path('example_folder'))
    False

    # Check if a file has a valid extension
    >>> check_extension(Path('example.txt'))
    False

    # Retrieve the extension from a file path
    >>> get_extension(Path('example.txt'))
    'txt'
"""


from pathlib import Path
from typing import Union, Optional

from archive_watch.core.common.constants import FILE_EXTENSIONS
from ..errors import *


__all__ = [
    'check_dir',
    'check_extension',
    'check_file',
    'check_path_exists',
    'get_extension',
    'prepare_path',
    'provision_path'
]


def check_dir(path):
    """
    Checks if a given path exists and is a directory.

    Parameters:
        path (Path):
            The path to check.

    Returns:
        bool:
            :obj:`True` if the path exists and is a directory, :obj:`False` otherwise.

    Example:
        >>> from pathlib import Path
        >>> check_dir(Path('example_folder'))
        False
    """
    if not check_file(path):
        return path.is_dir()


def check_extension(
        file_path:         Union[str, Path],
        valid_extensions:  list = FILE_EXTENSIONS,
        no_provision:      bool = False,
        no_existing_check: bool = False,
):
    """
    Checks if a file has a valid extension.

    Parameters:
        file_path (Union(str, Path)):
            The file path to check.

        valid_extensions (list):
            A list of valid file extensions.

        no_provision (Optional[bool]):
            If set to :obj:`True`, the file path is not provisioned.

        no_existing_check (Optional[bool]):
            If set to :obj:`True`, the file existence is not checked.

    Returns:
        bool:
            :obj:`True` if the file has a valid extension, :obj:`False` otherwise.

    Example:
        >>> from pathlib import Path
        >>> check_extension(Path('example.txt'))
        False
    """
    if not no_provision:
        file_path = prepare_path(file_path, no_existing_check)

    ext = get_extension(file_path, no_provision=no_provision)

    if ext.lower() in valid_extensions:
        return True

    return False


def check_file(file_path: Path):
    """
    Checks if a given file path exists and is a regular file.

    Parameters:
        file_path (Path):
            The file path to check.

    Raises:
        TypeError:
            If the provided :py:obj:`file_path` is not an instance of :class:`pathlib.Path`.

        NotAFileError:
            If the provided :py:obj:`file_path` does not point to a regular file.

    Returns:
        bool:
            :obj:`True` if the file exists and is a regular file, :obj:`False` otherwise.

    Example:
        >>> check_file(Path('some_file.txt'))
        True
        >>> check_file(Path('nonexistent_file.txt'))
        False
    """
    if not isinstance(file_path, Path):
        raise TypeError(f'`file_path` must be a `pathlib.Path` object. Not {type(file_path)}!')

    check_path_exists(file_path)

    return file_path.is_file()


def check_path_exists(file_path: Path) -> bool:
    """
    This function checks if a given file path exists.

    Parameters:
        file_path (Path): The file path to check. It should be an instance of :class:`Path`.

    Raises:
        TypeError:
            If the provided :py:obj:`file_path` is not an instance of :class:`pathlib.Path`.

    Returns:
        bool:
            :obj:`True` if the file path exists, :obj:`False` otherwise.

    Example:
        >>> check_path_exists(Path('some_file.txt'))
        True
        >>> check_path_exists(Path('nonexistent_file.txt'))
        False
    """
    if not isinstance(file_path, Path):
        raise TypeError(f'`file_path` must be a `pathlib.Path` object not `{type(file_path)}`!')

    return file_path.exists()


def get_extension(
        file_path: Union[str, Path],
        no_provision: bool = False,
        no_strip_dot: bool = False,
        no_prepare: bool = False,
        no_existing_check: bool = False
):
    """
    Gets the extension of a file path.

    Parameters:
        file_path (Union[str, Path]):
            The file path.

        no_provision (Optional[bool]):
            If set to :obj:`True`, the file path is not provisioned.

        no_strip_dot (Optional[bool]):
            If set to :obj:`True`, the leading dot in the extension is not stripped.

        no_prepare (Optional[bool]):
            If set to :obj:`True`, the file path is not prepared.

        no_existing_check (Optional[bool]):
            If set to :obj:`True`, the file existence is not checked.

    Raises:
        NotAFileError:
            If the provided path does not point to a regular file.

    Returns:
        str: The file extension.

    Example:
        >>> from pathlib import Path
        >>> get_extension(Path('example.txt'))
        'txt'
    """
    if not no_prepare:
        file_path = prepare_path(
            file_path,
            no_provision=no_provision,
            no_existing_check=no_existing_check
        )

    if not check_file(file_path):
        raise NotAFileError(f'{str(file_path)} is not a file!')

    suffix = file_path.suffix

    if suffix.startswith('.'):
        if not no_strip_dot:
            return suffix[1:]

    return suffix


def prepare_path(
        path:              Union[str, Path],
        do_not_expand:     Optional[bool] = False,
        do_not_resolve:    Optional[bool] = False,
        no_convert:        Optional[bool] = False,
        no_provision:      Optional[bool] = False,
        no_existing_check: Optional[bool] = False
) -> Path:
    """
    This function prepares a given path. It converts, provisions, and checks the existence of the path based on the
    flags set.

    Parameters:
        path (Union[str, Path]):
            The path to prepare. It can be an instance of :class:`pathlib.Path` or a :class:`string`.

        do_not_expand (Optional[bool]):
            If set to :obj:`True`, the user's home directory (~) in the :py:obj:`path` **will not** be expanded.
            (Defaults to :obj:`False`)

        do_not_resolve (Optional[bool]):
            If set to :obj:`True`, the symbolic links in the path **will not** be resolved.
            (Defaults to :obj:`False`)

        no_convert (Optional[bool]):
            If set to :obj:`True`, the function will not convert a :class:`string` path to a :class:`pathlib.Path`
            object. (Defaults to :obj:`False`)

        no_provision (Optional[bool]):
            If set to :obj:`True`, the function will not provision the path.
            (Defaults to :obj:`False`)

        no_existing_check (Optional[bool]):
            If set to :obj:`True`, the function will not check if the path exists.
            (Defaults to :obj:`False`)

    Returns:
        Path:
            The prepared path.

    Example:
        >>> prepare_path('~/Documents/test.txt', no_provision=True)
        PosixPath('~/Documents/test.txt')
    """
    if not no_convert:

        if isinstance(path, str):
            path = Path()

    if not no_provision:
        path = provision_path(
            path,
            do_not_expand=do_not_expand,
            do_not_resolve=do_not_resolve,
            no_convert=True
        )

    if not no_existing_check:
        check_path_exists(path)

    return path


def provision_path(
        file_path:      Union[str, Path],
        do_not_expand:  Optional[bool] = False,
        do_not_resolve: Optional[bool] = False,
        no_convert:     Optional[bool] = False,
):
    """
    This function provisions a given file path. It expands and resolves the file path if the respective flags are not
    set.

    Parameters:
        file_path (Union(str, Path)):
            The file path to provision. It should be an instance of :class:`pathlib.Path` or a :class:`string`.

        do_not_expand (Optional[bool]):
            If set to :obj:`True`, the user's home directory (~) in the :py:obj:`file_path` **will not** be expanded.
            (Defaults to :obj:`False`)

        do_not_resolve (Optional[bool]):
            If set to :obj:`True`, the symbolic links in the file path **will not** be resolved.
            (Defaults to :obj:`False`)

        no_convert (Optional[bool]):
            If set to :obj:`True`, the function will not convert a :class:`string` file path to a :class:`pathlib.Path`
            object. (Defaults to :obj:`False`)

    Raises:
        TypeError:
            If the provided :py:obj:`file_path` is neither a :class:`string` nor an instance of :class:`pathlib.Path`.

    Returns:
        Path:
            The provisioned file path.

    Example:
        >>> provision_path('~/Documents/test.txt', do_not_expand=True)
        PosixPath('~/Documents/test.txt')
    """
    if not isinstance(file_path, Path):
        if not no_convert and isinstance(file_path, str):
            return prepare_path(file_path, do_not_expand, do_not_resolve)

        raise TypeError(f'`file_path` must be a `pathlib.Path` object not `{type(file_path)}`!')

    if not do_not_expand:
        file_path.expanduser()

    if not do_not_resolve:
        file_path.resolve()

    return file_path
