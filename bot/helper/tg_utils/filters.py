from telegram.ext import MessageFilter

from bot import AUTHORIZED_CHATS, OWNER_ID, SUDO_USERS


class CustomFilters:
    class _OwnerFilter(MessageFilter):
        @staticmethod
        def filter(message):
            return bool(message.from_user.id == OWNER_ID)

    owner_filter = _OwnerFilter()

    class _AuthorizedUserFilter(MessageFilter):
        @staticmethod
        def filter(message):
            id = message.from_user.id
            return bool(id in AUTHORIZED_CHATS or id in SUDO_USERS or id == OWNER_ID)

    authorized_user = _AuthorizedUserFilter()

    class _AuthorizedChat(MessageFilter):
        @staticmethod
        def filter(message):
            return bool(message.chat.id in AUTHORIZED_CHATS)

    authorized_chat = _AuthorizedChat()

    class _SudoUser(MessageFilter):
        @staticmethod
        def filter(message):
            return bool(message.from_user.id in SUDO_USERS)

    sudo_user = _SudoUser()
