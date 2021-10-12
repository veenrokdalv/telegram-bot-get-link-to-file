from aiogram import Dispatcher
from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import InlineQuery

from settings import DEFAULT_LOCALE


class TranslatedInlineQueryTextFilter(BaseFilter):
    trquery: str

    async def __call__(self, inline_query: InlineQuery, _) -> dict[str, str]:
        query = _(inline_query.query, locale=DEFAULT_LOCALE)
        trquery = _(self.trquery, locale=DEFAULT_LOCALE)
        query_args = query.replace(inline_query_text, '')
        if inline_query_text in query:
            return {'query_args': query_args}


def setup(dispatcher: Dispatcher):
    dispatcher.inline_query.bind_filter(TranslatedInlineQueryTextFilter)
