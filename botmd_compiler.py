from mistletoe import Document, HTMLRenderer
from mistletoe.span_token import SpanToken
from mistletoe.block_token import BlockToken, Heading, CodeFence, Paragraph, List
import re
import json
import html
from flask import render_template

# Stuff we"re not allowed to include directly in format strings
newline = "\n"
empty = ""
quote = "'"
bquote = "\\'"

# SECTION 1: EXTENDING THE MISTLETOE PARSER

# A tag structure to detect if gates at the beginnings of paragraphs
class ParaConditionalTag(SpanToken):
    pattern = re.compile(r"^\(If `(.+)`\)\s*")
    parse_inner = False
    precedence = 6
    def __init__(self, match):
        self.content = match.group(1)

# A custom render for BotMD's specific needs.
class BotMDRenderer(HTMLRenderer):
    def __init__(self):
        super().__init__(ParaConditionalTag)
    
    def render_para_conditional_tag(self, match):
        return ''

    def render_raw_text(self, token):
        return super().render_raw_text(token).replace(quote, bquote)

    def render_inline_code(self, token):
        return f"' + String({token.children[0].content.replace(quote, bquote)}) + '"

    def render_link(self, token):
        template = '<a href="{target}"{title} target="_blank">{inner}</a>'
        target = self.escape_url(token.target)
        if token.title:
            title = ' title="{}"'.format(html.escape(token.title))
        else:
            title = ''
        inner = self.render_inner(token)
        return template.format(target=target, title=title, inner=inner)

def render_block(renderer, token: BlockToken):
    if isinstance(token, CodeFence):
        return f"(function () {{ {token.children[0].content} \nnext();}})"
    elif isinstance(token, List) and token.start == None:
        try:
            return render_list(renderer, token)
        except Exception:
            pass
    elif isinstance(token, Paragraph) and isinstance(token.children[0], ParaConditionalTag):
        return f"(function () {{ if ({token.children[0].content}) {{ say('{renderer.render(token).replace(newline, empty)}'); }} else {{ next(); }} }})"
    return f"(function() {{ say('{renderer.render(token).replace(newline, empty)}') }})"

input_re = re.compile(r"Input (\w+) (\w+)(?: \((.+)\))?")
goto_re = re.compile(r"Go to (.+)")

def render_list(renderer, list):
    list_options = []
    for sublist in list.children:
        assert 1 <= len(sublist.children) <= 2 # A paragraph for containing the text to give and a list for containing the commands to run.
        if isinstance(sublist.children[0].children[0], ParaConditionalTag):
            filter = (sublist.children[0].children[0].content)
        else:
            filter = "true"
        text = renderer.render(sublist.children[0])
        if len(sublist.children) == 1:
            full_list_command = "(function () {})"
        else:
            commands = []
            assert isinstance(sublist.children[1], List)
            for command_listitem in sublist.children[1].children:
                if isinstance(command_listitem.children[0], CodeFence):
                    commands.append(f"(function() {{ {command_listitem.children[0].children[0].content} }})();")
                elif isinstance(command_listitem.children[0], Paragraph):
                    assert len(command_listitem.children[0].children) == 1
                    command_text = command_listitem.children[0].children[0].content
                    input_match = input_re.match(command_text)
                    goto_match = goto_re.match(command_text)
                    if input_match:
                        commands.append(f"input('{input_match.group(2)}', {{{input_match.group(3) if input_match.group(3) else ''}}}, (function (x) {{ {input_match.group(1)} = x; }}));")
                    elif goto_match:
                        commands.append(f"go_to('{goto_match.group(1)}');")
                    elif command_text == 'Exit':
                        commands.append(f"exit();")
                    else:
                        commands.append(f"go_to('{command_text}');")
                else:
                    raise Exception
            full_list_command = f"(function () {{ {newline.join(commands)} }})"
        if text == "<p>--</p>":
            text = ""
        list_options.append(f"{{\ntext: (function () {{ return '{text}' }}),\ncommand: {full_list_command},\nfilter: (function () {{return {filter};}})}}")
    return f"(function (){{ choose ([{','.join(list_options)}]) }})"


def compile_bot_md(path):
    with open(path, "r") as file, BotMDRenderer() as renderer:
        doc = Document(file)
        jumps = {}
        script = []
        len = 0
        for child in doc.children:
            if isinstance(child, Heading):
                jumps[child.children[0].content] = len
            else:
                script.append(render_block(renderer, child))
                len += 1
        full_script = f"[{','.join(script)}, exit]"
        full_jumps = json.dumps(jumps)
        return render_template("botmd.js", script=full_script, jumps=full_jumps)
