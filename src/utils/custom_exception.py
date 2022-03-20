import gzip


class PipelineException(Exception):
    """Pipeline Base class for other exceptions"""
    pass


class MoveFileException(PipelineException):
    """Raised when something went wrong saving file to RAW"""
    pass


class DecompressException(gzip.BadGzipFile):
    """Raised when something went wrong descompressing file"""
    def __init__(self, infile, message="Error while decompressing file"):
        self.infile = infile
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message + f" :: {self.infile}"


class ReadCSVException(PipelineException):
    """Raised when something went wrong descompressing file"""
    pass
