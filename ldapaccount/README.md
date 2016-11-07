# Intro
To use LDAP bind information on configuration file, you need to have .netrc file on your own direcotry.


# Setup

*  create .netrc file with 600 permission.
```
-rw-------.  1 annmoon eng      127 Oct 25 02:35 .netrc
```

* update below lines on .netrc file. 
```
machine name01
    login userid
    password password

machine name02
    login userid
    password password
```

# reference page:
* http://www.mavetju.org/unix/netrc.php
* https://www.gnu.org/software/inetutils/manual/html_node/The-_002enetrc-file.html
