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

"""A Registry, storing Fudge FieldTypes."""

from fudge import codecs
from fudge import types
from fudge import utils

class UnknownTypeError(Exception):
    """An Unknown Type has been used

    TODO(jamesc)-We should be able to handle Unknown types
    in the registry."""
    pass


class FieldType(object):
    """The descriptor for a Fudge Field type.

    TODO(jamesc)- proper objects rather than this dispatch style?
    """
    def __init__(self, type_id, class_, is_variable_sized, fixed_size,
                 encoder=None, decoder=None, calc_size=None):
        """Create a new Field type.

        Arguments:
        type_id : the Fudge Type Identifier
        class : The python class this maps to
        is_variable_sized:
        fixed_size : the fixed size of the type

        encoder : Convert from object to bytes
            def encoder(obj) -> bytes
        decoder : Convert from bytes to object
            def decoder(bytes) -> object, bytes_read

        calc_size : if is_variable_sized is True, calculate the size needed
                to hold this object
            def size(object) -> num_bytes
        """
        self.type_id = type_id
        if class_:
            if isinstance(class_, str):
                self.classname = class_
            else:
                self.classname = class_.__name__
        else:
            self.classname = None
        self.is_variable_sized = is_variable_sized
        self.fixed_size = fixed_size
        self.encoder = encoder
        self.decoder = decoder
        self.calc_size = calc_size

        if self.is_variable_sized:
            assert self.calc_size

    def name(self):
        """Return the human friendly name of a Fudge Type.

        Return:
            The name of the type, if known, otherwise 'unknown(type_id)'
           """
        try:
            return types.FUDGE_TYPE_NAMES[self.type_id]
        except KeyError:
            return 'unknown(%s)'% self.type_id

    def __repr__(self):
        return "FieldType[id=%r, classname=%r]"% (self.type_id, self.classname)


def fullname(class_):
    """Return the full class name of a class."""
    if class_.__module__ == '__builtin__':
        return class_.__name__
    else:
        return '.'.join((class_.__module__, class_.__name__))

class Registry(object):
    """A Fudge Type registry.

    """
    def __init__(self):
        self.types_by_id = {}
        self.types_by_class = {}

        self._add(FieldType(types.INDICATOR_TYPE_ID, 'fudge.types.Indicator', \
                False, 0, \
                codecs.enc_indicator, codecs.dec_indicator, lambda x : 0))

        self._add(FieldType(types.BOOLEAN_TYPE_ID, bool, False, 1, \
                codecs.enc_bool, codecs.dec_bool))
        self._add(FieldType(types.BYTE_TYPE_ID, int, False, 1, \
                codecs.enc_byte, codecs.dec_byte))
        self._add(FieldType(types.SHORT_TYPE_ID, int, False, 2, \
                codecs.enc_short, codecs.dec_short))
        self._add(FieldType(types.INT_TYPE_ID, 'int', False, 4, \
                codecs.enc_int, codecs.dec_int))
        self._add(FieldType(types.LONG_TYPE_ID, long, False, 8, \
                codecs.enc_long, codecs.dec_long))

        self._add(FieldType(types.BYTEARRAY_TYPE_ID, str, True, 0, \
                codecs.enc_str, codecs.dec_str, types.size_str))
        self._add(FieldType(types.SHORTARRAY_TYPE_ID, None, True, 0, \
                lambda x : codecs.enc_array(codecs.enc_short, x), \
                lambda x : codecs.dec_array(codecs.dec_short, 2, x), \
                lambda x : 2 * len(x)))
        self._add(FieldType(types.INTARRAY_TYPE_ID, None, True, 0, \
                lambda x : codecs.enc_array(codecs.enc_int, x), \
                lambda x : codecs.dec_array(codecs.dec_int, 4, x), \
                lambda x : 4 * len(x)))
        self._add(FieldType(types.LONGARRAY_TYPE_ID, None, True, 0, \
                lambda x : codecs.enc_array(codecs.enc_long, x), \
                lambda x : codecs.dec_array(codecs.dec_long, 8, x), \
                lambda x : 8 * len(x)))

        self._add(FieldType(types.FLOAT_TYPE_ID, float, False, 4, \
                codecs.enc_float, codecs.dec_float))
        self._add(FieldType(types.DOUBLE_TYPE_ID, None, False, 8, \
                codecs.enc_double, codecs.dec_double))
        self._add(FieldType(types.FLOATARRAY_TYPE_ID, None, True, 0, \
                lambda x : codecs.enc_array(codecs.enc_float, x), \
                lambda x : codecs.dec_array(codecs.dec_float, 4, x), \
                lambda x : 4 * len(x)))
        self._add(FieldType(types.DOUBLEARRAY_TYPE_ID, None, True, 0, \
                lambda x : codecs.enc_array(codecs.enc_double, x), \
                lambda x : codecs.dec_array(codecs.dec_double, 8, x), \
                lambda x : 8 * len(x)))

        self._add(FieldType(types.STRING_TYPE_ID, unicode, True, 0, \
                codecs.enc_unicode, codecs.dec_unicode, types.size_unicode))

        # For FUDGEMSG, we shortcut the call to enc, dec
        self._add(FieldType(types.FUDGEMSG_TYPE_ID, \
                'fudge.message.Message', True,  0, \
                None, None, \
                calc_size = lambda x, taxonomy : x.size(taxonomy=taxonomy)))

        self._add(FieldType(types.BYTEARRAY4_TYPE_ID, str, False, 4, \
                codecs.enc_str, codecs.dec_str))
        self._add(FieldType(types.BYTEARRAY8_TYPE_ID, str, False, 8, \
                codecs.enc_str, codecs.dec_str))
        self._add(FieldType(types.BYTEARRAY16_TYPE_ID, str, False, 16, \
                codecs.enc_str, codecs.dec_str))
        self._add(FieldType(types.BYTEARRAY20_TYPE_ID, str, False, 20, \
                codecs.enc_str, codecs.dec_str))
        self._add(FieldType(types.BYTEARRAY32_TYPE_ID, str, False, 32, \
                codecs.enc_str, codecs.dec_str))
        self._add(FieldType(types.BYTEARRAY64_TYPE_ID, str, False, 64, \
                codecs.enc_str, codecs.dec_str))
        self._add(FieldType(types.BYTEARRAY128_TYPE_ID, str, False, 128, \
                codecs.enc_str, codecs.dec_str))
        self._add(FieldType(types.BYTEARRAY256_TYPE_ID, str, False, 256, \
                codecs.enc_str, codecs.dec_str))
        self._add(FieldType(types.BYTEARRAY512_TYPE_ID, str, False, 512, \
                codecs.enc_str, codecs.dec_str))


        self._narrower_fns = {
            types.BYTE_TYPE_ID: self._narrow_int,
            types.SHORT_TYPE_ID: self._narrow_int,
            types.INT_TYPE_ID: self._narrow_int,
            types.LONG_TYPE_ID: self._narrow_int,

            types.BYTEARRAY_TYPE_ID: self._narrow_str,
            types.BYTEARRAY4_TYPE_ID: self._narrow_str,
            types.BYTEARRAY8_TYPE_ID: self._narrow_str,
            types.BYTEARRAY16_TYPE_ID: self._narrow_str,
            types.BYTEARRAY20_TYPE_ID: self._narrow_str,
            types.BYTEARRAY32_TYPE_ID: self._narrow_str,
            types.BYTEARRAY64_TYPE_ID: self._narrow_str,
            types.BYTEARRAY128_TYPE_ID: self._narrow_str,
            types.BYTEARRAY256_TYPE_ID: self._narrow_str,
            types.BYTEARRAY512_TYPE_ID: self._narrow_str,

        }

    def __getitem__(self, key):
        return self.types_by_id[key]

    def _add(self, field_type):
        self.types_by_id[field_type.type_id] = field_type
        if field_type.classname:
            self.types_by_class[field_type.classname] = field_type

    def type_by_id(self, type_id):
        """Given a type_id return the Fudge FieldType which
        it represents.

        Arguments:
           type_id: the Fudge Type ID

        Return:
          The FieldType object for the Type Id

        Raise:
          UnknownTypeError: if we can't find a suitable class in the registry"""
        try:
            return self.types_by_id[type_id]
        except KeyError:
            raise UnknownTypeError("Did not recognize ID : %s"%type_id)

    def type_by_class(self, value, classname=None):
        """Given a value and an optional class return the Fudge FieldType which
        can hold it.

        Arguments:
           value: the object to find a class for
           classname: The name of class we wish to map to. (default: None)

        Return:
          A FieldType which can hold the object

        Raise:
          UnknownTypeError if we can't find a suitable class in the registry"""
        if not classname:
            classname = fullname(value.__class__)
        try:

            return self.types_by_class[classname]
        except KeyError:
            raise UnknownTypeError("No type mapping for class : %s"%classname)

    def narrow(self, type_, value):
        """Narrow a type if the value can fit into a smaller type."""

        if type_.type_id not in self._narrower_fns:
            return type_
        return self._narrower_fns[type_.type_id](value)

    def _narrow_int(self, value):
        if value >= utils.MIN_BYTE and value <= utils.MAX_BYTE:
            return self[types.BYTE_TYPE_ID]
        elif value >= utils.MIN_SHORT and value <= utils.MAX_SHORT:
            return self[types.SHORT_TYPE_ID]
        elif value >= utils.MIN_INT and value <= utils.MAX_INT:
            return self[types.INT_TYPE_ID]
        else:
            return self[types.LONG_TYPE_ID]

    def _narrow_str(self, value):

        fixed_bytelen = {
                4: self[types.BYTEARRAY4_TYPE_ID],
                8: self[types.BYTEARRAY8_TYPE_ID],
                16: self[types.BYTEARRAY16_TYPE_ID],
                20: self[types.BYTEARRAY20_TYPE_ID],
                32: self[types.BYTEARRAY32_TYPE_ID],
                64: self[types.BYTEARRAY64_TYPE_ID],
                128: self[types.BYTEARRAY128_TYPE_ID],
                256: self[types.BYTEARRAY256_TYPE_ID],
                512: self[types.BYTEARRAY512_TYPE_ID],
            }
        array_len = len(value)
        if array_len in fixed_bytelen:
            return fixed_bytelen[array_len]
        return self[types.BYTEARRAY_TYPE_ID]

DEFAULT_REGISTRY = Registry()
