#!/bin/python3
"""
Скрипт по архивированию директорий, находящихся в том же каталоге что и данный скрипт,
в архивы tar.gz. Архивы создаются в директории "archives" в данной директории
"""
import hashlib
import logging
import os.path
import stat
import tarfile
from os import chmod
from os import listdir
from os import mkdir
from os.path import abspath
from os.path import basename
from os.path import exists
from os.path import isdir
from os.path import join
from shutil import rmtree


def calc_md5(filename: str, md5sumfilename=None) -> str:
    """
    Расчёт md5 суммы файла и возврат её в виде строки и запись в указанный файл.
    Что бы не записывать, просто не нужно указывать имя файла с хеш-суммой.
    :param filename: ПОЛНЫЙ путь к файлу по которому считается md5-сумма
    :param md5sumfilename: ПОЛНЫЙ путь к файлу в котором записано имя файла и его md5 сумма
    :return: расчитанная хешь сумма
    """
    if isinstance(filename, str):
        with open(filename, 'rb') as f:
            # читаем файл по блокам для оптимизации
            md5 = hashlib.md5()
            while chunk := f.read(8192):
                md5.update(chunk)
            # write hash to file
            if md5sumfilename is not None and isinstance(md5sumfilename, str) and os.path.isabs(md5sumfilename):
                with open(md5sumfilename, 'w') as f:
                    f.write(f'{md5.hexdigest()}  {basename(filename)}')
                    message = f'\t\tфайл \"{md5sumfilename}\" с md5 суммой {md5.hexdigest()} записан'
                    logging.debug(message)
                    print(message)
            return md5.hexdigest()
    else:
        return ''


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
        logging.basicConfig(filename=abspath(join(curdir, basename(__file__[:-3] + ".log"))),
                            format='%(asctime)s %(message)s',
                            level=logging.DEBUG)
        logging.debug(
            '\n\n\n===================================================================================================='
            '=')

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
                    # set all allow permissions on files and dirs
                    chmod(path=arch_name, mode=stat.S_IRWXG + stat.S_IRWXU + stat.S_IRWXO)
                    chmod(path=backup_dir, mode=stat.S_IRWXG + stat.S_IRWXU + stat.S_IRWXO)
                    # write to log
                    message = f'\t+{arch_name}'
                    logging.debug(message)
                    print(message)
                    calc_md5(filename=arch_name, md5sumfilename=f'{arch_name}.md5')
    message = f'\n-------------------{backup_dir}--------------------------'
    logging.debug(message)
    print(message)
    message = listdir(abspath(join(abspath(backup_dir))))
    for m in message:
        print(m)
        logging.debug(m)
    logging.debug('')
    # os.system(f'ls -lah {abspath(join(abspath(backup_dir)))}')
