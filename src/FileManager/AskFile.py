from src.Config import Config
from colorama import init, Fore, Back
import os
from .errors import InvalidInput
from src.Log import Log
from .GetListDirs import getListDirs

init(autoreset=True)


def askPath(info: str, baseDir: str = Config.read("Files", "data_dir"), prefix: str = "*", suffix: str = "*", isParent: bool = True):
    """Prompts the user to select a file from a directory.

    Parameters
    ----------
    info: str
        The info that will be logged 
    baseDir : str, optional
        The base directory to list files from, by default Config.read("Files", "data_dir")
    prefix  : str, optional
        The prefix of the files to list, by default "*"
    suffix  : str, optional
        The suffix  the files to list, by default "*"
    isParent  : bool, optional
        True for the main function, avoids to get duplicated logs, by default True

    Returns
    -------
    str
        The selected file path.

    Raises
    ------
    InvalidInput
        If the selected index is out of range
    """
    Log.log(f"{info}\n{prefix=}, {suffix=}", Log.info, save=isParent)

    baseDir = os.path.join(baseDir)
    if baseDir.endswith("\\"):
        baseDir = baseDir[:-1]
    print(f"Files in: {Fore.YELLOW}{baseDir}")
    listdir = getListDirs(baseDir, prefix, suffix)

    def centerChar(string, n=5):
        string = str(string)
        return string.center(n, " ")

    parent = os.path.dirname(baseDir)

    print(
        f"{Back.YELLOW +
            Fore.BLACK}{centerChar("-1")}{Back.RESET + Fore.RESET}: {parent}"
    )

    for index, el in enumerate(listdir):
        path = os.path.join(baseDir, el)
        if os.path.isfile(path):
            print(
                f"{Back.CYAN +
                    Fore.BLACK}{centerChar(index)}{Back.RESET + Fore.RESET}: {path}"
            )
        if not os.path.isfile(path):
            print(
                f"{Back.LIGHTMAGENTA_EX +
                    Fore.BLACK}{centerChar(index)}{Back.RESET + Fore.RESET}: {path}"
            )

    try:
        selectedIndex = int(
            input(f"{Fore.GREEN}Select the index of the file:{Fore.RESET}\n"))

        if selectedIndex == -1:
            selection = parent
        else:
            selection = os.path.join(baseDir, listdir[selectedIndex])
        if os.path.isdir(selection):
            selection = askPath(info=info, baseDir=selection,
                                prefix=prefix, suffix=suffix, isParent=False)

        if isParent:
            Log.log(f"Selected path: {selection}", Log.info)

        return selection

    except IndexError:
        raise InvalidInput(
            f"Can't select the file {
                selectedIndex + 1}/{len(listdir)}"
        )
        return None

    except ValueError:

        Log.log(
            "Error, please select a valid integer number, please try again",
            Log.error
        )
        return askPath(info, baseDir, prefix, suffix)

    except Exception as e:
        Log.log(f"Error: {e}", Log.error)
        return None


if __name__ == "__main__":
    askPath("This is a test", prefix="AllSubjects", suffix=".xlsx")
