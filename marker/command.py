from . import ansi
import json
# import traceback
class CmdException(Exception):
    pass


def load(filePath, serialize_json=False):
    cmds = []
    try:
        with open(filePath, 'r') as f:
            cmds = [Command.deserialize(l) for l in f.readlines() if l]
    except Exception as e:
        raise Exception('Failed loading ' + filePath)
    return cmds

def save(commands, filePath):
    with open(filePath, 'w') as f:
        f.write('\n'.join([m.serialize() for m in commands]))

def add(commands, command):
    remove(commands, command)
    commands.append(command)

def remove(commands, command):
    try:
        match = next(m for m in commands if command == m)
        commands.remove(match)
    except StopIteration:
        pass

class Command(object):
    '''A Command is composed of the shell command string + optionnal alias + desp'''
    def __init__(self, cmd, alias, description='', json_serialize=False):
        if not cmd:
            raise CmdException("empty command argument")
        self.cmd = cmd
        self.alias = alias
        self.description = description
        self.json_serialize = json_serialize

    def __repr__(self):
        cmd_text = []
        cmd_text.append('cmd: ' + self.cmd)
        if self.alias:
            cmd_text.append('alias: ' + self.alias)
        if self.description:
            cmd_text.append('desp: ' + self.description)
        return ''.join(cmd_text)

    @staticmethod
    def deserialize(s):
        try:
            fields = json.loads(s)
            return Command(
                fields.get('command'),
                fields.get('alias'),
                fields.get('description'),
                json_serialize=True
            )
        except:
            s = s.strip('\n').strip('\r')
            if "##" in s:
                cmd, alias = s.split("##")
            else:
                cmd = s
                alias = ""
            return Command(cmd, alias)

    def serialize(self):
        if self.json_serialize:
            return json.dumps(
                {'command': self.cmd,
                 'alias': self.alias,
                 'description': self.description
                 }
            )
        if self.alias:
            return self.cmd + "##" + self.alias
        else:
            return self.cmd

    def __eq__(self, mark):
        return self.cmd == mark.cmd and self.alias == mark.alias \
               and self.description == mark.description

