import pickle

import fsspec

from rubicon.repository import LocalRepository


class MemoryRepository(LocalRepository):
    """The memory repository persists Rubicon data to an
    in-memory filesystem representation.

    The memory repository is intended for testing and
    development purposes. Data persisted to the memory
    filesystem will not be persisted between runtimes.

    Parameters
    ----------
    root_dir : str, optional
        A path representing the virtual root directory for
        the in-memory filesystem. This does not need to be
        specified unless interacting with an already created
        in-memory filesystem.
    """

    PROTOCOL = "memory"

    def __init__(self, root_dir=None):
        self.filesystem = fsspec.filesystem(self.PROTOCOL)
        self.root_dir = root_dir.rstrip("/") if root_dir is not None else "/root"

        self.filesystem.mkdir(self.root_dir)

    def _persist_dataframe(self, df, path):
        """Persists the `dask` dataframe `df` to the in-memory
        path defined by `path`.
        """
        with self.filesystem.open(path, "wb") as f:
            pickle.dump(df, f)

    def _read_dataframe(self, path, df_type="pandas"):
        """Reads the dataframe from the in-memory
        path defined by `path`.
        """
        with self.filesystem.open(path, "rb") as f:
            data = pickle.load(f)

        return data
