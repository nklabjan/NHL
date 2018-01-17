############################################################
#
# File Name:    main.py
#
# Author:       Nick Klabjan
#
# Description:  Creates an NHL object which allows to make
#               directories and ultimately runs the program.
#
############################################################

import nhl_etl as ne


def main():
    nhl = ne.NHL()  # creates NHL object
    nhl.makedir()  # creates directories for each NHL season
    nhl.transferfiles()  # downloads files from the NHL server


if __name__ == "__main__":
    main()
