import importlib
import logging

callback_modules = set()
_SEMAPHORE = False


def autodiscover_callbacks(packages=None, related_name='callbacks'):
    global _SEMAPHORE
    if _SEMAPHORE:
        return
    _SEMAPHORE = True
    try:
        modules = [find_related_module(pkg, related_name) for pkg in packages]
        logging.info(f'Found {len(modules)} callback modules')
        callback_modules.update(m.__name__ for m in modules if m)
    finally:
        _SEMAPHORE = False


def find_related_module(package, related_name):
    try:
        module = importlib.import_module(package)
        if not related_name and module:
            return module
    except ModuleNotFoundError:
        package, _, _ = package.rpartition('.')
        if not package:
            raise

    module_name = f'{package}.{related_name}'
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError as e:
        import_exc_name = getattr(e, 'name', None)
        if import_exc_name and module_name == import_exc_name:
            return

        raise e
