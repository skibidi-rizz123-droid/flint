# Rename process to "Flint" before Tkinter/NSApplication initializes —
# this is what makes macOS show "Flint" in the menu bar instead of "Python".
try:
    import ctypes, ctypes.util
    ctypes.CDLL(ctypes.util.find_library('c')).setprogname(b'Flint')
except Exception:
    pass
try:
    from Foundation import NSBundle
    _info = NSBundle.mainBundle().infoDictionary()
    _info['CFBundleName']        = 'Flint'
    _info['CFBundleDisplayName'] = 'Flint'
except Exception:
    pass

import builtins
import math
import random
import time
import inspect
import urllib.request
import os
import sys


def _projects_dir():
    """Default folder for Open / Save — ~/Documents/flint (created if missing)."""
    d = os.path.join(os.path.expanduser("~"), "Documents", "flint")
    os.makedirs(d, exist_ok=True)
    return d


# ── Auto-updater ──────────────────────────────
# Set this to your GitHub repo once you create it.
# Format:  "your-github-username/flint"
GITHUB_REPO = ""          # e.g. "henrymarcais/flint"
VERSION     = "0.1.2"

def _check_update():
    if not GITHUB_REPO:
        return
    try:
        url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/lang.py"
        with urllib.request.urlopen(url, timeout=3) as r:
            latest = r.read().decode()
        for line in latest.splitlines():
            if line.startswith("VERSION"):
                latest_ver = line.split('"')[1]
                if latest_ver != VERSION:
                    builtins.print(f"  Updating Flint {VERSION} → {latest_ver}...")
                    with open(__file__, 'w') as f:
                        f.write(latest)
                    builtins.print("  Updated! Restarting...\n")
                    os.execv(sys.executable, [sys.executable] + sys.argv)
                break
    except Exception:
        pass   # no internet or repo not set up yet — just continue
import tkinter as tk
import tkinter.font as tkfont
import tkinter.simpledialog as tkdialog
import tkinter.messagebox as tkmessagebox
import bext

# ─────────────────────────────────────
#  FUNCTION REGISTRY
#  Use @lang_function(color='...') on
#  each def. Color shows live as you type.
# ─────────────────────────────────────

FUNCTIONS = {}
VARIABLES = {}

def lang_function(color='white'):
    """Decorator — registers a function and gives it a highlight color."""
    def decorator(fn):
        fn._lang_color = color
        FUNCTIONS[fn.__name__] = fn
        return fn
    return decorator


# set is a built-in — always available, no need to define it yourself
FUNCTIONS['set'] = lambda name, value: VARIABLES.update({name: value})
FUNCTIONS['set']._lang_color = 'yellow'
FUNCTIONS['int'] = lambda a: builtins.int(a)
FUNCTIONS['int']._lang_color = 'cyan'
FUNCTIONS['float'] = lambda a: builtins.float(a)
FUNCTIONS['float']._lang_color = 'cyan'
FUNCTIONS['str'] = lambda a: builtins.str(a)
FUNCTIONS['str']._lang_color = 'cyan'
FUNCTIONS['sleep'] = lambda a: time.sleep(a)
FUNCTIONS['sleep']._lang_color = 'cyan'

# ─────────────────────────────────────
#  YOUR FUNCTIONS
#  Set color= to any of:
#  'red' 'green' 'blue' 'yellow'
#  'cyan' 'magenta' 'orange' 'white'
# ─────────────────────────────────────

@lang_function(color='red')
def add(a, b):
    return a + b

@lang_function(color='red')
def sub(a, b):
    return a - b

@lang_function(color='red')
def mul(a, b):
    return a * b

@lang_function(color='red')
def div(a, b):
    return a / b

@lang_function(color='red')
def mod(a, b):
    return a % b

@lang_function(color='red')
def pow(a, b):
    return a ** b

@lang_function(color='red')
def sqrt(a):
    return math.sqrt(a)

@lang_function(color='red')
def sin(a):
    return math.sin(a)

@lang_function(color='red')
def cos(a):
    return math.cos(a)

@lang_function(color='red')
def tan(a):
    return math.tan(a)

@lang_function(color='red')
def asin(a):
    return math.asin(a)

@lang_function(color='red')
def acos(a):
    return math.acos(a)

@lang_function(color='red')
def atan(a):
    return math.atan(a)

@lang_function(color='red')
def atan2(a, b):
    return math.atan2(a, b)

@lang_function(color='red')
def abs(a):
    return abs(a)

@lang_function(color='red')
def ceil(a):
    return math.ceil(a)

@lang_function(color='red')
def floor(a):
    return math.floor(a)

@lang_function(color='red')
def round(a):
    return builtins.round(a)

@lang_function(color='blue')
def say(*args):
    builtins.print(*args, sep='')

@lang_function(color='blue')
def ask(a):
    return builtins.input(a)

@lang_function(color='red')
def randint(a, b):
    return random.randint(a, b)

@lang_function(color='red')
def randfloat(a, b):
    return random.uniform(a, b)

@lang_function(color='red')
def random_binary(a):
    return random.choice([0, 1])

@lang_function(color='red')
def random_choice(a):
    return random.choice(a)

@lang_function(color='red')
def random_shuffle(a):
    random.shuffle(a)
    return a

@lang_function(color='cyan')
def is_even(a):
    return a % 2 == 0

@lang_function(color='cyan')
def is_odd(a):
    return a % 2 != 0

@lang_function(color='cyan')
def is_prime(a):
    if a <= 1:
        return False
    for i in range(2, a):
        if a % i == 0:
            return False
    return True

@lang_function(color='cyan')
def is_positive(a):
    return a > 0

@lang_function(color='cyan')
def is_negative(a):
    return a < 0

@lang_function(color='cyan')
def draw_txt_line(text, color, x):
    bext.fg(color)
    builtins.print(text * x)
    bext.fg('reset')

@lang_function(color='red')
def pi():
    return math.pi

@lang_function(color='red')
def e():
    return math.e

@lang_function(color='red')
def phi():
    return (1 + math.sqrt(5)) / 2
# ─────────────────────────────────────
#  INFRASTRUCTURE  (don't touch below)
# ─────────────────────────────────────

COLOR_MAP = {
    'red':     '#ff4444',
    'green':   '#44ff44',
    'blue':    '#4488ff',
    'yellow':  '#ffff44',
    'cyan':    '#44ffff',
    'magenta': '#ff44ff',
    'orange':  '#ff8800',
    'white':   '#e6edf3',
}

# ── GUI output routing ─────────────────────────────────────────────────────
# When the Tkinter app is running, _GUI_APP points to it and all
# output/errors are routed there instead of the terminal.

_GUI_APP = None

def _emit(msg, kind='normal'):
    if _GUI_APP:
        _GUI_APP.write_output(msg, kind)
    else:
        if kind == 'error':
            builtins.print(f"\033[31m{msg}\033[0m")
        else:
            builtins.print(msg)

def _tokenize(text):
    tokens = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch.isspace():
            i += 1
        elif ch.isdigit():
            j = i
            while j < len(text) and (text[j].isdigit() or text[j] == '.'):
                j += 1
            s = text[i:j]
            tokens.append(('NUM', float(s) if '.' in s else int(s)))
            i = j
        elif ch.isalpha() or ch == '_':
            j = i
            while j < len(text) and (text[j].isalnum() or text[j] == '_'):
                j += 1
            tokens.append(('IDENT', text[i:j]))
            i = j
        elif ch == '"':
            j = i + 1
            while j < len(text) and text[j] != '"':
                j += 1
            tokens.append(('STR', text[i+1:j]))
            i = j + 1
        elif ch == '=':
            if i+1 < len(text) and text[i+1] == '=':
                tokens.append(('CMP', '==')); i += 2
            else:
                tokens.append(('ASSIGN', '=')); i += 1
        elif ch == '!' and i+1 < len(text) and text[i+1] == '=':
            tokens.append(('CMP', '!=')); i += 2
        elif ch == '<':
            if i+1 < len(text) and text[i+1] == '=':
                tokens.append(('CMP', '<=')); i += 2
            else:
                tokens.append(('CMP', '<')); i += 1
        elif ch == '>':
            if i+1 < len(text) and text[i+1] == '=':
                tokens.append(('CMP', '>=')); i += 2
            else:
                tokens.append(('CMP', '>')); i += 1
        elif ch == '&' and i+1 < len(text) and text[i+1] == '&':
            tokens.append(('LGOP', '&&')); i += 2
        elif ch == '|' and i+1 < len(text) and text[i+1] == '|':
            tokens.append(('LGOP', '||')); i += 2
        elif ch == '!' :
            tokens.append(('LGOP', '!')); i += 1
        elif ch == '*' and i+1 < len(text) and text[i+1] == '*':
            tokens.append(('OP', '**'))
            i += 2
        elif ch in '+-*/%':
            tokens.append(('OP', ch))
            i += 1
        elif ch == '(':
            tokens.append(('LPAREN', '(')); i += 1
        elif ch == ')':
            tokens.append(('RPAREN', ')')); i += 1
        elif ch == ',':
            tokens.append(('COMMA', ',')); i += 1
        else:
            raise SyntaxError(f"Unknown character: {ch!r}")
    tokens.append(('EOF', None))
    return tokens

# operator precedence and associativity  (higher number = tighter binding)
_OP_PREC = {
    '||': (0, 'L'),
    '&&': (1, 'L'),
    '==': (2, 'L'), '!=': (2, 'L'),
    '<':  (3, 'L'), '>':  (3, 'L'), '<=': (3, 'L'), '>=': (3, 'L'),
    '+':  (4, 'L'), '-':  (4, 'L'),
    '*':  (5, 'L'), '/':  (5, 'L'), '%':  (5, 'L'),
    '**': (6, 'R'),
}

def _shunting_yard(tokens):
    """Convert infix token list to RPN using the Shunting-Yard algorithm."""
    output     = []
    ops        = []
    arg_counts = []          # arg count for each open function call
    set_flags  = []          # True if open function's first arg should be raw varname
    prev_type  = None

    for i, (tok_type, tok_val) in enumerate(tokens):
        if tok_type == 'EOF':
            break

        if tok_type in ('NUM', 'STR'):
            output.append((tok_type, tok_val))

        elif tok_type == 'IDENT':
            next_type = tokens[i+1][0] if i+1 < len(tokens) else 'EOF'
            if next_type == 'LPAREN':
                ops.append(('FN', tok_val))
            else:
                # raw varname if first arg of 'set'
                if set_flags and set_flags[-1]:
                    output.append(('VARNAME', tok_val))
                    set_flags[-1] = False
                else:
                    output.append(('IDENT', tok_val))

        elif tok_type == 'LPAREN':
            if ops and ops[-1][0] == 'FN':
                fn_name = ops[-1][1]
                next_type = tokens[i+1][0] if i+1 < len(tokens) else 'EOF'
                arg_counts.append(0 if next_type == 'RPAREN' else 1)
                set_flags.append(fn_name == 'set')
            ops.append(('LPAREN', '('))

        elif tok_type == 'RPAREN':
            while ops and ops[-1][0] != 'LPAREN':
                output.append(ops.pop())
            if not ops:
                raise SyntaxError("missing '('")
            ops.pop()  # discard LPAREN
            if ops and ops[-1][0] == 'FN':
                fn_tok = ops.pop()
                n = arg_counts.pop()
                set_flags.pop()
                output.append(('CALL', fn_tok[1], n))

        elif tok_type == 'COMMA':
            while ops and ops[-1][0] != 'LPAREN':
                output.append(ops.pop())
            if arg_counts:
                arg_counts[-1] += 1
            if set_flags:
                set_flags[-1] = False   # subsequent args are not raw varnames

        elif tok_type in ('OP', 'CMP', 'LGOP'):
            op = tok_val
            if op == '-' and prev_type in (None, 'OP', 'CMP', 'LGOP', 'LPAREN', 'COMMA'):
                ops.append(('UNARY', '-'))
            elif op == '!' and prev_type in (None, 'OP', 'CMP', 'LGOP', 'LPAREN', 'COMMA'):
                ops.append(('UNARY', '!'))
            else:
                prec, assoc = _OP_PREC[op]
                while ops and ops[-1][0] in ('OP', 'CMP', 'LGOP', 'UNARY'):
                    top = ops[-1]
                    top_prec = 7 if top[0] == 'UNARY' else _OP_PREC[top[1]][0]
                    if (assoc == 'L' and prec <= top_prec) or \
                       (assoc == 'R' and prec < top_prec):
                        output.append(ops.pop())
                    else:
                        break
                ops.append((tok_type, op))

        prev_type = tok_type

    while ops:
        tok = ops.pop()
        if tok[0] == 'LPAREN':
            raise SyntaxError("missing ')'")
        output.append(tok)

    return output

def _eval_rpn(rpn):
    """Evaluate an RPN token list and return the result."""
    stack = []
    for tok in rpn:
        t = tok[0]
        if t == 'NUM':
            stack.append(tok[1])
        elif t == 'STR':
            stack.append(tok[1])
        elif t == 'VARNAME':
            stack.append(tok[1])   # raw string — used by set()
        elif t == 'IDENT':
            name = tok[1]
            if name in VARIABLES:
                stack.append(VARIABLES[name])
            else:
                raise NameError(f"Unknown variable '{name}'")
        elif t == 'OP':
            if len(stack) < 2:
                raise SyntaxError("not enough operands")
            b, a = stack.pop(), stack.pop()
            match tok[1]:
                case '+':  stack.append(a + b)
                case '-':  stack.append(a - b)
                case '*':  stack.append(a * b)
                case '/':
                    if b == 0: raise ZeroDivisionError("division by zero")
                    stack.append(a / b)
                case '%':  stack.append(a % b)
                case '**': stack.append(a ** b)
        elif t == 'CMP':
            b, a = stack.pop(), stack.pop()
            match tok[1]:
                case '==': stack.append(a == b)
                case '!=': stack.append(a != b)
                case '<':  stack.append(a < b)
                case '>':  stack.append(a > b)
                case '<=': stack.append(a <= b)
                case '>=': stack.append(a >= b)
        elif t == 'LGOP':
            b, a = stack.pop(), stack.pop()
            match tok[1]:
                case '&&': stack.append(bool(a) and bool(b))
                case '||': stack.append(bool(a) or bool(b))
        elif t == 'UNARY':
            v = stack.pop()
            stack.append(not v if tok[1] == '!' else -v)
        elif t == 'CALL':
            _, name, n_args = tok
            args = stack[-n_args:] if n_args > 0 else []
            if n_args > 0:
                stack = stack[:-n_args]
            if name not in FUNCTIONS:
                raise NameError(f"Unknown function '{name}'")
            result = FUNCTIONS[name](*args)
            stack.append(result)

    return stack[0] if stack else None


def _err(msg, line_num):
    _emit(f"  error on line {line_num}: {msg}", 'error')

def _run_line(line, line_num):
    line = line.strip()
    if not line or line.startswith('#'):
        return
    try:
        tokens = _tokenize(line)
        if len(tokens) >= 3 and tokens[0][0] == 'IDENT' and tokens[1][0] == 'ASSIGN':
            var_name = tokens[0][1]
            rpn    = _shunting_yard(tokens[2:])
            result = _eval_rpn(rpn)
            VARIABLES[var_name] = result
        else:
            rpn    = _shunting_yard(tokens)
            result = _eval_rpn(rpn)
            if result is not None:
                _emit(f"= {result}", 'result')
    except SyntaxError as e:
        msg = str(e)
        if 'None' in msg or 'EOF' in msg.upper():
            _err("missing ')'", line_num)
        else:
            _err(f"syntax error — {msg}", line_num)
    except NameError as e:
        msg = str(e)
        if 'Unknown function' in msg:
            name = msg.split("'")[1]
            _err(f"'{name}' is not a function", line_num)
        elif 'Unknown variable' in msg:
            name = msg.split("'")[1]
            _err(f"'{name}' has no value — use  {name} = ...  first", line_num)
        else:
            _err(msg, line_num)
    except Exception as e:
        _err(str(e), line_num)

def _hex_lighten(hex_color, amount=30):
    """Brighten a hex color by `amount` for hover effects."""
    hex_color = hex_color.lstrip('#')
    r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    r = min(255, r + amount)
    g = min(255, g + amount)
    b = min(255, b + amount)
    return f'#{r:02x}{g:02x}{b:02x}'


# NSMenu "About" calls orderFrontStandardAboutPanel: — must replace target/action in Cocoa.
_flint_about_bridge_cls = None


def _flint_about_bridge_class():
    global _flint_about_bridge_cls
    if _flint_about_bridge_cls is False:
        return None
    if _flint_about_bridge_cls is not None:
        return _flint_about_bridge_cls
    if sys.platform != 'darwin':
        _flint_about_bridge_cls = False
        return None
    try:
        import objc
        from Foundation import NSObject
    except ImportError:
        _flint_about_bridge_cls = False
        return None

    class FlintAboutBridge(NSObject):
        def initWithFlint_(self, flint):
            self = objc.super(FlintAboutBridge, self).init()
            if self is None:
                return None
            self._flint = flint
            return self

        def showFlintAbout_(self, sender):
            fa = self._flint
            if fa is not None:
                fa.root.after(0, fa._mac_about_flint)

    _flint_about_bridge_cls = FlintAboutBridge
    return FlintAboutBridge


class FlintApp:
    BG      = "#0d1117"
    BG2     = "#161b22"
    BG3     = "#1c2128"
    FG      = "#e6edf3"
    FG_DIM  = "#8b949e"
    BORDER  = "#30363d"
    CURSOR  = "#58a6ff"

    # Pixel-art glyphs for F L I N T  (5 wide × 7 tall)
    _GLYPHS = {
        'F': [[1,1,1,1,1],[1,0,0,0,0],[1,1,1,1,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0]],
        'L': [[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,1,1,1,1]],
        'I': [[1,1,1,1,1],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[1,1,1,1,1]],
        'N': [[1,0,0,0,1],[1,1,0,0,1],[1,0,1,0,1],[1,0,1,0,1],[1,0,0,1,1],[1,0,0,0,1],[1,0,0,0,1]],
        'T': [[1,1,1,1,1],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0]],
    }
    _GLYPH_COLORS = ['#ff4444', '#ff8800', '#ffcc00', '#44dd55', '#3399ff']

    def __init__(self):
        self.root = tk.Tk()
        # Tk's own hook — this is what actually renames the macOS menu bar
        # (process tricks like setprogname are not enough for Tk/NSApplication).
        try:
            self.root.tk.call('tk', 'appname', 'Flint')
        except Exception:
            pass
        self.root.title("Flint")
        self.root.configure(bg=self.BG)
        self.root.geometry("980x760")
        self.root.minsize(700, 500)
        self.root.resizable(True, True)
        self._current_file = None
        self._projects_dir = _projects_dir()
        self._build_fonts()
        self._build_menu()
        self._build_ui()
        self._setup_bindings()
        self._setup_highlight_tags()
        self._schedule_mac_menu_branding()

    def _build_fonts(self):
        for name in ("SF Mono", "Menlo", "Monaco", "Courier New", "Courier"):
            try:
                f = tkfont.Font(family=name, size=14)
                if f.actual()['family'].lower() not in ('helvetica', '.sf ns text'):
                    self._font_family = name
                    self.mono      = tkfont.Font(family=name, size=14)
                    self.mono_sm   = tkfont.Font(family=name, size=10)
                    self.mono_btn  = tkfont.Font(family=name, size=13, weight='bold')
                    self.mono_out  = tkfont.Font(family=name, size=13)
                    self.mono_logo = tkfont.Font(family=name, size=11)
                    return
            except Exception:
                pass
        self._font_family = "Courier"
        self.mono = self.mono_sm = self.mono_btn = self.mono_out = self.mono_logo = \
            tkfont.Font(family="Courier", size=13)

    def _build_menu(self):
        import tkinter.filedialog as tkfile
        self._tkfile = tkfile

        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # ── File ──────────────────────────────────
        fm = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=fm)
        fm.add_command(label="New",              accelerator="Cmd+N",       command=self.clear_editor)
        fm.add_command(label="Open…",            accelerator="Cmd+O",       command=self._open_file)
        fm.add_separator()
        fm.add_command(label="Save",             accelerator="Cmd+S",       command=self._save_file)
        fm.add_command(label="Save As…",         accelerator="Cmd+Shift+S", command=self._save_file_as)
        fm.add_separator()
        fm.add_command(label="Close",            accelerator="Cmd+W",       command=self.root.destroy)

        # ── Edit ──────────────────────────────────
        em = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=em)
        em.add_command(label="Undo",             accelerator="Cmd+Z",  command=lambda: self.code.edit_undo())
        em.add_command(label="Redo",             accelerator="Cmd+Y",  command=lambda: self.code.edit_redo())
        em.add_separator()
        em.add_command(label="Cut",              accelerator="Cmd+X",  command=lambda: self.code.event_generate("<<Cut>>"))
        em.add_command(label="Copy",             accelerator="Cmd+C",  command=lambda: self.code.event_generate("<<Copy>>"))
        em.add_command(label="Paste",            accelerator="Cmd+V",  command=lambda: self.code.event_generate("<<Paste>>"))
        em.add_command(label="Select All",       accelerator="Cmd+A",  command=lambda: self.code.tag_add('sel', '1.0', 'end'))
        em.add_separator()
        em.add_command(label="Delete Line",      accelerator="Ctrl+Del", command=self._delete_last_line)

        # ── Run ───────────────────────────────────
        rm = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Run", menu=rm)
        rm.add_command(label="Run Code",         accelerator="F1",     command=self.run_code)
        rm.add_command(label="Clear Editor",                           command=self.clear_editor)
        rm.add_command(label="Clear Output",                           command=self.clear_output)

        # ── Help ──────────────────────────────────
        hm = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=hm)
        hm.add_command(label="About Flint", command=self._mac_about_flint)

    def _mac_about_flint(self, *args):
        tkmessagebox.showinfo(
            "About Flint",
            f"Flint Programming Language\n\n"
            f"Version {VERSION}\n\n"
            f"© 2026 Henry Marcais. All rights reserved.\n\n"
            f"A simple language for creative coding.",
            parent=self.root,
        )

    def _apply_mac_menu_branding(self):
        """Rename app menu to Flint and replace About (orderFrontStandardAboutPanel)."""
        if sys.platform != 'darwin':
            return
        try:
            from AppKit import NSApplication
        except ImportError:
            return
        try:
            app = NSApplication.sharedApplication()
            bar = app.mainMenu()
            if not bar or bar.numberOfItems() < 1:
                return
            bar.itemAtIndex_(0).setTitle_("Flint")
            app_menu = bar.itemAtIndex_(0).submenu()
            if not app_menu:
                return
            Cls = _flint_about_bridge_class()
            if Cls is None:
                return
            target = Cls.alloc().initWithFlint_(self)
            self._mac_about_bridge = target
            # Force the first app-menu item ("About ...") no matter its title.
            if app_menu.numberOfItems() > 0:
                about_item = app_menu.itemAtIndex_(0)
                about_item.setTitle_("About Flint")
                about_item.setTarget_(target)
                about_item.setAction_("showFlintAbout:")
            for i in range(app_menu.numberOfItems()):
                item = app_menu.itemAtIndex_(i)
                title = item.title()
                if not title:
                    continue
                if title.startswith('About '):
                    item.setTitle_("About Flint")
                    item.setTarget_(target)
                    item.setAction_("showFlintAbout:")
                elif 'Python' in title:
                    item.setTitle_(title.replace('Python', 'Flint'))
        except Exception:
            pass

    def _schedule_mac_menu_branding(self):
        if sys.platform != 'darwin':
            return
        def go():
            self._apply_mac_menu_branding()
        self.root.after_idle(go)
        self.root.after(100, go)
        self.root.after(400, go)
        self.root.after(1200, go)
        self.root.after(3000, go)

    def _open_file(self):
        path = self._tkfile.askopenfilename(
            title="Open Flint File",
            initialdir=self._projects_dir,
            filetypes=[("Flint Files", "*.flt"), ("Text Files", "*.txt"), ("All Files", "*.*")])
        if not path:
            return
        with open(path, 'r') as f:
            content = f.read()
        self.code.delete('1.0', 'end')
        self.code.insert('1.0', content)
        self._current_file = path
        self.root.title(f"Flint — {os.path.basename(path)}")
        self._update_line_numbers()
        self._highlight()

    def _save_file(self):
        if self._current_file:
            with open(self._current_file, 'w') as f:
                f.write(self.code.get('1.0', 'end-1c'))
            self._status_lbl.config(text="saved ✓", fg="#44dd55")
        else:
            self._save_file_as()

    def _save_file_as(self):
        path = self._tkfile.asksaveasfilename(
            title="Save Flint File",
            initialdir=self._projects_dir,
            defaultextension=".flt",
            filetypes=[("Flint Files", "*.flt"), ("Text Files", "*.txt"), ("All Files", "*.*")])
        if not path:
            return
        self._current_file = path
        self.root.title(f"Flint — {os.path.basename(path)}")
        self._save_file()

    def _build_ui(self):
        # ── Header: pixel-art logo on canvas ──────
        header = tk.Frame(self.root, bg=self.BG)
        header.pack(fill='x', pady=(18, 0))

        px, gap, letter_gap = 9, 2, 14
        cols, rows = 5, 7
        cell = px + gap
        n_letters = len(self._GLYPHS)
        cw = n_letters * cols * cell + (n_letters - 1) * letter_gap
        ch = rows * cell

        logo_canvas = tk.Canvas(header, width=cw, height=ch,
                                bg=self.BG, highlightthickness=0)
        logo_canvas.pack(anchor='center')

        for li, (letter, color) in enumerate(zip('FLINT', self._GLYPH_COLORS)):
            glyph = self._GLYPHS[letter]
            x_off = li * (cols * cell + letter_gap)
            for r, row in enumerate(glyph):
                for c, on in enumerate(row):
                    if on:
                        x1 = x_off + c * cell
                        y1 = r * cell
                        logo_canvas.create_rectangle(
                            x1, y1, x1 + px, y1 + px,
                            fill=color, outline='')

        tk.Label(header,
                 text="© 2026 Henry Marcais  •  Flint v" + VERSION,
                 font=self.mono_sm, fg=self.FG_DIM, bg=self.BG).pack(pady=(8, 10))

        # ── Toolbar ───────────────────────────────
        tk.Frame(self.root, bg=self.BORDER, height=1).pack(fill='x')
        toolbar = tk.Frame(self.root, bg=self.BG3)
        toolbar.pack(fill='x')
        inner = tk.Frame(toolbar, bg=self.BG3)
        inner.pack(fill='x', padx=16, pady=8)

        def lbtn(parent, label, bg, fg, cmd):
            """Label-based button — macOS won't override its background color."""
            w = tk.Label(parent, text=label, font=self.mono_btn,
                         bg=bg, fg=fg, padx=18, pady=7, cursor='hand2')
            w.bind('<Button-1>', lambda e: cmd())
            w.bind('<Enter>',    lambda e: w.config(bg=_hex_lighten(bg)))
            w.bind('<Leave>',    lambda e: w.config(bg=bg))
            return w

        lbtn(inner, "▶  Run",   "#238636", "#ffffff", self.run_code).pack(side='left', padx=(0, 4))
        tk.Label(inner, text="F1", font=self.mono_sm,
                 fg=self.FG_DIM, bg=self.BG3).pack(side='left', padx=(0, 16))
        lbtn(inner, "⟳  Clear", "#2d333b", self.FG,  self.clear_editor).pack(side='left', padx=(0, 4))
        lbtn(inner, "✕  Quit",  "#2d333b", self.FG,  self.root.destroy).pack(side='left', padx=(0, 4))

        tk.Label(inner,
                 text="F2 quit   •   Ctrl+Z undo   •   Ctrl+Del delete line",
                 font=self.mono_sm, fg=self.FG_DIM, bg=self.BG3).pack(side='right')

        tk.Frame(self.root, bg=self.BORDER, height=1).pack(fill='x')

        # ── Editor + line numbers ─────────────────
        editor_pane = tk.Frame(self.root, bg=self.BG2)
        editor_pane.pack(fill='both', expand=True)

        self.line_nums = tk.Text(
            editor_pane, font=self.mono,
            bg="#0d1117", fg="#444c56",
            relief='flat', bd=0, width=4,
            padx=6, pady=10,
            state='disabled', wrap='none',
            cursor='arrow', takefocus=0,
        )
        self.line_nums.pack(side='left', fill='y')
        tk.Frame(editor_pane, bg=self.BORDER, width=1).pack(side='left', fill='y')

        editor_inner = tk.Frame(editor_pane, bg=self.BG2)
        editor_inner.pack(side='left', fill='both', expand=True)

        self.code = tk.Text(
            editor_inner, font=self.mono,
            bg=self.BG2, fg=self.FG,
            insertbackground=self.CURSOR,
            selectbackground="#264f78",
            relief='flat', bd=0,
            padx=14, pady=10,
            wrap='none', undo=True,
        )
        vsb = tk.Scrollbar(editor_inner, orient='vertical', command=self._sync_scroll)
        self.code.configure(yscrollcommand=self._on_editor_scroll)
        vsb.pack(side='right', fill='y')
        self.code.pack(fill='both', expand=True)

        # ── Output panel ──────────────────────────
        tk.Frame(self.root, bg=self.BORDER, height=1).pack(fill='x')
        out_bar = tk.Frame(self.root, bg=self.BG3)
        out_bar.pack(fill='x')
        tk.Label(out_bar, text="  OUTPUT", font=self.mono_sm,
                 fg=self.FG_DIM, bg=self.BG3).pack(side='left', pady=4)
        _clr = tk.Label(out_bar, text="clear ✕", font=self.mono_sm,
                        bg=self.BG3, fg=self.FG_DIM, padx=10, pady=4, cursor='hand2')
        _clr.bind('<Button-1>', lambda e: self.clear_output())
        _clr.bind('<Enter>',    lambda e: _clr.config(fg=self.FG))
        _clr.bind('<Leave>',    lambda e: _clr.config(fg=self.FG_DIM))
        _clr.pack(side='right', padx=4)
        tk.Frame(self.root, bg=self.BORDER, height=1).pack(fill='x')

        self.output = tk.Text(
            self.root, font=self.mono_out,
            bg=self.BG, fg=self.FG,
            relief='flat', bd=0,
            padx=20, pady=12,
            wrap='word', state='disabled',
            height=8,
        )
        self.output.pack(fill='x')

        # ── Status bar ────────────────────────────
        tk.Frame(self.root, bg=self.BORDER, height=1).pack(fill='x')
        status = tk.Frame(self.root, bg=self.BG3)
        status.pack(fill='x')
        tk.Label(status, text="  Flint Programming Language",
                 font=self.mono_sm, fg="#555", bg=self.BG3).pack(side='left', pady=3)
        self._status_lbl = tk.Label(status, text="ready",
                 font=self.mono_sm, fg="#555", bg=self.BG3)
        self._status_lbl.pack(side='right', padx=12, pady=3)

    def _sync_scroll(self, *args):
        self.code.yview(*args)
        self.line_nums.yview(*args)

    def _on_editor_scroll(self, first, last):
        self.line_nums.yview_moveto(first)

    def _update_line_numbers(self):
        content = self.code.get('1.0', 'end-1c')
        n = content.count('\n') + 1
        nums = '\n'.join(str(i).rjust(3) for i in range(1, n + 1))
        self.line_nums.config(state='normal')
        self.line_nums.delete('1.0', 'end')
        self.line_nums.insert('1.0', nums)
        self.line_nums.config(state='disabled')

    def clear_editor(self):
        self.code.delete('1.0', 'end')
        self._update_line_numbers()
        self.clear_output()

    def _setup_highlight_tags(self):
        # output tags
        self.output.config(state='normal')
        self.output.tag_config('error',  foreground='#ff4444')
        self.output.tag_config('result', foreground='#888888')
        self.output.tag_config('normal', foreground=self.FG)
        self.output.config(state='disabled')

        # editor syntax tags
        self.code.tag_config('_str',    foreground='#44ff88')
        self.code.tag_config('_num',    foreground='#79c0ff')
        self.code.tag_config('_var',    foreground='#e6edf3')
        for fn_name, fn in FUNCTIONS.items():
            color = COLOR_MAP.get(getattr(fn, '_lang_color', 'white'), '#e6edf3')
            self.code.tag_config(f'_fn_{fn_name}', foreground=color)

    def _setup_bindings(self):
        self.root.bind('<F1>',            lambda e: self.run_code())
        self.root.bind('<F2>',            lambda e: self.root.destroy())
        self.root.bind('<Control-z>',     lambda e: self.code.edit_undo())
        self.root.bind('<Control-Delete>', self._delete_last_line)
        self.root.bind('<Command-n>',     lambda e: self.clear_editor())
        self.root.bind('<Command-o>',     lambda e: self._open_file())
        self.root.bind('<Command-s>',     lambda e: self._save_file())
        self.root.bind('<Command-S>',     lambda e: self._save_file_as())
        self.root.bind('<Command-w>',     lambda e: self.root.destroy())
        self.code.bind('<KeyRelease>',    self._on_key)

        for open_ch, close_ch in [('(', ')'), ('"', '"'), ('{', '}'), ('[', ']')]:
            self.code.bind(open_ch, self._make_autoclose(open_ch, close_ch))

    def _make_autoclose(self, open_ch, close_ch):
        def handler(event):
            pos = self.code.index('insert')
            nxt = self.code.get(pos)
            if nxt == close_ch and open_ch != close_ch:
                self.code.mark_set('insert', f'{pos}+1c')
                return 'break'
            self.code.insert('insert', open_ch + close_ch)
            self.code.mark_set('insert', f'{pos}+1c')
            return 'break'
        return handler

    def _delete_last_line(self, event=None):
        last = self.code.index('end-1c linestart')
        self.code.delete(last, 'end-1c')

    def _on_key(self, event=None):
        self._update_line_numbers()
        self.root.after(1, self._highlight)

    def _highlight(self):
        text = self.code
        content = text.get('1.0', 'end')

        # Remove all tags
        for tag in text.tag_names():
            text.tag_remove(tag, '1.0', 'end')

        for line_i, line in enumerate(content.split('\n')):
            row = line_i + 1
            i = 0
            while i < len(line):
                if line[i] == '"':
                    j = i + 1
                    while j < len(line) and line[j] != '"':
                        j += 1
                    text.tag_add('_str', f'{row}.{i}', f'{row}.{j+1}')
                    i = j + 1
                elif line[i].isdigit():
                    j = i
                    while j < len(line) and (line[j].isdigit() or line[j] == '.'):
                        j += 1
                    text.tag_add('_num', f'{row}.{i}', f'{row}.{j}')
                    i = j
                elif line[i].isalpha() or line[i] == '_':
                    j = i
                    while j < len(line) and (line[j].isalnum() or line[j] == '_'):
                        j += 1
                    word = line[i:j]
                    if word in FUNCTIONS:
                        text.tag_add(f'_fn_{word}', f'{row}.{i}', f'{row}.{j}')
                    i = j
                else:
                    i += 1

    def write_output(self, msg, kind='normal'):
        self.output.config(state='normal')
        self.output.insert('end', msg + '\n', kind)
        self.output.see('end')
        self.output.config(state='disabled')

    def clear_output(self):
        self.output.config(state='normal')
        self.output.delete('1.0', 'end')
        self.output.config(state='disabled')

    def run_code(self):
        global _GUI_APP
        _GUI_APP = self
        self.clear_output()
        code = self.code.get('1.0', 'end').strip()
        if not code:
            return

        self._status_lbl.config(text="running…", fg="#58a6ff")
        self.root.update_idletasks()

        original_print = builtins.print
        original_input = builtins.input
        builtins.print = lambda *a, sep=' ', end='\n', **kw: \
            self.write_output(sep.join(str(x) for x in a))
        builtins.input = lambda prompt='': \
            tkdialog.askstring("Input", str(prompt), parent=self.root) or ''

        try:
            for line_num, line in enumerate(code.splitlines(), 1):
                _run_line(line, line_num)
            self._status_lbl.config(text="done ✓", fg="#44dd55")
        except Exception:
            self._status_lbl.config(text="error", fg="#ff4444")
        finally:
            builtins.print = original_print
            builtins.input = original_input

    def run(self):
        self._update_line_numbers()
        self.code.focus_set()
        self.root.mainloop()


def main():
    _check_update()
    app = FlintApp()
    app.run()


if __name__ == "__main__":
    main()
