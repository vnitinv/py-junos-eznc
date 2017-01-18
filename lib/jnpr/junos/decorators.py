# stdlib
from functools import wraps
from jnpr.junos.exception import RpcError
from jnpr.junos.jxml import normalize_xslt


def timeoutDecorator(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if 'dev_timeout' in kwargs:
            try:
                dev = args[0].dev
            except:
                dev = args[0]
            restore_timeout = dev.timeout
            dev.timeout = kwargs.pop('dev_timeout', None)
            try:
                result = function(*args, **kwargs)
                dev.timeout = restore_timeout
                return result
            except Exception:
                dev.timeout = restore_timeout
                raise
        else:
            try:
                return function(*args, **kwargs)
            except Exception:
                raise

    return wrapper


def normalizeDecorator(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if 'normalize' in kwargs:
            normalize = kwargs.pop('normalize', None)
            try:
                dev = args[0].dev
            except:
                dev = args[0]

            if dev._normalize != normalize:
                restore_transform = dev.transform

                if normalize is False:
                    try:
                        dev.transform = dev._nc_transform
                        result = function(*args, **kwargs)
                        dev.transform = restore_transform
                        return result
                    except Exception:
                        dev.transform = restore_transform
                        raise
                else:
                    try:
                        dev.transform = dev._norm_transform
                        result = function(*args, **kwargs)
                        dev.transform = restore_transform
                        return result
                    except Exception:
                        dev.transform = restore_transform
                        raise
            else:
                try:
                    return function(*args, **kwargs)
                except Exception:
                    raise
        else:
            try:
                return function(*args, **kwargs)
            except Exception:
                raise

    return wrapper


def ignoreWarnDecorator(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if 'ignore_warning' in kwargs:
            ignore_warn = kwargs.pop('ignore_warning', None)
            if ignore_warn is True:
                try:
                    result = function(*args, **kwargs)
                    return result
                except RpcError as ex:
                    # ignore warning
                    if hasattr(ex, 'rpc_error') and\
                                    ex.rpc_error['severity'] == 'warning':
                        return ex.rsp.getparent()
                    else:
                        raise ex
                except Exception:
                    raise
            else:
                try:
                    return function(*args, **kwargs)
                except Exception:
                    raise
        else:
            try:
                return function(*args, **kwargs)
            except Exception:
                raise

    return wrapper