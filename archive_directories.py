#!/bin/python3
"""
Скрипт по архивированию директорий, находящихся в том же каталоге что и данный скрипт,
в архивы tar.gz. Архивы создаются в директории "archives" в данной директории
"""
import logging
import os.path
import tarfile
from os import listdir
from os import mkdir
from os.path import abspath
from os.path import basename
from os.path import exists
from os.path import isdir
from os.path import join
from shutil import rmtree

if __name__ == "__main__":
    # получаем путь к текущей директории
    curdir = os.path.dirname(os.path.realpath(__file__))
    backup_dir = os.path.normpath(join(curdir, 'archives'))
    #  clear or create backup_dir
    if listdir(curdir).count(basename(backup_dir)) == 1 and isdir(backup_dir):
        rmtree(abspath(backup_dir))
    try:
        mkdir(path=backup_dir, mode=0o777)
        # create log
        logging.basicConfig(filename=abspath(join(curdir, basename(__file__[:-3]+".log"))), format='%(asctime)s %(message)s',
                            level=logging.DEBUG)
        logging.debug(
            '\n\n\n=====================================================================================================')

        message = f'Директория {backup_dir} создана успешно!'
        logging.debug(message)
        print(message)
    except FileExistsError:
        message = f'Директория {backup_dir} существует или её нельзя создать по другой причине!'
        logging.debug(message)
        print(message)
        exit(1)
    # create backup
    for item in listdir(curdir):
        if isdir(abspath(join(curdir, item))):
            if abspath(join(curdir, item)) == backup_dir and exists(backup_dir):
                continue
            else:
                arch_name = abspath(join(abspath(backup_dir), f'{item}.tar.gz'))
                with tarfile.open(name=arch_name, mode='w:gz') as out:
                    out.add(name=abspath(join(curdir, item)))
                    out.close()
                    message = f'\t+{arch_name}'
                    logging.debug(message)
                    print(message)
    message = f'\n-------------------{backup_dir}--------------------------'
    logging.debug(message)
    print(message)
    message = listdir(abspath(join(abspath(backup_dir))))
    for m in message:
        print(m)
        logging.debug(m)
    logging.debug('')
    # os.system(f'ls -lah {abspath(join(abspath(backup_dir)))}')
