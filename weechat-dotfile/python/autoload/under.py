import sys
import weechat
import re

SCRIPT_NAME = "under"
SCRIPT_AUTHOR = "H"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC = ("Converts the text between :: to [every_day]\n"
               "\n"
               "ie, typing: /under TOKI WO TOMARE :every day:\n"
               "will output: TOKI WO TOMARE [every_day]")

PY3 = sys.version > '3'

if PY3:
    unichr = chr
    def send(buf, text):
        weechat.command(buf, "/input send {}".format(text))
else:
    def send(buf, text):
        weechat.command(buf, "/input send {}".format(text.encode("utf-8")))

def cb_under_cmd(data, buf, args):
    chars = []
    ind = [i for i, ltr in enumerate(args) if ltr == ":"]
    start = ind[0]
    end = ind[1]

    if not PY3:
        args = args.decode("utf-8")

    for i, char in enumerate(list(args)):
        if start < i < end:
            char = char.upper().replace(" ", "_")
        elif start == i:
            char = u'['
        elif end == i:
            char = u']'

        chars.append(char)

    send(buf, ''.join(chars))
    return weechat.WEECHAT_RC_OK

if __name__ == "__main__":
    weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION,
                     SCRIPT_LICENSE, SCRIPT_DESC, '', '')
    weechat.hook_command("under", SCRIPT_DESC, "<text :text:>", '', '',
                         "cb_under_cmd", '')
