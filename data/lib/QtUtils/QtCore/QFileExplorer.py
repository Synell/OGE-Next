#----------------------------------------------------------------------

    # Libraries
import os
#----------------------------------------------------------------------

    # Class
class QFileExplorer:
    def __new__(cls):
        return None

    @staticmethod
    def get_files(directory = None, extensions = [], sub_dir = True, only_files = False):
        if directory is None:
            return None

        total_files = []
        for x in range(len(extensions)):
            extensions[x] = extensions[x].replace('.', '')

        if sub_dir:
            for (now, subfolders, files) in os.walk(directory):
                for x in files:
                    if x.split('.')[-1] in extensions:
                        if only_files:
                            total_files.append(x)
                        else:
                            total_files.append(f'{now}\\{x}')
        else:
            if only_files:
                total_files = [ file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file)) if file.split('.')[-1] in extensions and len(file.split('.')) > 1 ]
            else:
                total_files = [ f'{directory}{file}' for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file)) if file.split('.')[-1] in extensions and len(file.split('.')) > 1 ]

        return total_files
#----------------------------------------------------------------------
