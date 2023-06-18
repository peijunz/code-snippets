from flask import Flask, render_template, send_file, redirect, Response
import os
import sys

app = Flask(__name__)

CWD = '.'

TXT_FILES = ['py', 'txt', 'md', 'yaml', 'json', 'html', 'log']
MIMETYPES = {
    'html': 'text/html',
    'json': 'application/json',
    }

def get_mimetype(format):
    """Return mimetype metadata according to file format"""
    return MIMETYPES.get(format, 'text/plain')

def get_format(fname):
    """Infer file format from file name"""
    return fname.split('.')[-1]

def simplify_logic_path(url_path: str) -> str:
    """Simplify the logic path.

    Input should not contain leading slash, and the simplified path
    will also not contain leading /. The simplified path will not contain
    trailing / unless original path does.

    Examples
    =========
    '/'         => 无效输入
    ''          => ''
    'a/'        => 'a/'
    'a/b/..'    => 'a'
    'a/../..'   => ''
    """
    assert (not url_path) or url_path[0] != '/', "path should not contain leading /"
    stack = []
    for sub in url_path.split('/'):
        if sub == '..':
            if stack:
                stack.pop()
        elif sub != '.' and sub:
            stack.append(sub)
    if url_path.endswith('/'):
        stack.append('')
    return '/'.join(stack)

def path_exists(fs_path):
    """Decide that the dir or file exists

    fs_path indicates directory or file by trailing slash
    """
    if fs_path.endswith('/') and not os.path.isdir(fs_path):
        return False
    if not fs_path.endswith('/') and not os.path.isfile(fs_path):
        return False
    return True

def redirect_and_404(url_path):
    """重定向和404等异常路径"""
    # simplify path.
    simplified = simplify_logic_path(url_path)
    if simplified != url_path:
        return redirect(simplified)

    fs_path = os.path.join(CWD, simplified)

    # redirect directory with no slash /
    if not fs_path.endswith('/') and os.path.isdir(fs_path):
        return redirect(url_path + '/')

    # report 404 if file/dir is not found.
    if not path_exists(fs_path):
        return render_template('404.html'), 404

def handle_directory(url_path, fs_path):
    """Handle directory"""
    # fs_path points to a dir
    subs = ['../']
    subs += [x.name + '/' if x.is_dir() else x.name for x in os.scandir(fs_path)]
    subs.sort()

    # index.html is supplied
    if 'index.html' in subs:
        with open(fs_path + 'index.html') as page:
            contents = page.read()
        return contents
    return render_template("directfor.html", cur_dir = '/' + url_path, subs = subs)

def handle_file(url_path, fs_path):
    """Handle file"""
    format = get_format(fs_path)
    # send file
    if format not in TXT_FILES:
        return send_file(fs_path, as_attachment=True)

    # send contents
    with open(fs_path) as f:
        contents = f.read()
    return Response(contents, status=200, mimetype=get_mimetype(format))

@app.route('/', defaults = {'url_path':''})
@app.route('/<path:url_path>')
def direct(url_path):
    redirect_response = redirect_and_404(url_path)
    if redirect_response:
        return redirect_response

    # path is already simplified, so we just join current to get actual path
    fs_path = os.path.join(CWD, url_path)
    if fs_path.endswith('/'):
        return handle_directory(url_path, fs_path)
    return handle_file(url_path, fs_path)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        CWD = sys.argv[1]
    app.run(debug = True, port=5000)
