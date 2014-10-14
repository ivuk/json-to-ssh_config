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
The `global.conf` file is a special case, its intended usage is to contain the
`Host *` settings that apply to all hosts:
```json
{
    "Host":"*",
    "ControlMaster":"auto",
    "ControlPath":"somepath",
    "ForwardAgent":"no",
    "IdentityFile":"somefile",
    "IdentitiesOnly":"yes",
    "Protocol":2,
    "User":"username",
    "VisualHostKey":"yes"
}
```
Which results in:
```sh
$ ./gensshconf.py -s .
# Content from ./global.conf
Host *
  ControlMaster auto
  ControlPath somepath
  ForwardAgent no
  IdentityFile somefile
  IdentitiesOnly yes
  Protocol 2
  User username
  VisualHostKey yes

```
Note that there are some aspects of ssh_config(5) which are not supported
directly, such as overriding a set of hosts via wildcards (`*.example.com`).
That could be hacked around via a combination of some smart file naming and
existing syntax.

There are two supported output modes, `screen` and `file`, controlled via the
`-o` parameter. The default value is `screen`. When used with the `-o file`
parameter, the default output file is `outfile-example` in the script
directory. This can be overriden via the `-f` parameter.
