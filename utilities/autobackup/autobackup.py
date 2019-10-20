import argparse
import distutils.dir_util as dir_util


def _parse_arguments():
    parser = argparse.ArgumentParser(description='Recursive backup '
            'of a folder to the specified destination.')
    parser.add_argument('--source',
            help='path to the existing folder to be backed-up')
    parser.add_argument('--destination',
            help='path to the folder to copy the files to')
    return parser.parse_args()


def backup(src_directory, dst_directory):
    """Backup the source directory `src_directory` to the destination
    directory `dst_directory`.

    Parameters
    ----------
    src_directory : str
        Source directory.
    dst_directory : str
        Destination directory.
    """
    dir_util.copy_tree(src_directory, dst_directory, update=1)


def main():
    arguments = _parse_arguments()
    print('Autobackup: copying the files from "%s" to "%s"...'
            %(arguments.source, arguments.destination))
    try:
        backup(arguments.source, arguments.destination)
    except dir_util.DistutilsFileError:
        print('The source path should point to a valid folder.')


if __name__ == '__main__':
    main()
