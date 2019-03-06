#! /usr/bin/python

import re

def isValid(value, type, length, format, precision, signed, defaultvalue):

        # check for default value
        if (value == defaultvalue): return 0

        # check for integer
        if (type == "int"):
                int_regexp=re.compile('^[0-9]+$')
                if not int_regexp.match(value): return 1

        # check for decimal
        if (type == "decimal"):
                n_length = "%d" % (length-precision)
                reg_exp="^[0-9]{%s}.[0-9]{%s}$" % (n_length, precision)
                decimal_regexp=re.compile(reg_exp)
                if not decimal_regexp.match(value): return 1

        # check for date
        if (type == "date"):
                int_regexp=re.compile('^[0-9]{8}$')
                if not int_regexp.match(value): return 1
                y = int(value[0:4])
                m = int(value[4:6])
                d = int(value[6:8])
                if ( m < 1 or m > 12 ): return 1
                if ( d < 1 or d > 31 ): return 1
                if ( d > 30 and ( m == 4 or m == 6 or m == 9 or m == 11 ) ): return 1
                if ( m == 2 ):
                        if ( y % 400 == 0 ):
                                LEAP_YEAR = 1
                        elif ( y % 100 == 0 ):
                                LEAP_YEAR = 0
                        elif ( y % 4   == 0 ):
                                LEAP_YEAR = 1
                        else:
                                LEAP_YEAR = 0
                        if (  LEAP_YEAR and d > 29 ): return 1

        return 0


#-EOF