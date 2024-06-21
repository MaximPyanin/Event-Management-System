from typing import get_type_hints, Union


class AppConfigError(Exception):
    pass


class AppConfig:
    POSTGRES_URI: str
    PRIVATE_KEY: str
    PUBLIC_KEY: str

    SENDER_EMAIL: str

    PAPERTRAIL_HOST: str

    SENDER_PHONE: str

    ACCOUNT_SID: str
    AUTH_TOKEN: str
    PAPERTRAIL_PORT: int

    SENDGRID_API_KEY: str
    DOMAIN: str

    def __init__(self, env):
        for field in self.__annotations__:
            if not field.isupper():
                continue

            default_value = getattr(self, field, None)
            if default_value is None and env.get(field) is None:
                raise AppConfigError("The {} field is required".format(field))

            var_type = get_type_hints(AppConfig)[field]
            try:
                if var_type == bool:
                    value = self._parse_bool(env.get(field, default_value))
                elif var_type == list[int]:
                    value = list(
                        map(
                            lambda item: int(item),
                            self._parse_list(env.get(field, default_value)),
                        )
                    )
                elif var_type == list[str]:
                    value = self._parse_list(env.get(field, default_value))
                else:
                    value = var_type(env.get(field, default_value))

                self.__setattr__(field, value)
            except ValueError:
                err_msg = (
                    'Unable to cast value of "{}" to type "{}" for "{}" field'.format(
                        env[field], var_type, field
                    )
                )

                raise AppConfigError(err_msg)

    def __repr__(self):
        return str(self.__dict__)

    @staticmethod
    def _parse_bool(val: Union[str, bool]) -> bool:
        return val if type(val) == bool else val.lower() in ["true", "yes", "1"]

    @staticmethod
    def _parse_list(val: Union[str, list]) -> list:
        match val:
            case str():
                if "," not in val:
                    return [val]

                return val.split(",")

            case _:
                return val
