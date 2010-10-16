#
# Copyright CERN, 2010.
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#
"""
A Printer which outputs a hexdump version of a Fudge Message
"""

import sys


def ascii(val):
    if 32 <= val <= 126:
        return chr(val)
    else:
        return '.'

ASC_MAP = [ ascii(x) for x in range(256) ]

class HexPrinter(object):
    """Print a Fudge Message as a byte array.

    This basically isn't aware of any Fudge Structure, just
    does a hexdump"""

    def __init__(self, writer=sys.stdout, width=16):
        """Create a new HexPrinter

        Arguments:
            writer:  the writer stream to output to
            width:  how many bytes per line (Default:16)
        """
        self._writer = writer
        self._width = width

    def format(self, message):
        """Output a formatted message to the underlying writer

         Arguments:
             message: the message to write
        """

        hexwidth = 3 * self._width + 1
        start = 0
        while start < len(message):
            end = start + self._width
            if end > len(message):
                end = len(message)

            line = message[start:end]
            hex_line = [ "%02x" % ord(val)+' ' for val in line]
            # Add middle space
            hex_line.insert(self._width/2, ' ')
            asc_line = [ ASC_MAP[ord(val)] for val in line]
            self._writer.write("%08x  %-*s |%s|\n" %
                 (start, hexwidth, ''.join(hex_line), ''.join(asc_line)))
            start += self._width
        self._writer.write("%08x\n" % len(message))