# Jinja2-TemplateCacheExtension

## Description
**[TemplateCacheExtension](jinja2_extension.py )** - extension for Jinja2, caching template fragments in Django. Adds a tag to the Jinja2 template engine *{% cache %} {% endcache %}* in terms of functionality, it resembles the tag of the same name of the native Django template engine as much as possible.

## Installation
To install the extension globally in the template engine, you need to connect it in the settings file "[settings.py](settings.py)". Or this extension can be connected to an instance of the Jinja2 environment: 
`env = Environment(extensions=["path_to_extensions.TemplateCacheExtension"], \**options)`

## Using
To cache a fragment, you need to enclose it in the tag *cache* as shown in the file [example.html](example.html).
```
{% cache 3600, "left-sidebar", request.user.username, using="cacheAliasName" %}
    {% include "for_inclusion/left_menu.html" %}
{% endcache %}
```
The first positional parameter specifies the cache lifetime, in this case it is *3600*. The following positional parameter defines the unique name of the cached fragment, in our example it is "*left-sidebar*". Next comes a number of optional positional parameters characterizing this cache, for example, in our case it is only the user name *request.user.username*, which will determine that for each authorized user the cached fragment will be its own. Last comes the optional named parameter *using* through which you can set the alias of the cache instance to be used for the fragment caching process. By default, this parameter has the value '*default*'.

To learn more about the extension for Jinja2, caching of template fragments in Django, its installation and use, you can visit my website "[Парадокс-Портал/Расширение для jinja2, кэширование фрагментов шаблона в Django](http://www.paradox-portal.ru/blog/article/8-rasshirenie_dlya_jinja2_keshirovanie_fragmentov_shablona_v_django)"
