import pathlib
import tomli

path = pathlib.Path(__file__).parent / "config.toml"
with path.open(mode="rb") as fp:
    config1 = tomli.load(fp)

path2 = pathlib.Path(__file__).parent / "howto_config.toml"
with path2.open(mode="rb") as fp:
    config2 = tomli.load(fp)

config = config1 | config2