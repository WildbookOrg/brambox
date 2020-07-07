# -*- coding: utf-8 -*-
def main():  # nocover
    import brambox

    print('Looks like the imports worked')
    print('brambox = {!r}'.format(brambox))
    print('brambox.__file__ = {!r}'.format(brambox.__file__))
    print('brambox.__version__ = {!r}'.format(brambox.__version__))


if __name__ == '__main__':
    """
    CommandLine:
       python -m brambox
    """
    main()
