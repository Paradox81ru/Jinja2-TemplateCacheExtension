# Jinja2-TemplateCacheExtension

## Описание
**TemplateCacheExtension** - расширение для Jinja2, кэширование фрагментов шаблона в Django. Добавляет в шаблонизатор Jinja2 тэг *{% cache %} {% endcache %}* по функционалу максимально напомнинающий одноименный тэг родного шаболнизатора Django.

## Установка
Для глобальной установки расширения в шаблонизатор требуется подключить его в файле настроек "[settings.py](settings.py)". Либо это расширение можно подколючить в экземпляр окружения Jinja2: 
`env = Environment(extensions=["path_to_extensions.TemplateCacheExtension"], \**options)`

