"""Modify lektors behaviour via monkeypatching."""
import importlib.util
import logging
import re
import subprocess
import time
from itertools import chain
from pprint import pformat
from types import ModuleType
from typing import List

import lektor.pluginsystem
import lektor.reporter
from lektor._compat import iteritems

from lebut.config import PATH

log = logging.getLogger(__name__)


def patch_all():
    lektor.reporter.CliReporter = CliReporterWithNotify
    lektor.pluginsystem.initialize_plugins = initialize_plugins_with_local_plugins


class CliReporterWithNotify(lektor.reporter.CliReporter):
    """Send notifications about build events."""

    def report_failure(self, artifact, exc_info):
        super().report_failure(artifact, exc_info)
        self._notify(
            f"{artifact.artifact_name}: {exc_info[1]}",
            urgency="critical",
            expire_time=5,
        )

    def start_build(self, activity):
        super().start_build(activity)
        self._notify(f"start {activity}", urgency="low")

    def finish_build(self, activity, start_time):
        super().finish_build(activity, start_time)
        self._notify(
            f"finish {activity} {time.time() - start_time:0.2f}", urgency="normal"
        )

    @staticmethod
    def _notify(msg, urgency="normal", expire_time=1):
        subprocess.check_call(
            [
                "notify-send",
                "--app-name",
                "lektor",
                "--urgency",
                urgency,
                "--expire-time",
                str(expire_time * 1000),
                msg,
            ]
        )


def initialize_plugins_with_local_plugins(env):
    """Initializes the plugins for the environment.

    Patch with LocalPluginRegistrator to load simple local plugins
    """
    plugins = lektor.pluginsystem.load_plugins()
    for plugin_id, plugin_cls in iteritems(plugins):
        env.plugin_controller.instanciate_plugin(plugin_id, plugin_cls)
    LocalPluginRegistrator.register(path=PATH.HERE, env=env)
    env.plugin_controller.emit("setup-env")


class LocalPluginRegistrator:
    """Collect plugin classes, initialize and register them.

    Only for simple, self-contained plugin modules.
    """

    PLUGIN_PATTERN = "plugin_*.py"

    @classmethod
    def register(cls, *, path, env):
        """Given a directory path: register all plugins with lektor.

        instantiate, initialize and add to env.
        This is outside of lektors normal flow, so calling initializers manually.
        Only using what is interesting for me here.
        Only works for plugins that don't need any special parameters passed in on init.
        """
        paths = list(path.glob(cls.PLUGIN_PATTERN))
        modules = [cls.get_module(path) for path in paths]
        classes = list(chain(*[cls.collect_classes(module) for module in modules]))
        for Klass in classes:
            parts = re.sub(r"([A-Z])", r" \1", Klass.__name__).split()
            id_ = "-".join([p.lower() for p in parts[:-1]])
            plugin = Klass(env, id_)
            env.plugins[id_] = plugin
            log.debug(f"added {plugin}")
        log.info(f"registered plugins:\n{pformat(env.plugins)}")

    @staticmethod
    def get_module(path) -> ModuleType:
        """Given a Python module path: load and evaluate it."""
        log.info(f"load {path}")
        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    @staticmethod
    def collect_classes(module: ModuleType) -> List[type]:
        """Given a module: collect the plugin class(es)."""
        classes = []
        for name in [n for n in dir(module) if not n.startswith("_")]:
            obj = getattr(module, name)
            if obj is lektor.pluginsystem.Plugin:
                continue

            try:
                if issubclass(obj, lektor.pluginsystem.Plugin):
                    classes.append(obj)
            except TypeError:
                pass
        return classes
