from jinja2 import nodes
from jinja2 import lexer
from jinja2.ext import Extension

from django.core.cache import caches
from django.core.cache.utils import make_template_fragment_key


class TemplateCacheExtension(Extension):
    """ Расширение кеширование фрагмента шаблона для Jinja2 """
    tags = {"cache"}

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        args, kwargs = self._get_token_args(parser)

        body = parser.parse_statements(end_tokens=("name:endcache",), drop_needle=True)
        return nodes.CallBlock(
            self.call_method("_cache_support", args, kwargs), [], [], body
        ).set_lineno(lineno)

    @classmethod
    def _get_token_args(cls, parser):
        """ Возвращает параметры блока кеширования """
        args = []
        kwargs = {}

        # Пока не будет достигнут конец знака блока
        while parser.stream.current.type != lexer.TOKEN_BLOCK_END:
            # будем анализировать входные параметры.
            # Во первых надо пропустить все запятые.
            if parser.stream.skip_if(lexer.TOKEN_COMMA):
                continue
            # Двлее получим очередной параметр,
            token = parser.parse_expression()
            # и проверим, если это параметр 'using', значит это указатель на вид cache-а,
            if isinstance(token, nodes.Name) and token.name == 'using':
                # и тогда перепрыгиваем знак равно,
                next(parser.stream)
                # получаем значение типа кэша, и добавляем его в виде ключевого параметра,
                kwargs = [nodes.Keyword('using', parser.parse_expression())]
                # и выходим из анализа параметров. так этот параметр должен быть последним.
                break
            # Все остальные параметры добавляем в позиционные параметры.
            args.append(token)
        return args, kwargs

    @classmethod
    def _cache_support(cls, *args, **kwargs):
        """ Кеширует указанный фрагмент шаблона """
        # Первым параметром должно быть время жизни кэша.
        timeout = args[0]
        # Вторым параметром должно быть название фрагмента.
        fragment_name = args[1]
        ext_name = []
        # Далее надо пройтись по всем оставшимся параметрам.
        if len(args) > 2:
            for i in range(2, len(args)):
                ext_name.append(args[i])
                # Если в блоке указан ключевой параметр 'using', значит через него передан алиас кэширования.
        cache = caches['default'] if 'using' not in kwargs else caches[kwargs['using']]
        # В эту переменную сохраняется функция возврата содержимого текущего фрагмента шаблона.
        caller = kwargs['caller']

        # Для начала надо сформировать ключ фрагмента, причем с учетом дополнительных параметров фрагмента.
        key = make_template_fragment_key(fragment_name, ext_name)
        # По ключу попробуем взять фрагмент из кэша.
        fragment = cache.get(key)
        # Если в кэше этого фрагмента ещё нет, или срок его истёк,
        if fragment is None:
            # то получим фрагмент из шаблона,
            fragment = caller()
            # и сразу отправим его в кэш.
            cache.set(key, fragment, timeout)
        # По окоанчанию работы с кэшем его лучше закрыть.
        cache.close()
        # Возвращаем полученный фрагмент.
        return fragment
