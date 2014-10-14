json-to-ssh_config
==================

A simple JSON to ssh_config file generator. The basic usage model is that you
stick all the JSON files into a certain folder (the default value is
`~/.ssh/confs/`, overrideable via the `-s` parameter), which then in turn get
loaded/validated via Python's `json.load()`, and translated to
[ssh_config(5)](manpg.es/ssh_config) file format.

There are some assumptions that the script makes:
* All JSON files are in the same folder
* All JSON files end with a `.conf` suffix
* All JSON files get {displayed,written} alphabetically, except for `global.conf`,
which is always last

