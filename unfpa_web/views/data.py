#!/usr/bin/env python
# encoding=utf-8
# maintainer: alou/fad


def rate_cal(*args):
    try:
        return (args[0] * 100) / args[1]
    except:
        return 0
