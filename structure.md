# Structure.md - How a build.py site is structured


## A page's TOML Structure

```toml
[page]
title = <Page Title>
navigation = [ {name = <Link Title>, link = <Link>}, ...]

[content]
body = '''
<Markdown/HTML Content>
'''

```
