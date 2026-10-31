"""Check public routes, local dependencies, and JavaScript syntax without packages."""
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ('href', 'src'):
            if attrs.get(key):
                self.links.append(attrs[key])

files = [ROOT/'index.html', *ROOT.joinpath('games').rglob('*.html'), *ROOT.joinpath('labs').rglob('*.html')]
for path in files:
    content = path.read_text()
    parser = Links(); parser.feed(content)
    for link in parser.links:
        url = urlsplit(link)
        if url.scheme or url.netloc or not url.path:
            continue
        assert not url.path.startswith('/'), f'Route must work under /staging/: {path}: {link}'
        target = (path.parent / unquote(url.path)).resolve()
        assert target == ROOT or ROOT in target.parents, f'Link escapes site: {link}'
        assert target.exists(), f'Missing route: {path}: {link}'
        if target.is_dir():
            assert (target/'index.html').exists(), f'Missing index: {link}'
    for script in re.findall(r'<script(?:\s[^>]*)?>([\s\S]*?)</script>', content):
        if script.strip():
            subprocess.run(['node', '--check', '-'], input=script, text=True, check=True)
for script in ROOT.joinpath('assets').rglob('*.js'):
    subprocess.run(['node', '--check', str(script)], check=True)
assert (ROOT/'CNAME').read_text().strip() == 'zoe.games'
print(f'Checked {len(files)} HTML pages, local routes, CNAME, and JavaScript syntax')
