# [My personal homepage](http://oliver.bestwalter.de) [(src)](https://github.com/obestwalter/obestwalter.github.io)

## Installation

Use the officially recommended (but very unusual) Python2.7 installation:

    mkvirtualenv 2.7.11 lektor
    curl -sf https://www.getlektor.com/install.sh | sh
    pip install -e .

Hopefully installing lektor with pip and Python3 is possible soonish.

The inbuilt pygments plugin has a bug (creates wrong class name 'highlight' instead of 'hll'). I use my own stylesheet with adapted class name atm. Hint: list themes with `pygmentize -L` and generate css files with `pygmentize -S <theme name> -f html > <file name>.css`

## Development

Plugin development:

    LEKTOR_DEV=1 lektor server

## Acknowledgements

* created with[Lektor](https://getlektor.com)
* served via [Github Pages](https://pages.github.com/)
* [google webfonts helper](https://google-webfonts-helper.herokuapp.com/fonts) (TTF versions need to be downloaded extra from somewhere else though :()
* [name that color](http://chir.ag/projects/name-that-color)
* [interactive CSS tools](http://www.cssmatic.com)
* [color blender](http://meyerweb.com/eric/tools/color-blend)
* [pygments, pygmentize](http://pygments.org/)
* [mkdocs](http://www.mkdocs.org) (not for this site but for documentation of my projects)

## Legalese

Code is under MIT license and content is CC BY-NC-SA 4.0. If code is integrated that has a different license the license is included in the source here and their license apply.

[![code license](https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/License_icon-mit-2.svg/32px-License_icon-mit-2.svg.png)](http://opensource.org/licenses/mit-license.php)
[![content license](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-nc-sa/4.0/)
