class DatabaseError(Exception):
    pass


class ValidationError(DatabaseError):
    pass


class RecordNotFoundError(DatabaseError):
    pass