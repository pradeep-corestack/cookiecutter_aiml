from dynaconf import Dynaconf

# can also be taken from environment variables
config = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=["config.toml", ".secrets.toml"],
)

