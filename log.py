#!/usr/bin/env python
#-*- coding: utf-8 -*-
import logging

FORMAT = '%(asctime)-15s [%(levelname)s] %(name)s: %(message)s'
DATEFMT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(format=FORMAT, level=logging.INFO, datefmt=DATEFMT)
