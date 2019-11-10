from livereload import Server

from lebut.config import PATH


def watch_output():
    server = Server()
    server.watch(PATH.OUTPUT)
    server.serve(root=str(PATH.OUTPUT))


if __name__ == '__main__':
    watch_output()
