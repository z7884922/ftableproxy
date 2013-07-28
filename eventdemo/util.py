
def getRequestArg(request, field, default):
    start = request.GET.get('start')
    if start is None:
        start = default
    else:
        start = int(start)
    return start
