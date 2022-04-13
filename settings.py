# either
TEMPLATES = [
    {
        'NAME': 'jinja2',
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': 'DjangoProject.jinja2.environment',
            'autoescape': False,
            'trim_blocks': True,
            "extensions": [
                "jinja2.ext.do",
                "jinja2.ext.i18n",
                "path_to_extensions.TemplateCacheExtension"
            ],
        }
    }
]

# or
env = Environment(extensions=["path_to_extensions.TemplateCacheExtension"], **options)
