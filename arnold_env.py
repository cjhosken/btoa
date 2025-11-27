import os, pathlib

root = pathlib.Path.home() / ".arnold" / "install" / "arnoldusd"

os.environ["PXR_PLUGINPATH_NAME"] = f"{root/'plugin'}:{root/'lib/usd'}"
os.environ["LD_LIBRARY_PATH"] = f"{root/'bin'}:{os.environ.get('LD_LIBRARY_PATH','')}"
os.environ["PATH"] = f"{root/'bin'}:{os.environ.get('PATH','')}"