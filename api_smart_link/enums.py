from enum import Enum, auto


class StatusEnum(Enum):
    new = auto()
    approve = auto()
    decline = auto()


class SocialEnum(Enum):
    vk = 'vk'
    fb = 'fb'


class BanReasonEnum(Enum):
    """
    Взято отсюда: https://vk.com/dev/groups.ban
    """
    other = 0  # другое (по умолчанию)
    spam = 1  # спам
    abuse = 2  # оскорбление участников
    obscene = 3  # нецензурные выражения
    offtopic = 4  # сообщения не по теме


class OrderDirEnum(Enum):
    asc = 'asc'
    desc = 'desc'
