import enum


class ItemType(enum.Enum):
    OFFER = 'OFFER'
    CATEGORY = 'CATEGORY'


IMPORT_UNIT_NAME_MAX_LENGTH = 200
IMPORT_UNIT_TYPE_CHOICES=((ItemType.OFFER.value, ItemType.OFFER.value), (ItemType.CATEGORY.value, ItemType.CATEGORY.value))