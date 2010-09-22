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

"""Methods for dealing with Fudge Field Prefixes:

<http://www.fudgemsg.org/display/FDG/Encoding+Specification#EncodingSpecification-FieldPrefix>
"""

def decode_prefix(byte):
    """Decode a byte according to the Field Prefix encoding
    scheme.

    Arguments:
        byte: the encoded representation of the prefix

    Return:
        fixedwidth: Is the field fixed width (bool)
        variablewidth: if not fixed width, the number of bytes
            needed to encode the value width (1, 2 or 4)
        has_ordinal: The field has an ordinal encoded  (bool)
        has_name: This field has a name encoded (bool)

    """
    fixedwidth = (byte & 0x80) != 0
    has_name = (byte & 0x08) != 0
    has_ordinal = (byte & 0x10) != 0
    variablewidth = (byte & 0x60) >>5
    if variablewidth == 3:
        variablewidth = 4
    return fixedwidth, variablewidth, has_ordinal, has_name

def encode_prefix(fixedwidth, variablewidth, has_ordinal, has_name):
    """Encode a Field Prefix byte according to the Field Prefix
    encoding scheme.

    Arguments:
        fixedwidth: Is the field fixed width (bool)
        variablewidth: if not fixed width, the number of bytes
            needed to encode the value width (1, 2 or 4)
        has_ordinal: The field has an ordinal encoded  (bool)
        has_name: This field has a name encoded (bool)

    Return:
        The Field Prefix (str of length 1)

    """
    byte = 0x00
    if fixedwidth:
        byte = byte | 0x80
    if has_name:
        byte = byte | 0x08
    if has_ordinal:
        byte = byte | 0x10
    if variablewidth > 0:
        if variablewidth == 4:
            varwidth = 3
        else:
            varwidth = variablewidth
        byte = byte | varwidth << 5
    return byte
