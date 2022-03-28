# Sources for my personal website

If you just want to read - this might look better: [https://oliver.bestwalter.de](https://oliver.bestwalter.de).

## Clone this project with submodules

3rd party packages in `packages` are [git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules), so cloning this repo completely means:

    $ git clone --recurse-submodules <url of this repo>

add submodules later after normal clone:

    $ git submodule update --init.
    
update submodules:

    $ git submodule update --remote <repo name>

add new plugin:

    $ git submodule add <repo url>
    $ git commit -am 'add <repo name>
    $ git push origin master

## Lektor development installation

The officially recommended way is weird and the way lektor deals with plugins is extra weird. I work from a local lektor clone with my own little server wrapper to be make it easier to debug and modify.

    $ cd /path/to/here
    $ pip install tox
    $ tox -e dev

## task automation

All things worth doing are accessible via tox:

    $ tox -av
    
shows what's on offer

## Acknowledgements

* created with 
    * [Lektor](https://getlektor.com)
    * (some articles) [Jupyter notebooks](https://jupyter.org/)
    * [old skool sass](https://sass-lang.com/documentation/syntax#the-indented-syntax)
    * no javascript

* served via [Github Pages](https://pages.github.com/)

* helpful tools
    * [google webfonts helper](https://google-webfonts-helper.herokuapp.com/fonts) (TTF versions need to be downloaded extra from somewhere else though :()
    * [name that color](http://chir.ag/projects/name-that-color)
    * [interactive CSS tools](http://www.cssmatic.com)
    * [color blender](http://meyerweb.com/eric/tools/color-blend)
    * [pygments, pygmentize](http://pygments.org/)
    
## notes

### Pygments bug

The inbuilt pygments plugin has a bug (creates wrong class name 'highlight' instead of 'hll'). For now I use my own stylesheet with adapted class name.

Hint: list themes with `pygmentize -L` and generate css files with `pygmentize -S <theme name> -f html > <file name>.css`

### sass problems?

When getting `LoadError: cannot load such file -- rb-fsevent` run:

    gem install rb-fsevent

## css is a wondrous thing

* https://iamvdo.me/en/blog/css-font-metrics-line-height-and-vertical-align
* https://font-display.glitch.me/
* https://www.w3.org/Style/Examples/007/units.en.html

## Legalese

Code is under MIT license and content is CC BY-NC-SA 4.0. If code is integrated that has a different license the license is included in the source here and their license apply.

[![code license](https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/License_icon-mit-2.svg/32px-License_icon-mit-2.svg.png)](http://opensource.org/licenses/mit-license.php)
[![content license](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-nc-sa/4.0/)
