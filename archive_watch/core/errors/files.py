class NotAFileError(FileExistsError):
    pass


class NotADirectoryError(NotADirectoryError):
    pass


__all__ = [
    'NotAFileError',
    'NotADirectoryError',
]
