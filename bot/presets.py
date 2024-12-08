import builtins
import datetime

from colorama import Back, Fore, Style


def prefix():
    return (Back.BLACK + Fore.GREEN + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") + Back.RESET + Fore.WHITE +
            Style.BRIGHT)


def print(*args, **kwargs):
    """
    Custom print function that adds a prefix to the start of the output.
    """
    message = prefix() + ' ' + ' '.join(map(str, args))
    # Call the original print function from the builtins module
    builtins.print(message, **kwargs)


async def ban(member, reason):
    await member.ban(reason=reason)


async def kick(member):
    await member.kick()


def log(content):
    print(prefix() + content)


def datetime_now():
    return datetime.datetime.now(datetime.UTC)


def convert_datetime_from_str(datetime_str: None | str) -> None | datetime.datetime:
    formats = ["%d.%m.%Y %H:%M", "%d-%m-%Y %H:%M", "%d/%m/%Y %H:%M"]
    for fmt in formats:
        try:
            datetime_obj = datetime.datetime.strptime(datetime_str, fmt)
            datetime_obj.replace(tzinfo=datetime.timezone.utc)
            return datetime_obj
        except ValueError:
            pass
    else:
        return None
