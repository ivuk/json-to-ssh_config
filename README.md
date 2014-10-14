json-to-ssh_config
==================

A simple JSON to ssh_config file generator. The basic usage model is that you
stick all the JSON files into a certain folder (the default value is
`~/.ssh/confs/`, overrideable via the `-s` parameter), which then in turn get
loaded/validated via Python's `json.load()`, and translated to
[ssh_config(5)](http://manpg.es/ssh_config) file format.

There are some assumptions that the script makes:
* All JSON files are in the same folder
* All JSON files end with a `.conf` suffix
* All JSON files get {displayed,written} alphabetically, except for `global.conf`,
which is always last

There are two basic syntax models that are supported:

```json
{
    "Host":"aliasname",
    "HostName":"fqdnname",
    "Port":12345
}
```
Which results in:
```sh
$ ./gensshconf.py -s .
# Content from ./demo1.conf
Host aliasname
  HostName fqdnname
  Port 12345

```
And:
```json
{
    "default":
    {
        "IdentityFile":"pathtoidentityfile"
    },
    "Host":
    {
    "aliasname1":"fqdnname1",
    "aliasname2":"fqdnname2"
    }
}
```
Which results in:
```sh
$ ./gensshconf.py -s .
# Content from ./demo2.conf
Host aliasname1
  HostName fqdnname1
  IdentityFile pathtoidentityfile
Host aliasname2
  HostName fqdnname2
  IdentityFile pathtoidentityfile

```
