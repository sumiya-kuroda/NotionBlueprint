from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("NotionBlueprint")
except PackageNotFoundError:
    # package is not installed
    pass
