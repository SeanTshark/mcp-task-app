class HttpExceptionError(Exception):
    def __init__(self, status_code):
        self.status_code = status_code


def http_exception_error(status_code):
    # HTTP 100 Error Codes
    if status_code == 100:
        pass
    elif status_code == 101:
        pass
    elif status_code == 102:
        pass
    elif status_code == 103:
        pass

    # HTTP 300 Error Codes
    elif status_code == 300:
        pass
    elif status_code == 301:
        pass
    elif status_code == 302:
        pass
    elif status_code == 303:
        pass
    elif status_code == 304:
        pass
    elif status_code == 307:
        pass
    elif status_code == 308:
        pass

    #HTTP 400 Error Codes
    elif status_code == 400:
        pass
    elif status_code == 401:
        pass
    elif status_code == 402:
        pass
    elif status_code == 403:
        pass
    elif status_code == 404:
        pass
    elif status_code == 405:
        pass
    elif status_code == 406:
        pass
    elif status_code == 407:
        pass
    elif status_code == 408:
        pass
    elif status_code == 409:
        pass
    elif status_code == 410:
        pass
    elif status_code == 411:
        pass
    elif status_code == 412:
        pass
    elif status_code == 413:
        pass
    elif status_code == 414:
        pass
    elif status_code == 415:
        pass
    elif status_code == 416:
        pass
    elif status_code == 417:
        pass
    elif status_code == 418:
        pass
    elif status_code == 421:
        pass
    elif status_code == 422:
        pass
    elif status_code == 423:
        pass
    elif status_code == 424:
        pass
    elif status_code == 425:
        pass
    elif status_code == 426:
        pass
    elif status_code == 428:
        pass
    elif status_code == 429:
        pass
    elif status_code == 431:
        pass
    elif status_code == 451:
        pass

    # HTTP 500 Error Codes
    elif status_code == 500:
        pass
    elif status_code == 501:
        pass
    elif status_code == 502:
        pass
    elif status_code == 503:
        pass
    elif status_code == 504:
        pass
    elif status_code == 505:
        pass
    elif status_code == 506:
        pass
    elif status_code == 507:
        pass
    elif status_code == 508:
        pass
    elif status_code == 510:
        pass
    elif status_code == 511:
        pass

    #MCP Server Error Codes
    elif status_code == -32700:
        pass
    elif status_code == -32600:
        pass
    elif status_code == -32601:
        pass
    elif status_code == -32602:
        pass
    elif status_code == -32603:
        pass
    elif -32099 <= status_code <= -32000:
        pass

