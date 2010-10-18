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

import sys

from  cStringIO import StringIO

from fudge import types

def max_len(fields):
    max_len = 0
    for field in fields:
        if len(field) > max_len:
            max_len = len(field)
    return max_len

class PrettyPrinter(object):
    """A PrettyPrinter for Fudge messages.

    Based on the Java FudgeMsgFormatter.

    """

    DEFAULT_INDENT = 2

    def __init__(self, writer = sys.stdout, indent = DEFAULT_INDENT):
        """Create a new PrettyPrinter

        Arguments:
            writer:  the writer stream to output to
            indent:  how much to indent a sub-message (Default:2)
        """
        self._writer = writer
        self._indent = indent

    def format(self, message, depth=0):
        """Output a formatted message to the underlying writer

        Arguments:
            message:  the message to write
            depth:  The depth of this message/sub-message (Default:0)

        """
        if not message.fields:
            return
        num_fields = len(message.fields)

        fieldspecs = []
        for field, index in zip(message.fields, range(num_fields)):
            fieldspec = self._get_fieldspec(field, index, depth)
            fieldspecs.append(fieldspec)

        max_fieldspec_width = max_len(fieldspecs)
        max_typename_width = max_len([types.name_for_type(x.type_.type_id) for x in  message.fields])

        for field, fieldspec, index in  zip(message.fields, fieldspecs, range(num_fields)) :
            self._format_field(field, fieldspec, index, depth, \
                    max_fieldspec_width, max_typename_width)

    def _format_field(self, field, fieldspec, index, depth, max_fs, max_tn):
        """Format a single field on a line"""
        typename = types.name_for_type(field.type_.type_id)
        #self._writer.write("{0:<{width}} {1:<{tn_width}} ".format(fieldspec, typename, width=max_fs, tn_width=max_tn) )
        self._writer.write("%-*s %-*s "%(max_fs, fieldspec, max_tn, typename) )
        if field.is_type(types.FUDGEMSG_TYPE_ID):
            self._writer.write('\n')
            self.format(field.value, depth + 1)
        else:
            self._write_typed_value(field.type_, field.value)
        self._writer.write('\n')
        self._writer.flush()

    def _get_fieldspec(self, field, index, depth):
        """Create a string representation of a Field specification header.

        Arguments:
            field : The field
            index : Index within the current message of this field
            depth : Depth of current message
        Return:
            Formatted string representation of the Field header

        """
        buf = StringIO()

        buf.write(' ' * self._indent * depth)
        buf.write(str(index))
        buf.write('-')
        if field.ordinal is not None:
            buf.write('(%s)'%field.ordinal)
            if field.name:
                buf.write(' ')
        if field.name:
            buf.write(field.name)
        return buf.getvalue()

    def _output_array(self, value, truncate=8):
        num_elements = len(value)
        if truncate > num_elements:
            truncate = num_elements
        self._writer.write('[')
        self._writer.write(', '.join(map(lambda x : str(x), value[:truncate])))
        if truncate < num_elements:
            self._writer.write(" ... %d more"%(num_elements - truncate))
        self._writer.write(']')

    def _write_typed_value(self, type_, value):
        renderers = {
            types.SHORTARRAY_TYPE_ID : self._output_array,
            types.FLOATARRAY_TYPE_ID : self._output_array,
            types.DOUBLEARRAY_TYPE_ID : self._output_array,
            types.INTARRAY_TYPE_ID : self._output_array,
            types.LONGARRAY_TYPE_ID : self._output_array,
            types.BYTEARRAY_TYPE_ID : self._output_array,
            types.BYTEARRAY4_TYPE_ID : self._output_array,
            types.BYTEARRAY8_TYPE_ID : self._output_array,
            types.BYTEARRAY16_TYPE_ID : self._output_array,
            types.BYTEARRAY20_TYPE_ID : self._output_array,
            types.BYTEARRAY32_TYPE_ID : self._output_array,
            types.BYTEARRAY64_TYPE_ID : self._output_array,
            types.BYTEARRAY128_TYPE_ID : self._output_array,
            types.BYTEARRAY256_TYPE_ID : self._output_array,
            types.BYTEARRAY512_TYPE_ID : self._output_array,

        }

        try :
            renderers[type_.type_id](value)
        except KeyError:
            self._writer.write(str(value))
