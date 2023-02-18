# -*- coding: utf-8 -*-
#
# Converts the text between :: to fullwidth then adds 「 and 」.
# ie: 
# /stand TOKI WO TOMARE :THE WORLD:
# will output:
# TOKI WO TOMARE 「ＴＨＥ ＷＯＲＬＤ」
#
# This script is derived from fullwidth https://weechat.org/scripts/source/fullwidth.py/
# Original author: Germain Z. <germanosz@gmail.com>

import sys
import weechat

SCRIPT_NAME = "stand"
SCRIPT_AUTHOR = "Hairo"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC = ("Converts the text between :: to fullwidth then adds 「 and 」.\n"
               "\n"
               "ie, typing: /stand TOKI WO TOMARE :THE WORLD:\n"
               "will output: TOKI WO TOMARE 「ＴＨＥ ＷＯＲＬＤ」")

PY3 = sys.version > '3'

if PY3:
    unichr = chr
    def send(buf, text):
        weechat.command(buf, "/input send {}".format(text))
else:
    def send(buf, text):
        weechat.command(buf, "/input send {}".format(text.encode("utf-8")))

def cb_stand_cmd(data, buf, args):
    """Callback for ``/stand``, convert to fulwidth and uppercase then add 「 and 」."""
    
    chars = []
    ind = [i for i, ltr in enumerate(args) if ltr == ":"]
    start = ind[0]
    end = ind[1]
    
    if not PY3:
        args = args.decode("utf-8")

    for i, char in enumerate(list(args)):
        if start < i < end:
            char = char.upper()
            ord_char = ord(char)
            if ord_char >= 32 and ord_char <= 126:
                char = unichr(ord_char + 65248)
        elif start == i:
            char = u'「'
        elif end == i:
            char = u'」'
        
        chars.append(char)

    send(buf, ''.join(chars))
    return weechat.WEECHAT_RC_OK


if __name__ == "__main__":
    weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION,
                     SCRIPT_LICENSE, SCRIPT_DESC, '', '')
    weechat.hook_command("stand", SCRIPT_DESC, "<text :text:>", '', '',
                         "cb_stand_cmd", '')
