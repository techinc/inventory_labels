== Inventory system for Technologia Incognita ==

label_gen/ : label generation

Needed packages (Ubuntu): texlive-xetex texlive-latex-recommended texlive-latex-extra

Usage for label:

usage: label.py [-h] [-o OWNER] [-p PERMS] {gen,print} name description

Generate and print labels for Technologia Incognita

positional arguments:
  {gen,print}           [gen]erate LaTeX to stdout or [print] to send directly
                        to printer.
  name                  the name of the item
  description           a description of the item

optional arguments:
  -h, --help            show this help message and exit
  -o OWNER, --owner OWNER
                        who the item belongs to [TechInc]
  -p PERMS, --perms PERMS
                        what we're allowed to do with it [Hack it]
