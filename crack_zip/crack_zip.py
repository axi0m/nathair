# author: axi0m
# purpose: rudimentary zip cracker

import argparse
import pyzipper
import zipfile
import sys
import os
import logging
from rich.console import Console
from rich.progress import track

# Init console
console = Console()

# init logging
logging.basicConfig(level="INFO")

parser = argparse.ArgumentParser()
parser.add_argument(
    "--file", nargs="?", action="store", dest="file", help="The zip file to crack."
)
parser.add_argument(
    "--pwdfile",
    nargs="?",
    action="store",
    dest="pwdfile",
    help="The reference password file.",
)

# Parse our arguments provided at CLI
args = parser.parse_args()

# Verify the variables were provided or console.print help
if not args.file:
    parser.print_help()
    sys.exit(1)

if not args.pwdfile:
    parser.print_help()
    sys.exit(1)

# Set to cleaner variable names for ease later on
zfile = args.file
pfile = args.pwdfile


def test_pyzipper():
    """ Test if pyzipper is installed """

    if "pyzipper" not in sys.modules:
        logging.info(f"Module pyzipper is not installed")
        return False
    elif "pyzipper" in sys.modules:
        logging.info(f"Module pyzipper installed")
        return True


def test_zipfile(zfile):
    """ Test if file is legit Zip file or not """

    result = zipfile.is_zipfile(zfile)
    return result


def test_read(file):
    """ Test that file path provided exists and we have read permissions """

    if os.access(file, os.R_OK):
        return True


def test_exists(file):
    """ Test that file exists """
    if os.path.exists(file):
        return True


def extract_file(zfile, password):
    """ Extract Zip archive given particular password """

    try:
        zfile.extractall(pwd=password.encode("utf-8"))
        console.print(f"[+] Password found: [blue]{password}[/blue]", style="bold green")
        return (True, password)

    except RuntimeError as runerr:
        console.print(f"[-] Encountered a runtime error: {runerr}", style="bold red")
        return (False, runerr)

    except Exception as err:
        console.print(f"[-] Encountered generic exception: {err}", style="bold red")
        return (False, err)


def main():
    """ Main function """

    # Check if pyzipper support is present
    result_pyzipper = test_pyzipper()

    if result_pyzipper:
        console.print(
            f"[+] You have pyzipper installed, AES encrypted Zip support enabled!", style="bold green"
        )
    if not result_pyzipper:
        console.print(
            f"[!] You have not imported the pyzipper module, AES encryption for Zip archives not enabled", style="bold yellow"
        )

    # Check if file is a Zip file by magic number
    result_zip = test_zipfile(zfile)

    if result_zip:
        console.print(f"[+] File [blue]{zfile}[/blue] is a valid Zip archive", style="bold green")
    if not result_zip:
        console.print(f"[!] File [green]{zfile}[/green] is not a valid Zip archive, exiting...", style="bold red")
        sys.exit(1)

    # Check if file exists
    result_exists = test_exists(zfile)

    if result_exists:
        console.print(f"[+] File [blue]{zfile}[/blue] exists", style="bold green")
    if not result_exists:
        console.print(f"[!] File [green]{zfile}[/green] doesn't exist", style="bold red")
        sys.exit(1)

    # Check if file can be read
    result_read = test_read(zfile)

    if result_read:
        console.print(f"[+] File [blue]{zfile}[/blue] is readable", style="bold green")
    if not result_read:
        console.print(f"[!] File [green]{zfile}[/green] cannot be read", style="bold red")
        sys.exit(1)

    console.print(
        f"[-] Begin extraction subroutine for archive [white]{zfile}[/white] with provided password file: [white]{pfile}[/white]", style="bold yellow"
    )

    if result_pyzipper:
        with pyzipper.AESZipFile(zfile) as archive:
            with open(pfile, "r") as dictFile:
                for word in dictFile:

                    password = word.strip("\n")
                    extraction_result = extract_file(archive, password)

                    if extraction_result[0]:
                        console.print(
                            f"[*] Successfully extracted password-protected Zip archive: [blue]{zfile}[/blue]", style="bold green"
                        )
                        break

                    elif not extraction_result[0]:
                        continue

    else:
        with zipfile.ZipFile(zfile) as archive:
            with open(pfile, "r") as dictFile:
                for word in dictFile:

                    password = word.strip("\n")
                    extraction_result = extract_file(archive, password)

                    if extraction_result[0]:
                        console.print(
                            f"[*] Successfully extracted password-protected Zip archive: [blue]{zfile}[/blue]", style="bold green"
                        )
                        break

                    elif not extraction_result[0]:
                        console.print(
                            f"[!] Failed to extract password-protected Zip archive: {zfile}", style="bold red"
                        )

                    if "compress_type=99" in repr(extraction_result[1]):
                        console.print(
                            f"[!] Fatal error archive {zfile} is AES encrypted and AES encryption support is not present!", style="bold red"
                        )
                        sys.exit(1)
                    continue


if __name__ == "__main__":
    main()
