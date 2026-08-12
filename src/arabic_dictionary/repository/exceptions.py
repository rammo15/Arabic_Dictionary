"""
Repository exceptions.
"""


class RepositoryError(Exception):
    """Base repository exception."""


class EntryAlreadyExistsError(RepositoryError):
    """Entry already exists."""


class EntryNotFoundError(RepositoryError):
    """Entry not found."""
