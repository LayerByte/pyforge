# Architecture

PyForge separates pure tool functions from terminal rendering, persistent
history, configuration, and exporting. The lazy registry stores import paths,
so listing tools does not trigger network, filesystem, process, or Git work.
Tool results use JSON-friendly dictionaries and lists wherever practical.
