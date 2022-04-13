from jinja2 import Environment

def environment(**options):
    env = Environment(extensions=["path_to_extensions.TemplateCacheExtension"], **options)
    return env
