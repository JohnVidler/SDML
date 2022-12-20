# SDML - The 'Simple' Document Markup Language

A 'Simple Document Markup Language' that will no doubt prove to be anything but 'Simple'

Written mostly as a learning tool, so I can hopefully become better at Python, but I'm uploading it here in the remote
chance that it might be of some use to anyone.

PRs welcome, if anyone wants to extend this monster :)

## Running

To run, clone the repository, and launch via `./sdml.py` in the project root. The program currently
accepts no command line arguments, but does recognise a handful of environment variables:

- SDML_BUILD_PATH: defaults to CWD/output
- SDML_SOURCE_PATH: defaults to CWD
- SDML_ENCODING: defaults to 'utf-8'