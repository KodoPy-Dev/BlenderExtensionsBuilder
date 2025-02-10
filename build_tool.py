########################•########################
"""                   NOTES                   """
########################•########################

'''
______LICENSE______
GNU GENERAL PUBLIC LICENSE

______DISCLAIMER______
This software is provided "as is" without any warranties, express or implied. 
Use at your own risk. The author is not responsible for any damage, data loss, 
or issues arising from the use of this code.

______USAGE______
Run python script from system terminal
>python build_tool.py
Use the GUI interface to set the Directories and Extension Settings
Press Build to generate the build folder, write the manifest file and process the build commands

______LEGEND______
PATH = Full file path with extension
DIR  = Directory only
EXE  = Executable File
MANI = Manifest
VER  = Version
DEV  = Developer
'''

########################•########################
"""                  IMPORTS                  """
########################•########################

import os
import re
import sys
import json
import shutil
import traceback
import subprocess
from pathlib import Path
from collections.abc import Iterable
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

########################•########################
"""                   OPTIONS                 """
########################•########################

LICENSES = {
    "BSD Zero Clause License"                                                                   : "0BSD",
    "3D Slicer License v1.0"                                                                    : "3D-Slicer-1.0",
    "Attribution Assurance License"                                                             : "AAL",
    "Abstyles License"                                                                          : "Abstyles",
    "AdaCore Doc License"                                                                       : "AdaCore-doc",
    "Adobe Systems Incorporated Source Code License Agreement"                                  : "Adobe-2006",
    "Adobe Display PostScript License"                                                          : "Adobe-Display-PostScript",
    "Adobe Glyph List License"                                                                  : "Adobe-Glyph",
    "Adobe Utopia Font License"                                                                 : "Adobe-Utopia",
    "Amazon Digital Services License"                                                           : "ADSL",
    "Academic Free License v1.1"                                                                : "AFL-1.1",
    "Academic Free License v1.2"                                                                : "AFL-1.2",
    "Academic Free License v2.0"                                                                : "AFL-2.0",
    "Academic Free License v2.1"                                                                : "AFL-2.1",
    "Academic Free License v3.0"                                                                : "AFL-3.0",
    "Afmparse License"                                                                          : "Afmparse",
    "Affero General Public License v1.0 only"                                                   : "AGPL-1.0-only",
    "Affero General Public License v1.0 or later"                                               : "AGPL-1.0-or-later",
    "GNU Affero General Public License v3.0 only"                                               : "AGPL-3.0-only",
    "GNU Affero General Public License v3.0 or later"                                           : "AGPL-3.0-or-later",
    "Aladdin Free Public License"                                                               : "Aladdin",
    "AMD newlib License"                                                                        : "AMD-newlib",
    "AMD's plpa_map.c License"                                                                  : "AMDPLPA",
    "Apple MIT License"                                                                         : "AML",
    "AML glslang variant License"                                                               : "AML-glslang",
    "Academy of Motion Picture Arts and Sciences BSD"                                           : "AMPAS",
    "ANTLR Software Rights Notice"                                                              : "ANTLR-PD",
    "ANTLR Software Rights Notice with license fallback"                                        : "ANTLR-PD-fallback",
    "Any OSI License"                                                                           : "any-OSI",
    "Any OSI License - Perl Modules"                                                            : "any-OSI-perl-modules",
    "Apache License 1.0"                                                                        : "Apache-1.0",
    "Apache License 1.1"                                                                        : "Apache-1.1",
    "Apache License 2.0"                                                                        : "Apache-2.0",
    "Adobe Postscript AFM License"                                                              : "APAFML",
    "Adaptive Public License 1.0"                                                               : "APL-1.0",
    "App::s2p License"                                                                          : "App-s2p",
    "Apple Public Source License 1.0"                                                           : "APSL-1.0",
    "Apple Public Source License 1.1"                                                           : "APSL-1.1",
    "Apple Public Source License 1.2"                                                           : "APSL-1.2",
    "Apple Public Source License 2.0"                                                           : "APSL-2.0",
    "Arphic Public License"                                                                     : "Arphic-1999",
    "Artistic License 1.0"                                                                      : "Artistic-1.0",
    "Artistic License 1.0 w/clause 8"                                                           : "Artistic-1.0-cl8",
    "Artistic License 1.0 (Perl)"                                                               : "Artistic-1.0-Perl",
    "Artistic License 2.0"                                                                      : "Artistic-2.0",
    "ASWF Digital Assets License version 1.0"                                                   : "ASWF-Digital-Assets-1.0",
    "ASWF Digital Assets License 1.1"                                                           : "ASWF-Digital-Assets-1.1",
    "Baekmuk License"                                                                           : "Baekmuk",
    "Bahyph License"                                                                            : "Bahyph",
    "Barr License"                                                                              : "Barr",
    "bcrypt Solar Designer License"                                                             : "bcrypt-Solar-Designer",
    "Beerware License"                                                                          : "Beerware",
    "Bitstream Charter Font License"                                                            : "Bitstream-Charter",
    "Bitstream Vera Font License"                                                               : "Bitstream-Vera",
    "BitTorrent Open Source License v1.0"                                                       : "BitTorrent-1.0",
    "BitTorrent Open Source License v1.1"                                                       : "BitTorrent-1.1",
    "SQLite Blessing"                                                                           : "blessing",
    "Blue Oak Model License 1.0.0"                                                              : "BlueOak-1.0.0",
    "Boehm-Demers-Weiser GC License"                                                            : "Boehm-GC",
    "Boehm-Demers-Weiser GC License (without fee)"                                              : "Boehm-GC-without-fee",
    "Borceux license"                                                                           : "Borceux",
    "Brian Gladman 2-Clause License"                                                            : "Brian-Gladman-2-Clause",
    "Brian Gladman 3-Clause License"                                                            : "Brian-Gladman-3-Clause",
    "BSD 1-Clause License"                                                                      : "BSD-1-Clause",
    "BSD 2-Clause Simplified License"                                                           : "BSD-2-Clause",
    "BSD 2-Clause - Ian Darwin variant"                                                         : "BSD-2-Clause-Darwin",
    "BSD 2-Clause - first lines requirement"                                                    : "BSD-2-Clause-first-lines",
    "BSD-2-Clause Plus Patent License"                                                          : "BSD-2-Clause-Patent",
    "BSD 2-Clause with views sentence"                                                          : "BSD-2-Clause-Views",
    "BSD 3-Clause New or Revised License"                                                       : "BSD-3-Clause",
    "BSD 3-Clause acpica variant"                                                               : "BSD-3-Clause-acpica",
    "BSD with attribution"                                                                      : "BSD-3-Clause-Attribution",
    "BSD 3-Clause Clear License"                                                                : "BSD-3-Clause-Clear",
    "BSD 3-Clause Flex variant"                                                                 : "BSD-3-Clause-flex",
    "Hewlett-Packard BSD variant license"                                                       : "BSD-3-Clause-HP",
    "Lawrence Berkeley National Labs BSD variant license"                                       : "BSD-3-Clause-LBNL",
    "BSD 3-Clause Modification"                                                                 : "BSD-3-Clause-Modification",
    "BSD 3-Clause No Military License"                                                          : "BSD-3-Clause-No-Military-License",
    "BSD 3-Clause No Nuclear License"                                                           : "BSD-3-Clause-No-Nuclear-License",
    "BSD 3-Clause No Nuclear License 2014"                                                      : "BSD-3-Clause-No-Nuclear-License-2014",
    "BSD 3-Clause No Nuclear Warranty"                                                          : "BSD-3-Clause-No-Nuclear-Warranty",
    "BSD 3-Clause Open MPI variant"                                                             : "BSD-3-Clause-Open-MPI",
    "BSD 3-Clause Sun Microsystems"                                                             : "BSD-3-Clause-Sun",
    "BSD 4-Clause Original or Old License"                                                      : "BSD-4-Clause",
    "BSD 4 Clause Shortened"                                                                    : "BSD-4-Clause-Shortened",
    "BSD-4-Clause (University of California-Specific)"                                          : "BSD-4-Clause-UC",
    "BSD 4.3 RENO License"                                                                      : "BSD-4.3RENO",
    "BSD 4.3 TAHOE License"                                                                     : "BSD-4.3TAHOE",
    "BSD Advertising Acknowledgement License"                                                   : "BSD-Advertising-Acknowledgement",
    "BSD with Attribution and HPND disclaimer"                                                  : "BSD-Attribution-HPND-disclaimer",
    "BSD-Inferno-Nettverk"                                                                      : "BSD-Inferno-Nettverk",
    "BSD Protection License"                                                                    : "BSD-Protection",
    "BSD Source Code Attribution - beginning of file variant"                                   : "BSD-Source-beginning-file",
    "BSD Source Code Attribution"                                                               : "BSD-Source-Code",
    "Systemics BSD variant license"                                                             : "BSD-Systemics",
    "Systemics W3Works BSD variant license"                                                     : "BSD-Systemics-W3Works",
    "Boost Software License 1.0"                                                                : "BSL-1.0",
    "Business Source License 1.1"                                                               : "BUSL-1.1",
    "bzip2 and libbzip2 License v1.0.6"                                                         : "bzip2-1.0.6",
    "Computational Use of Data Agreement v1.0"                                                  : "C-UDA-1.0",
    "Cryptographic Autonomy License 1.0"                                                        : "CAL-1.0",
    "Cryptographic Autonomy License 1.0 (Combined Work Exception)"                              : "CAL-1.0-Combined-Work-Exception",
    "Caldera License"                                                                           : "Caldera",
    "Caldera License (without preamble)"                                                        : "Caldera-no-preamble",
    "Catharon License"                                                                          : "Catharon",
    "Computer Associates Trusted Open Source License 1.1"                                       : "CATOSL-1.1",
    "Creative Commons Attribution 1.0 Generic"                                                  : "CC-BY-1.0",
    "Creative Commons Attribution 2.0 Generic"                                                  : "CC-BY-2.0",
    "Creative Commons Attribution 2.5 Generic"                                                  : "CC-BY-2.5",
    "Creative Commons Attribution 2.5 Australia"                                                : "CC-BY-2.5-AU",
    "Creative Commons Attribution 3.0 Unported"                                                 : "CC-BY-3.0",
    "Creative Commons Attribution 3.0 Austria"                                                  : "CC-BY-3.0-AT",
    "Creative Commons Attribution 3.0 Australia"                                                : "CC-BY-3.0-AU",
    "Creative Commons Attribution 3.0 Germany"                                                  : "CC-BY-3.0-DE",
    "Creative Commons Attribution 3.0 IGO"                                                      : "CC-BY-3.0-IGO",
    "Creative Commons Attribution 3.0 Netherlands"                                              : "CC-BY-3.0-NL",
    "Creative Commons Attribution 3.0 United States"                                            : "CC-BY-3.0-US",
    "Creative Commons Attribution 4.0 International"                                            : "CC-BY-4.0",
    "Creative Commons Attribution Non Commercial 1.0 Generic"                                   : "CC-BY-NC-1.0",
    "Creative Commons Attribution Non Commercial 2.0 Generic"                                   : "CC-BY-NC-2.0",
    "Creative Commons Attribution Non Commercial 2.5 Generic"                                   : "CC-BY-NC-2.5",
    "Creative Commons Attribution Non Commercial 3.0 Unported"                                  : "CC-BY-NC-3.0",
    "Creative Commons Attribution Non Commercial 3.0 Germany"                                   : "CC-BY-NC-3.0-DE",
    "Creative Commons Attribution Non Commercial 4.0 International"                             : "CC-BY-NC-4.0",
    "Creative Commons Attribution Non Commercial No Derivatives 1.0 Generic"                    : "CC-BY-NC-ND-1.0",
    "Creative Commons Attribution Non Commercial No Derivatives 2.0 Generic"                    : "CC-BY-NC-ND-2.0",
    "Creative Commons Attribution Non Commercial No Derivatives 2.5 Generic"                    : "CC-BY-NC-ND-2.5",
    "Creative Commons Attribution Non Commercial No Derivatives 3.0 Unported"                   : "CC-BY-NC-ND-3.0",
    "Creative Commons Attribution Non Commercial No Derivatives 3.0 Germany"                    : "CC-BY-NC-ND-3.0-DE",
    "Creative Commons Attribution Non Commercial No Derivatives 3.0 IGO"                        : "CC-BY-NC-ND-3.0-IGO",
    "Creative Commons Attribution Non Commercial No Derivatives 4.0 International"              : "CC-BY-NC-ND-4.0",
    "Creative Commons Attribution Non Commercial Share Alike 1.0 Generic"                       : "CC-BY-NC-SA-1.0",
    "Creative Commons Attribution Non Commercial Share Alike 2.0 Generic"                       : "CC-BY-NC-SA-2.0",
    "Creative Commons Attribution Non Commercial Share Alike 2.0 Germany"                       : "CC-BY-NC-SA-2.0-DE",
    "Creative Commons Attribution-NonCommercial-ShareAlike 2.0 France"                          : "CC-BY-NC-SA-2.0-FR",
    "Creative Commons Attribution Non Commercial Share Alike 2.0 England and Wales"             : "CC-BY-NC-SA-2.0-UK",
    "Creative Commons Attribution Non Commercial Share Alike 2.5 Generic"                       : "CC-BY-NC-SA-2.5",
    "Creative Commons Attribution Non Commercial Share Alike 3.0 Unported"                      : "CC-BY-NC-SA-3.0",
    "Creative Commons Attribution Non Commercial Share Alike 3.0 Germany"                       : "CC-BY-NC-SA-3.0-DE",
    "Creative Commons Attribution Non Commercial Share Alike 3.0 IGO"                           : "CC-BY-NC-SA-3.0-IGO",
    "Creative Commons Attribution Non Commercial Share Alike 4.0 International"                 : "CC-BY-NC-SA-4.0",
    "Creative Commons Attribution No Derivatives 1.0 Generic"                                   : "CC-BY-ND-1.0",
    "Creative Commons Attribution No Derivatives 2.0 Generic"                                   : "CC-BY-ND-2.0",
    "Creative Commons Attribution No Derivatives 2.5 Generic"                                   : "CC-BY-ND-2.5",
    "Creative Commons Attribution No Derivatives 3.0 Unported"                                  : "CC-BY-ND-3.0",
    "Creative Commons Attribution No Derivatives 3.0 Germany"                                   : "CC-BY-ND-3.0-DE",
    "Creative Commons Attribution No Derivatives 4.0 International"                             : "CC-BY-ND-4.0",
    "Creative Commons Attribution Share Alike 1.0 Generic"                                      : "CC-BY-SA-1.0",
    "Creative Commons Attribution Share Alike 2.0 Generic"                                      : "CC-BY-SA-2.0",
    "Creative Commons Attribution Share Alike 2.0 England and Wales"                            : "CC-BY-SA-2.0-UK",
    "Creative Commons Attribution Share Alike 2.1 Japan"                                        : "CC-BY-SA-2.1-JP",
    "Creative Commons Attribution Share Alike 2.5 Generic"                                      : "CC-BY-SA-2.5",
    "Creative Commons Attribution Share Alike 3.0 Unported"                                     : "CC-BY-SA-3.0",
    "Creative Commons Attribution Share Alike 3.0 Austria"                                      : "CC-BY-SA-3.0-AT",
    "Creative Commons Attribution Share Alike 3.0 Germany"                                      : "CC-BY-SA-3.0-DE",
    "Creative Commons Attribution-ShareAlike 3.0 IGO"                                           : "CC-BY-SA-3.0-IGO",
    "Creative Commons Attribution Share Alike 4.0 International"                                : "CC-BY-SA-4.0",
    "Creative Commons Public Domain Dedication and Certification"                               : "CC-PDDC",
    "Creative    Commons Public Domain Mark 1.0 Universal"                                      : "CC-PDM-1.0",
    "Creative Commons Share Alike 1.0 Generic"                                                  : "CC-SA-1.0",
    "Creative Commons Zero v1.0 Universal"                                                      : "CC0-1.0",
    "Common Development and Distribution License 1.0"                                           : "CDDL-1.0",
    "Common Development and Distribution License 1.1"                                           : "CDDL-1.1",
    "Common Documentation License 1.0"                                                          : "CDL-1.0",
    "Community Data License Agreement Permissive 1.0"                                           : "CDLA-Permissive-1.0",
    "Community Data License Agreement Permissive 2.0"                                           : "CDLA-Permissive-2.0",
    "Community Data License Agreement Sharing 1.0"                                              : "CDLA-Sharing-1.0",
    "CeCILL Free Software License Agreement v1.0"                                               : "CECILL-1.0",
    "CeCILL Free Software License Agreement v1.1"                                               : "CECILL-1.1",
    "CeCILL Free Software License Agreement v2.0"                                               : "CECILL-2.0",
    "CeCILL Free Software License Agreement v2.1"                                               : "CECILL-2.1",
    "CeCILL-B Free Software License Agreement"                                                  : "CECILL-B",
    "CeCILL-C Free Software License Agreement"                                                  : "CECILL-C",
    "CERN Open Hardware Licence v1.1"                                                           : "CERN-OHL-1.1",
    "CERN Open Hardware Licence v1.2"                                                           : "CERN-OHL-1.2",
    "CERN Open Hardware Licence Version 2 - Permissive"                                         : "CERN-OHL-P-2.0",
    "CERN Open Hardware Licence Version 2 - Strongly Reciprocal"                                : "CERN-OHL-S-2.0",
    "CERN Open Hardware Licence Version 2 - Weakly Reciprocal"                                  : "CERN-OHL-W-2.0",
    "CFITSIO License"                                                                           : "CFITSIO",
    "check-cvs License"                                                                         : "check-cvs",
    "Checkmk License"                                                                           : "checkmk",
    "Clarified Artistic License"                                                                : "ClArtistic",
    "Clips License"                                                                             : "Clips",
    "CMU Mach License"                                                                          : "CMU-Mach",
    "CMU    Mach - no notices-in-documentation variant"                                         : "CMU-Mach-nodoc",
    "CNRI Jython License"                                                                       : "CNRI-Jython",
    "CNRI Python License"                                                                       : "CNRI-Python",
    "CNRI Python Open Source GPL Compatible License Agreement"                                  : "CNRI-Python-GPL-Compatible",
    "Copyfree Open Innovation License"                                                          : "COIL-1.0",
    "Community Specification License 1.0"                                                       : "Community-Spec-1.0",
    "Condor Public License v1.1"                                                                : "Condor-1.1",
    "copyleft-next 0.3.0"                                                                       : "copyleft-next-0.3.0",
    "copyleft-next 0.3.1"                                                                       : "copyleft-next-0.3.1",
    "Cornell Lossless JPEG License"                                                             : "Cornell-Lossless-JPEG",
    "Common Public Attribution License 1.0"                                                     : "CPAL-1.0",
    "Common Public License 1.0"                                                                 : "CPL-1.0",
    "Code Project Open License 1.02"                                                            : "CPOL-1.02",
    "Cronyx License"                                                                            : "Cronyx",
    "Crossword License"                                                                         : "Crossword",
    "CrystalStacker License"                                                                    : "CrystalStacker",
    "CUA Office Public License v1.0"                                                            : "CUA-OPL-1.0",
    "Cube License"                                                                              : "Cube",
    "curl License"                                                                              : "curl",
    "Common Vulnerability Enumeration ToU License"                                              : "cve-tou",
    "Deutsche Freie Software Lizenz"                                                            : "D-FSL-1.0",
    "DEC 3-Clause License"                                                                      : "DEC-3-Clause",
    "diffmark license"                                                                          : "diffmark",
    "Data licence Germany â attribution â version 2.0"                                          : "DL-DE-BY-2.0",
    "Data licence Germany â zero â version 2.0"                                                 : "DL-DE-ZERO-2.0",
    "DOC License"                                                                               : "DOC",
    "DocBook Schema License"                                                                    : "DocBook-Schema",
    "DocBook Stylesheet License"                                                                : "DocBook-Stylesheet",
    "DocBook XML License"                                                                       : "DocBook-XML",
    "Dotseqn License"                                                                           : "Dotseqn",
    "Detection Rule License 1.0"                                                                : "DRL-1.0",
    "Detection Rule License 1.1"                                                                : "DRL-1.1",
    "DSDP License"                                                                              : "DSDP",
    "David M. Gay dtoa License"                                                                 : "dtoa",
    "dvipdfm License"                                                                           : "dvipdfm",
    "Educational Community License v1.0"                                                        : "ECL-1.0",
    "Educational Community License v2.0"                                                        : "ECL-2.0",
    "Eiffel Forum License v1.0"                                                                 : "EFL-1.0",
    "Eiffel Forum License v2.0"                                                                 : "EFL-2.0",
    "eGenix.com Public License 1.1.0"                                                           : "eGenix",
    "Elastic License 2.0"                                                                       : "Elastic-2.0",
    "Entessa Public License v1.0"                                                               : "Entessa",
    "EPICS Open License"                                                                        : "EPICS",
    "Eclipse Public License 1.0"                                                                : "EPL-1.0",
    "Eclipse Public License 2.0"                                                                : "EPL-2.0",
    "Erlang Public License v1.1"                                                                : "ErlPL-1.1",
    "Etalab Open License 2.0"                                                                   : "etalab-2.0",
    "EU DataGrid Software License"                                                              : "EUDatagrid",
    "European Union Public License 1.0"                                                         : "EUPL-1.0",
    "European Union Public License 1.1"                                                         : "EUPL-1.1",
    "European Union Public License 1.2"                                                         : "EUPL-1.2",
    "Eurosym License"                                                                           : "Eurosym",
    "Fair License"                                                                              : "Fair",
    "Fuzzy Bitmap License"                                                                      : "FBM",
    "Fraunhofer FDK AAC Codec Library"                                                          : "FDK-AAC",
    "Ferguson Twofish License"                                                                  : "Ferguson-Twofish",
    "Frameworx Open License 1.0"                                                                : "Frameworx-1.0",
    "FreeBSD Documentation License"                                                             : "FreeBSD-DOC",
    "FreeImage Public License v1.0"                                                             : "FreeImage",
    "FSF All Permissive License"                                                                : "FSFAP",
    "FSF All Permissive License (without Warranty)"                                             : "FSFAP-no-warranty-disclaimer",
    "FSF Unlimited License"                                                                     : "FSFUL",
    "FSF Unlimited License (with License Retention)"                                            : "FSFULLR",
    "FSF Unlimited License (With License Retention and Warranty Disclaimer)"                    : "FSFULLRWD",
    "Freetype Project License"                                                                  : "FTL",
    "Furuseth License"                                                                          : "Furuseth",
    "fwlw License"                                                                              : "fwlw",
    "Gnome GCR Documentation License"                                                           : "GCR-docs",
    "GD License"                                                                                : "GD",
    "Generic XTS License"                                                                       : "generic-xts",
    "GNU Free Documentation License v1.1 only - invariants"                                     : "GFDL-1.1-invariants-only",
    "GNU Free Documentation License v1.1 or later - invariants"                                 : "GFDL-1.1-invariants-or-later",
    "GNU Free Documentation License v1.1 only - no invariants"                                  : "GFDL-1.1-no-invariants-only",
    "GNU Free Documentation License v1.1 or later - no invariants"                              : "GFDL-1.1-no-invariants-or-later",
    "GNU Free Documentation License v1.1 only"                                                  : "GFDL-1.1-only",
    "GNU Free Documentation License v1.1 or later"                                              : "GFDL-1.1-or-later",
    "GNU Free Documentation License v1.2 only - invariants"                                     : "GFDL-1.2-invariants-only",
    "GNU Free Documentation License v1.2 or later - invariants"                                 : "GFDL-1.2-invariants-or-later",
    "GNU Free Documentation License v1.2 only - no invariants"                                  : "GFDL-1.2-no-invariants-only",
    "GNU Free Documentation License v1.2 or later - no invariants"                              : "GFDL-1.2-no-invariants-or-later",
    "GNU Free Documentation License v1.2 only"                                                  : "GFDL-1.2-only",
    "GNU Free Documentation License v1.2 or later"                                              : "GFDL-1.2-or-later",
    "GNU Free Documentation License v1.3 only - invariants"                                     : "GFDL-1.3-invariants-only",
    "GNU Free Documentation License v1.3 or later - invariants"                                 : "GFDL-1.3-invariants-or-later",
    "GNU Free Documentation License v1.3 only - no invariants"                                  : "GFDL-1.3-no-invariants-only",
    "GNU Free Documentation License v1.3 or later - no invariants"                              : "GFDL-1.3-no-invariants-or-later",
    "GNU Free Documentation License v1.3 only"                                                  : "GFDL-1.3-only",
    "GNU Free Documentation License v1.3 or later"                                              : "GFDL-1.3-or-later",
    "Giftware License"                                                                          : "Giftware",
    "GL2PS License"                                                                             : "GL2PS",
    "3dfx Glide License"                                                                        : "Glide",
    "Glulxe License"                                                                            : "Glulxe",
    "Good Luck With That Public License"                                                        : "GLWTPL",
    "gnuplot License"                                                                           : "gnuplot",
    "GNU General Public License v1.0 only"                                                      : "GPL-1.0-only",
    "GNU General Public License v1.0 or later"                                                  : "GPL-1.0-or-later",
    "GNU General Public License v2.0 only"                                                      : "GPL-2.0-only",
    "GNU General Public License v2.0 or later"                                                  : "GPL-2.0-or-later",
    "GNU General Public License v3.0 only"                                                      : "GPL-3.0-only",
    "GNU General Public License v3.0 or later"                                                  : "GPL-3.0-or-later",
    "Graphics Gems License"                                                                     : "Graphics-Gems",
    "gSOAP Public License v1.3b"                                                                : "gSOAP-1.3b",
    "gtkbook License"                                                                           : "gtkbook",
    "Gutmann License"                                                                           : "Gutmann",
    "Haskell Language Report License"                                                           : "HaskellReport",
    "hdparm License"                                                                            : "hdparm",
    "HIDAPI License"                                                                            : "HIDAPI",
    "Hippocratic License 2.1"                                                                   : "Hippocratic-2.1",
    "Hewlett-Packard 1986 License"                                                              : "HP-1986",
    "Hewlett-Packard 1989 License"                                                              : "HP-1989",
    "Historical Permission Notice and Disclaimer"                                               : "HPND",
    "Historical Permission Notice and Disclaimer - DEC variant"                                 : "HPND-DEC",
    "Historical Permission Notice and Disclaimer - documentation variant"                       : "HPND-doc",
    "Historical Permission Notice and Disclaimer - documentation sell variant"                  : "HPND-doc-sell",
    "HPND with US Government export control warning"                                            : "HPND-export-US",
    "HPND with US Government export control warning and acknowledgment"                         : "HPND-export-US-acknowledgement",
    "HPND with US Government export control warning and modification rqmt"                      : "HPND-export-US-modify",
    "HPND with US Government export control and 2 disclaimers"                                  : "HPND-export2-US",
    "Historical Permission Notice and Disclaimer - Fenneberg-Livingston variant"                : "HPND-Fenneberg-Livingston",
    "Historical Permission Notice and Disclaimer    - INRIA-IMAG variant"                       : "HPND-INRIA-IMAG",
    "Historical Permission Notice and Disclaimer - Intel variant"                               : "HPND-Intel",
    "Historical Permission Notice and Disclaimer - Kevlin Henney variant"                       : "HPND-Kevlin-Henney",
    "Historical Permission Notice and Disclaimer - Markus Kuhn variant"                         : "HPND-Markus-Kuhn",
    "Historical Permission Notice and Disclaimer - merchantability variant"                     : "HPND-merchantability-variant",
    "Historical Permission Notice and Disclaimer with MIT disclaimer"                           : "HPND-MIT-disclaimer",
    "Historical Permission Notice and Disclaimer - Netrek variant"                              : "HPND-Netrek",
    "Historical Permission Notice and Disclaimer - Pbmplus variant"                             : "HPND-Pbmplus",
    "Historical Permission Notice and Disclaimer - sell xserver variant with MIT disclaimer"    : "HPND-sell-MIT-disclaimer-xserver",
    "Historical Permission Notice and Disclaimer - sell regexpr variant"                        : "HPND-sell-regexpr",
    "Historical Permission Notice and Disclaimer - sell variant"                                : "HPND-sell-variant",
    "HPND sell variant with MIT disclaimer"                                                     : "HPND-sell-variant-MIT-disclaimer",
    "HPND sell variant with MIT disclaimer - reverse"                                           : "HPND-sell-variant-MIT-disclaimer-rev",
    "Historical Permission Notice and Disclaimer - University of California variant"            : "HPND-UC",
    "Historical Permission Notice and Disclaimer - University of California, US export warning" : "HPND-UC-export-US",
    "HTML Tidy License"                                                                         : "HTMLTIDY",
    "IBM PowerPC Initialization and Boot Software"                                              : "IBM-pibs",
    "ICU License"                                                                               : "ICU",
    "IEC    Code Components End-user licence agreement"                                         : "IEC-Code-Components-EULA",
    "Independent JPEG Group License"                                                            : "IJG",
    "Independent JPEG Group License - short"                                                    : "IJG-short",
    "ImageMagick License"                                                                       : "ImageMagick",
    "iMatix Standard Function Library Agreement"                                                : "iMatix",
    "Imlib2 License"                                                                            : "Imlib2",
    "Info-ZIP License"                                                                          : "Info-ZIP",
    "Inner Net License v2.0"                                                                    : "Inner-Net-2.0",
    "Inno Setup License"                                                                        : "InnoSetup",
    "Intel Open Source License"                                                                 : "Intel",
    "Intel ACPI Software License Agreement"                                                     : "Intel-ACPI",
    "Interbase Public License v1.0"                                                             : "Interbase-1.0",
    "IPA Font License"                                                                          : "IPA",
    "IBM Public License v1.0"                                                                   : "IPL-1.0",
    "ISC License"                                                                               : "ISC",
    "ISC Veillard variant"                                                                      : "ISC-Veillard",
    "Jam License"                                                                               : "Jam",
    "JasPer License"                                                                            : "JasPer-2.0",
    "JPL Image Use Policy"                                                                      : "JPL-image",
    "Japan Network Information Center License"                                                  : "JPNIC",
    "JSON License"                                                                              : "JSON",
    "Kastrup License"                                                                           : "Kastrup",
    "Kazlib License"                                                                            : "Kazlib",
    "Knuth CTAN License"                                                                        : "Knuth-CTAN",
    "Licence Art Libre 1.2"                                                                     : "LAL-1.2",
    "Licence Art Libre 1.3"                                                                     : "LAL-1.3",
    "Latex2e License"                                                                           : "Latex2e",
    "Latex2e with translated notice permission"                                                 : "Latex2e-translated-notice",
    "Leptonica License"                                                                         : "Leptonica",
    "GNU Library General Public License v2 only"                                                : "LGPL-2.0-only",
    "GNU Library General Public License v2 or later"                                            : "LGPL-2.0-or-later",
    "GNU Lesser General Public License v2.1 only"                                               : "LGPL-2.1-only",
    "GNU Lesser General Public License v2.1 or later"                                           : "LGPL-2.1-or-later",
    "GNU Lesser General Public License v3.0 only"                                               : "LGPL-3.0-only",
    "GNU Lesser General Public License v3.0 or later"                                           : "LGPL-3.0-or-later",
    "Lesser General Public License For Linguistic Resources"                                    : "LGPLLR",
    "libpng License"                                                                            : "Libpng",
    "PNG Reference Library version 2"                                                           : "libpng-2.0",
    "libselinux public domain notice"                                                           : "libselinux-1.0",
    "libtiff License"                                                                           : "libtiff",
    "libutil David Nugent License"                                                              : "libutil-David-Nugent",
    "Licence Libre du QuÃ©bec â Permissive version 1.1"                                         : "LiLiQ-P-1.1",
    "Licence Libre du QuÃ©bec â RÃ©ciprocitÃ© version 1.1"                                      : "LiLiQ-R-1.1",
    "Licence Libre du QuÃ©bec â RÃ©ciprocitÃ© forte version 1.1"                                : "LiLiQ-Rplus-1.1",
    "Linux man-pages - 1 paragraph"                                                             : "Linux-man-pages-1-para",
    "Linux man-pages Copyleft"                                                                  : "Linux-man-pages-copyleft",
    "Linux man-pages Copyleft - 2 paragraphs"                                                   : "Linux-man-pages-copyleft-2-para",
    "Linux man-pages Copyleft Variant"                                                          : "Linux-man-pages-copyleft-var",
    "Linux Kernel Variant of OpenIB.org license"                                                : "Linux-OpenIB",
    "Common Lisp LOOP License"                                                                  : "LOOP",
    "LPD Documentation License"                                                                 : "LPD-document",
    "Lucent Public License Version 1.0"                                                         : "LPL-1.0",
    "Lucent Public License v1.02"                                                               : "LPL-1.02",
    "LaTeX Project Public License v1.0"                                                         : "LPPL-1.0",
    "LaTeX Project Public License v1.1"                                                         : "LPPL-1.1",
    "LaTeX Project Public License v1.2"                                                         : "LPPL-1.2",
    "LaTeX Project Public License v1.3a"                                                        : "LPPL-1.3a",
    "LaTeX Project Public License v1.3c"                                                        : "LPPL-1.3c",
    "lsof License"                                                                              : "lsof",
    "Lucida Bitmap Fonts License"                                                               : "Lucida-Bitmap-Fonts",
    "LZMA SDK License (versions 9.11 to 9.20)"                                                  : "LZMA-SDK-9.11-to-9.20",
    "LZMA SDK License (versions 9.22 and beyond)"                                               : "LZMA-SDK-9.22",
    "Mackerras 3-Clause License"                                                                : "Mackerras-3-Clause",
    "Mackerras 3-Clause - acknowledgment variant"                                               : "Mackerras-3-Clause-acknowledgment",
    "magaz License"                                                                             : "magaz",
    "mailprio License"                                                                          : "mailprio",
    "MakeIndex License"                                                                         : "MakeIndex",
    "Martin Birgmeier License"                                                                  : "Martin-Birgmeier",
    "McPhee Slideshow License"                                                                  : "McPhee-slideshow",
    "metamail License"                                                                          : "metamail",
    "Minpack License"                                                                           : "Minpack",
    "MIPS License"                                                                              : "MIPS",
    "The MirOS Licence"                                                                         : "MirOS",
    "MIT License"                                                                               : "MIT",
    "MIT No Attribution"                                                                        : "MIT-0",
    "Enlightenment License (e16)"                                                               : "MIT-advertising",
    "MIT Click License"                                                                         : "MIT-Click",
    "CMU License"                                                                               : "MIT-CMU",
    "enna License"                                                                              : "MIT-enna",
    "feh License"                                                                               : "MIT-feh",
    "MIT Festival Variant"                                                                      : "MIT-Festival",
    "MIT Khronos - old variant"                                                                 : "MIT-Khronos-old",
    "MIT License Modern Variant"                                                                : "MIT-Modern-Variant",
    "MIT Open Group variant"                                                                    : "MIT-open-group",
    "MIT testregex Variant"                                                                     : "MIT-testregex",
    "MIT Tom Wu Variant"                                                                        : "MIT-Wu",
    "MIT +no-false-attribs license"                                                             : "MITNFA",
    "MMIXware License"                                                                          : "MMIXware",
    "Motosoto License"                                                                          : "Motosoto",
    "MPEG Software Simulation"                                                                  : "MPEG-SSG",
    "mpi Permissive License"                                                                    : "mpi-permissive",
    "mpich2 License"                                                                            : "mpich2",
    "Mozilla Public License 1.0"                                                                : "MPL-1.0",
    "Mozilla Public License 1.1"                                                                : "MPL-1.1",
    "Mozilla Public License 2.0"                                                                : "MPL-2.0",
    "Mozilla Public License 2.0 (no copyleft exception)"                                        : "MPL-2.0-no-copyleft-exception",
    "mplus Font License"                                                                        : "mplus",
    "Microsoft Limited Public License"                                                          : "MS-LPL",
    "Microsoft Public License"                                                                  : "MS-PL",
    "Microsoft Reciprocal License"                                                              : "MS-RL",
    "Matrix Template Library License"                                                           : "MTLL",
    "Mulan Permissive Software License, Version 1"                                              : "MulanPSL-1.0",
    "Mulan Permissive Software License, Version 2"                                              : "MulanPSL-2.0",
    "Multics License"                                                                           : "Multics",
    "Mup License"                                                                               : "Mup",
    "Nara Institute of Science and Technology License (2003)"                                   : "NAIST-2003",
    "NASA Open Source Agreement 1.3"                                                            : "NASA-1.3",
    "Naumen Public License"                                                                     : "Naumen",
    "Net Boolean Public License v1"                                                             : "NBPL-1.0",
    "NCBI Public Domain Notice"                                                                 : "NCBI-PD",
    "Non-Commercial Government Licence"                                                         : "NCGL-UK-2.0",
    "NCL Source Code License"                                                                   : "NCL",
    "University of Illinois/NCSA Open Source License"                                           : "NCSA",
    "NetCDF license"                                                                            : "NetCDF",
    "Newsletr License"                                                                          : "Newsletr",
    "Nethack General Public License"                                                            : "NGPL",
    "NICTA Public Software License, Version 1.0"                                                : "NICTA-1.0",
    "NIST Public Domain Notice"                                                                 : "NIST-PD",
    "NIST Public Domain Notice with license fallback"                                           : "NIST-PD-fallback",
    "NIST Software License"                                                                     : "NIST-Software",
    "Norwegian Licence for Open Government Data (NLOD) 1.0"                                     : "NLOD-1.0",
    "Norwegian Licence for Open Government Data (NLOD) 2.0"                                     : "NLOD-2.0",
    "No Limit Public License"                                                                   : "NLPL",
    "Nokia Open Source License"                                                                 : "Nokia",
    "Netizen Open Source License"                                                               : "NOSL",
    "Noweb License"                                                                             : "Noweb",
    "Netscape Public License v1.0"                                                              : "NPL-1.0",
    "Netscape Public License v1.1"                                                              : "NPL-1.1",
    "Non-Profit Open Software License 3.0"                                                      : "NPOSL-3.0",
    "NRL License"                                                                               : "NRL",
    "NTP License"                                                                               : "NTP",
    "NTP No Attribution"                                                                        : "NTP-0",
    "Open Use of Data Agreement v1.0"                                                           : "O-UDA-1.0",
    "OAR License"                                                                               : "OAR",
    "Open CASCADE Technology Public License"                                                    : "OCCT-PL",
    "OCLC Research Public License 2.0"                                                          : "OCLC-2.0",
    "Open Data Commons Open Database License v1.0"                                              : "ODbL-1.0",
    "Open Data Commons Attribution License v1.0"                                                : "ODC-By-1.0",
    "OFFIS License"                                                                             : "OFFIS",
    "SIL Open Font License 1.0"                                                                 : "OFL-1.0",
    "SIL Open Font License 1.0 with no Reserved Font Name"                                      : "OFL-1.0-no-RFN",
    "SIL Open Font License 1.0 with Reserved Font Name"                                         : "OFL-1.0-RFN",
    "SIL Open Font License 1.1"                                                                 : "OFL-1.1",
    "SIL Open Font License 1.1 with no Reserved Font Name"                                      : "OFL-1.1-no-RFN",
    "SIL Open Font License 1.1 with Reserved Font Name"                                         : "OFL-1.1-RFN",
    "OGC Software License, Version 1.0"                                                         : "OGC-1.0",
    "Taiwan Open Government Data License, version 1.0"                                          : "OGDL-Taiwan-1.0",
    "Open Government Licence - Canada"                                                          : "OGL-Canada-2.0",
    "Open Government Licence v1.0"                                                              : "OGL-UK-1.0",
    "Open Government Licence v2.0"                                                              : "OGL-UK-2.0",
    "Open Government Licence v3.0"                                                              : "OGL-UK-3.0",
    "Open Group Test Suite License"                                                             : "OGTSL",
    "Open LDAP Public License v1.1"                                                             : "OLDAP-1.1",
    "Open LDAP Public License v1.2"                                                             : "OLDAP-1.2",
    "Open LDAP Public License v1.3"                                                             : "OLDAP-1.3",
    "Open LDAP Public License v1.4"                                                             : "OLDAP-1.4",
    "Open LDAP Public License v2.0 (or possibly 2.0A and 2.0B)"                                 : "OLDAP-2.0",
    "Open LDAP Public License v2.0.1"                                                           : "OLDAP-2.0.1",
    "Open LDAP Public License v2.1"                                                             : "OLDAP-2.1",
    "Open LDAP Public License v2.2"                                                             : "OLDAP-2.2",
    "Open LDAP Public License v2.2.1"                                                           : "OLDAP-2.2.1",
    "Open LDAP Public License 2.2.2"                                                            : "OLDAP-2.2.2",
    "Open LDAP Public License v2.3"                                                             : "OLDAP-2.3",
    "Open LDAP Public License v2.4"                                                             : "OLDAP-2.4",
    "Open LDAP Public License v2.5"                                                             : "OLDAP-2.5",
    "Open LDAP Public License v2.6"                                                             : "OLDAP-2.6",
    "Open LDAP Public License v2.7"                                                             : "OLDAP-2.7",
    "Open LDAP Public License v2.8"                                                             : "OLDAP-2.8",
    "Open Logistics Foundation License Version 1.3"                                             : "OLFL-1.3",
    "Open Market License"                                                                       : "OML",
    "OpenPBS v2.3 Software License"                                                             : "OpenPBS-2.3",
    "OpenSSL License"                                                                           : "OpenSSL",
    "OpenSSL License - standalone"                                                              : "OpenSSL-standalone",
    "OpenVision License"                                                                        : "OpenVision",
    "Open Public License v1.0"                                                                  : "OPL-1.0",
    "United    Kingdom Open Parliament Licence v3.0"                                            : "OPL-UK-3.0",
    "Open Publication License v1.0"                                                             : "OPUBL-1.0",
    "OSET Public License version 2.1"                                                           : "OSET-PL-2.1",
    "Open Software License 1.0"                                                                 : "OSL-1.0",
    "Open Software License 1.1"                                                                 : "OSL-1.1",
    "Open Software License 2.0"                                                                 : "OSL-2.0",
    "Open Software License 2.1"                                                                 : "OSL-2.1",
    "Open Software License 3.0"                                                                 : "OSL-3.0",
    "PADL License"                                                                              : "PADL",
    "The Parity Public License 6.0.0"                                                           : "Parity-6.0.0",
    "The Parity Public License 7.0.0"                                                           : "Parity-7.0.0",
    "Open Data Commons Public Domain Dedication & License 1.0"                                  : "PDDL-1.0",
    "PHP License v3.0"                                                                          : "PHP-3.0",
    "PHP License v3.01"                                                                         : "PHP-3.01",
    "Pixar License"                                                                             : "Pixar",
    "pkgconf License"                                                                           : "pkgconf",
    "Plexus Classworlds License"                                                                : "Plexus",
    "pnmstitch License"                                                                         : "pnmstitch",
    "PolyForm Noncommercial License 1.0.0"                                                      : "PolyForm-Noncommercial-1.0.0",
    "PolyForm Small Business License 1.0.0"                                                     : "PolyForm-Small-Business-1.0.0",
    "PostgreSQL License"                                                                        : "PostgreSQL",
    "Peer Production License"                                                                   : "PPL",
    "Python Software Foundation License 2.0"                                                    : "PSF-2.0",
    "psfrag License"                                                                            : "psfrag",
    "psutils License"                                                                           : "psutils",
    "Python License 2.0"                                                                        : "Python-2.0",
    "Python License 2.0.1"                                                                      : "Python-2.0.1",
    "Python ldap License"                                                                       : "python-ldap",
    "Qhull License"                                                                             : "Qhull",
    "Q Public License 1.0"                                                                      : "QPL-1.0",
    "Q Public License 1.0 - INRIA 2004 variant"                                                 : "QPL-1.0-INRIA-2004",
    "radvd License"                                                                             : "radvd",
    "Rdisc License"                                                                             : "Rdisc",
    "Red Hat eCos Public License v1.1"                                                          : "RHeCos-1.1",
    "Reciprocal Public License 1.1"                                                             : "RPL-1.1",
    "Reciprocal Public License 1.5"                                                             : "RPL-1.5",
    "RealNetworks Public Source License v1.0"                                                   : "RPSL-1.0",
    "RSA Message-Digest License"                                                                : "RSA-MD",
    "Ricoh Source Code Public License"                                                          : "RSCPL",
    "Ruby License"                                                                              : "Ruby",
    "Ruby pty extension license"                                                                : "Ruby-pty",
    "Sax Public Domain Notice"                                                                  : "SAX-PD",
    "Sax Public Domain Notice 2.0"                                                              : "SAX-PD-2.0",
    "Saxpath License"                                                                           : "Saxpath",
    "SCEA Shared Source License"                                                                : "SCEA",
    "Scheme Language Report License"                                                            : "SchemeReport",
    "Sendmail License"                                                                          : "Sendmail",
    "Sendmail License 8.23"                                                                     : "Sendmail-8.23",
    "Sendmail Open Source License v1.1"                                                         : "Sendmail-Open-Source-1.1",
    "SGI Free Software License B v1.0"                                                          : "SGI-B-1.0",
    "SGI Free Software License B v1.1"                                                          : "SGI-B-1.1",
    "SGI Free Software License B v2.0"                                                          : "SGI-B-2.0",
    "SGI OpenGL License"                                                                        : "SGI-OpenGL",
    "SGP4 Permission Notice"                                                                    : "SGP4",
    "Solderpad Hardware License v0.5"                                                           : "SHL-0.5",
    "Solderpad Hardware License, Version 0.51"                                                  : "SHL-0.51",
    "Simple Public License 2.0"                                                                 : "SimPL-2.0",
    "Sun Industry Standards Source License v1.1"                                                : "SISSL",
    "Sun Industry Standards Source License v1.2"                                                : "SISSL-1.2",
    "SL License"                                                                                : "SL",
    "Sleepycat License"                                                                         : "Sleepycat",
    "SMAIL General Public License"                                                              : "SMAIL-GPL",
    "Standard ML of New Jersey License"                                                         : "SMLNJ",
    "Secure Messaging Protocol Public License"                                                  : "SMPPL",
    "SNIA Public License 1.1"                                                                   : "SNIA",
    "snprintf License"                                                                          : "snprintf",
    "softSurfer License"                                                                        : "softSurfer",
    "Soundex License"                                                                           : "Soundex",
    "Spencer License 86"                                                                        : "Spencer-86",
    "Spencer License 94"                                                                        : "Spencer-94",
    "Spencer License 99"                                                                        : "Spencer-99",
    "Sun Public License v1.0"                                                                   : "SPL-1.0",
    "ssh-keyscan License"                                                                       : "ssh-keyscan",
    "SSH OpenSSH license"                                                                       : "SSH-OpenSSH",
    "SSH short notice"                                                                          : "SSH-short",
    "SSLeay License - standalone"                                                               : "SSLeay-standalone",
    "Server Side Public License, v 1"                                                           : "SSPL-1.0",
    "SugarCRM Public License v1.1.3"                                                            : "SugarCRM-1.1.3",
    "Sun PPP License"                                                                           : "Sun-PPP",
    "Sun PPP License (2000)"                                                                    : "Sun-PPP-2000",
    "SunPro License"                                                                            : "SunPro",
    "Scheme Widget Library (SWL) Software License Agreement"                                    : "SWL",
    "swrule License"                                                                            : "swrule",
    "Symlinks License"                                                                          : "Symlinks",
    "TAPR Open Hardware License v1.0"                                                           : "TAPR-OHL-1.0",
    "TCL/TK License"                                                                            : "TCL",
    "TCP Wrappers License"                                                                      : "TCP-wrappers",
    "TermReadKey License"                                                                       : "TermReadKey",
    "Transitive Grace Period Public Licence 1.0"                                                : "TGPPL-1.0",
    "ThirdEye License"                                                                          : "ThirdEye",
    "threeparttable License"                                                                    : "threeparttable",
    "TMate Open Source License"                                                                 : "TMate",
    "TORQUE v2.5+ Software License v1.1"                                                        : "TORQUE-1.1",
    "Trusster Open Source License"                                                              : "TOSL",
    "Time::ParseDate License"                                                                   : "TPDL",
    "THOR Public License 1.0"                                                                   : "TPL-1.0",
    "TrustedQSL License"                                                                        : "TrustedQSL",
    "Text-Tabs+Wrap License"                                                                    : "TTWL",
    "TTYP0 License"                                                                             : "TTYP0",
    "Technische Universitaet Berlin License 1.0"                                                : "TU-Berlin-1.0",
    "Technische Universitaet Berlin License 2.0"                                                : "TU-Berlin-2.0",
    "Ubuntu Font Licence v1.0"                                                                  : "Ubuntu-font-1.0",
    "UCAR License"                                                                              : "UCAR",
    "Upstream Compatibility License v1.0"                                                       : "UCL-1.0",
    "ulem License"                                                                              : "ulem",
    "Michigan/Merit Networks License"                                                           : "UMich-Merit",
    "Unicode License v3"                                                                        : "Unicode-3.0",
    "Unicode License Agreement - Data Files and Software (2015)"                                : "Unicode-DFS-2015",
    "Unicode License Agreement - Data Files and Software (2016)"                                : "Unicode-DFS-2016",
    "Unicode Terms of Use"                                                                      : "Unicode-TOU",
    "UnixCrypt License"                                                                         : "UnixCrypt",
    "The Unlicense"                                                                             : "Unlicense",
    "Universal Permissive License v1.0"                                                         : "UPL-1.0",
    "Utah Raster Toolkit Run Length Encoded License"                                            : "URT-RLE",
    "Vim License"                                                                               : "Vim",
    "VOSTROM Public License for Open Source"                                                    : "VOSTROM",
    "Vovida Software License v1.0"                                                              : "VSL-1.0",
    "W3C Software Notice and License (2002-12-31)"                                              : "W3C",
    "W3C Software Notice and License (1998-07-20)"                                              : "W3C-19980720",
    "W3C Software Notice and Document License (2015-05-13)"                                     : "W3C-20150513",
    "w3m License"                                                                               : "w3m",
    "Sybase Open Watcom Public License 1.0"                                                     : "Watcom-1.0",
    "Widget Workshop License"                                                                   : "Widget-Workshop",
    "Wsuipa License"                                                                            : "Wsuipa",
    "Do What The F*ck You Want To Public License"                                               : "WTFPL",
    "WWL License"                                                                               : "wwl",
    "X11 License"                                                                               : "X11",
    "X11 License Distribution Modification Variant"                                             : "X11-distribute-modifications-variant",
    "X11 swapped final paragraphs"                                                              : "X11-swapped",
    "Xdebug License v 1.03"                                                                     : "Xdebug-1.03",
    "Xerox License"                                                                             : "Xerox",
    "Xfig License"                                                                              : "Xfig",
    "XFree86 License 1.1"                                                                       : "XFree86-1.1",
    "xinetd License"                                                                            : "xinetd",
    "xkeyboard-config Zinoviev License"                                                         : "xkeyboard-config-Zinoviev",
    "xlock License"                                                                             : "xlock",
    "X.Net License"                                                                             : "Xnet",
    "XPP License"                                                                               : "xpp",
    "XSkat License"                                                                             : "XSkat",
    "xzoom License"                                                                             : "xzoom",
    "Yahoo! Public License v1.0"                                                                : "YPL-1.0",
    "Yahoo! Public License v1.1"                                                                : "YPL-1.1",
    "Zed License"                                                                               : "Zed",
    "Zeeff License"                                                                             : "Zeeff",
    "Zend License v2.0"                                                                         : "Zend-2.0",
    "Zimbra Public License v1.3"                                                                : "Zimbra-1.3",
    "Zimbra Public License v1.4"                                                                : "Zimbra-1.4",
    "zlib License"                                                                              : "Zlib",
    "zlib/libpng License with Acknowledgement"                                                  : "zlib-acknowledgement",
    "Zope Public License 1.1"                                                                   : "ZPL-1.1",
    "Zope Public License 2.0"                                                                   : "ZPL-2.0",
    "Zope Public License 2.1"                                                                   : "ZPL-2.1",
}

EXTENSION_TYPES = [
    "add-on",
    "theme",
]

ADDON_TAGS = [
    "3D View",
    "Add Curve",
    "Add Mesh",
    "Animation",
    "Bake",
    "Camera",
    "Compositing",
    "Development",
    "Game Engine",
    "Geometry Nodes",
    "Grease Pencil",
    "Import-Export",
    "Lighting",
    "Material",
    "Modeling",
    "Mesh",
    "Node",
    "Object",
    "Paint",
    "Pipeline",
    "Physics",
    "Render",
    "Rigging",
    "Scene",
    "Sculpt",
    "Sequencer",
    "System",
    "Text Editor",
    "Tracking",
    "User Interface",
    "UV",
]

THEME_TAGS = [
    "Dark",
    "Light",
    "Colorful",
    "Inspired By",
    "Print",
    "Accessibility",
    "High Contrast",
]

PLATFORMS = [
    "windows-x64",
    "macos-arm64",
    "linux-x64",
    "windows-arm64",
    "macos-x64"
]

PERMISSIONS = [
    "files",
    "network",
    "clipboard",
    "camera",
    "microphone",
]

PATH_EXCLUDE_PATTERNS = [
  "__pycache__/",
  "/.git/",
  "/*.zip",
]

########################•########################
"""                   UTILS                   """
########################•########################

def create_safe_name(name=""):
    name = name.strip()
    name = re.sub(r'[<>:"/\\|?*.]', '', name)
    name = re.sub(r'[\x00-\x1f\x7f]', '', name)
    name = name.replace(" ", "_")
    name = name[:255]
    return name


def get_file_extension(file_path):
    return Path(file_path).suffix.lower()

########################•########################
"""                 VALIDATORS                """
########################•########################

is_integer     = lambda item: isinstance(item, int)
is_string      = lambda item: isinstance(item, str) and bool(item.strip())
is_float       = lambda item: isinstance(item, float)
is_tuple       = lambda item: isinstance(item, tuple)
is_path        = lambda item: isinstance(item, (str, Path)) and Path(item).is_file()
is_dir         = lambda item: isinstance(item, (str, Path)) and Path(item).exists()
is_exe         = lambda item: is_path(item) and os.access(item, os.X_OK)
is_folder_name = lambda item: is_string(item) and item == create_safe_name(name=item)
is_file_name   = lambda item: is_string(item) and len(os.path.splitext(item)) == 2 and all(is_string(sub) for sub in os.path.splitext(item))
is_iterable    = lambda item: isinstance(item, Iterable) and not isinstance(item, (str, bytes))
is_all_strs    = lambda item: is_iterable(item) and all(is_string(sub) for sub in item)
is_ver_str     = lambda item: is_string(item) and len(item.split(".")) == 3 and all(sub.isdigit() for sub in item.split("."))
is_email       = lambda item: is_string(item) and bool(re.match(r"[^@]+@[^@]+\.[^@]+", item))
is_website     = lambda item: is_string(item) and bool(re.match(r'^(http[s]?://)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}(/[\w\-._~:/?#[\]@!$&\'()*+,;=]*)?$', item))

does_file_ext_match           = lambda file_path, file_ext : is_path(file_path) and is_string(file_ext) and get_file_extension(file_path) == file_ext.lower()
does_file_name_match_no_ext   = lambda file_path, file_name: is_path(file_path) and is_string(file_name) and Path(file_path).name == file_name
does_file_name_match_with_ext = lambda file_path, file_name: is_path(file_path) and is_file_name(file_name) and Path(file_path).name.lower() == file_name.lower()

########################•########################
"""                 DATA BASE                 """
########################•########################

DB = None

class DataBase:
    def __init__(self):
        # --- BLENDER --- #
        self.__blender_exe_path = None
        self.__blender_ver_min  = None
        self.__blender_ver_max  = None
        # --- DIRECTORIES --- #
        self.__src_dir   = None
        self.__build_dir = None
        # --- BUILD --- #
        self.__build_split_plats = None
        self.__build_verbose     = None
        # --- DEVELOPER --- #
        self.__dev_author = None
        self.__dev_email  = None
        # --- EXTENSION --- #
        self.__ext_id            = None
        self.__ext_name          = None
        self.__ext_type          = None
        self.__ext_tags          = None
        self.__ext_version       = None
        self.__ext_tag_line      = None
        self.__ext_website       = None
        self.__ext_licenses      = None
        self.__ext_copyright     = None
        self.__ext_platforms     = None
        self.__ext_wheels        = None
        self.__ext_permissions   = None
        self.__ext_path_includes = None
        self.__ext_path_excludes = None

    @property # IN -> String or Path || OUT -> Path
    def blender_exe_path(self):
        if is_exe(self.__blender_exe_path):
            return Path(self.__blender_exe_path)
        return None
    @blender_exe_path.setter
    def blender_exe_path(self, value):
        self.__blender_exe_path = None
        if is_exe(value):
            self.__blender_exe_path = Path(value)

    @property # IN -> (0,0,0) || OUT -> "0.0.0"
    def blender_ver_min(self):
        if is_iterable(self.__blender_ver_min):
            if len(self.__blender_ver_min) == 3:
                a, b, c = self.__blender_ver_min
                return f"{a}.{b}.{c}"
        return None
    @blender_ver_min.setter
    def blender_ver_min(self, value):
        self.__blender_ver_min = None
        if is_iterable(value):
            if len(value) == 3:
                if all(isinstance(item, int) for item in value):
                    self.__blender_ver_min = value

    @property # IN -> (0,0,0) || OUT -> "0.0.0"
    def blender_ver_max(self):
        if is_iterable(self.__blender_ver_max):
            if len(self.__blender_ver_max) == 3:
                a, b, c = self.__blender_ver_max
                return f"{a}.{b}.{c}"
        return None
    @blender_ver_max.setter
    def blender_ver_max(self, value):
        self.__blender_ver_max = None
        if is_iterable(value):
            if len(value) == 3:
                if all(isinstance(item, int) for item in value):
                    self.__blender_ver_max = value

    @property # IN -> String or Path || OUT -> Path
    def src_dir(self):
        if is_dir(self.__src_dir):
            return Path(self.__src_dir)
        return None
    @src_dir.setter
    def src_dir(self, value):
        self.__src_dir = None
        if is_dir(value):
            self.__src_dir = Path(value)

    @property # IN -> String or Path || OUT -> Path
    def build_dir(self):
        if is_dir(self.__build_dir):
            return Path(self.__build_dir)
        return None
    @build_dir.setter
    def build_dir(self, value):
        self.__build_dir = None
        if is_dir(value):
            self.__build_dir = Path(value)

    @property # IN -> self.ext_id & self.ext_version || OUT -> String
    def build_file_name(self):
        if self.ext_id:
            if self.ext_version:
                return f"{self.ext_id}-{self.ext_version}.zip"
        return None

    @property # IN -> Bool || OUT -> Bool
    def build_split_plats(self):
        return bool(self.__build_split_plats)
    @build_split_plats.setter
    def build_split_plats(self, value):
        self.__build_split_plats = None
        if isinstance(value, bool):
            self.__build_split_plats = value

    @property # IN -> Bool || OUT -> Bool
    def build_verbose(self):
        return bool(self.__build_verbose)
    @build_verbose.setter
    def build_verbose(self, value):
        self.__build_verbose = None
        if isinstance(value, bool):
            self.__build_verbose = value

    @property # OUT -> "0.0.0"
    def mani_schema_ver(self):
        return "1.0.0"

    @property # OUT -> String Filename w Extension
    def mani_file_name(self):
        return "blender_manifest.toml"

    @property # IN -> self.src_dir || OUT -> Path
    def mani_file_path(self):
        if self.src_dir:
            return self.src_dir.joinpath(self.mani_file_name)
        return None

    @property # IN -> String || OUT -> String
    def dev_author(self):
        if is_string(self.__dev_author):
            return self.__dev_author
        return None
    @dev_author.setter
    def dev_author(self, value):
        self.__dev_author = None
        if is_string(value):
            self.__dev_author = value

    @property # IN -> String || OUT -> String
    def dev_email(self):
        if is_string(self.__dev_email):
            return self.__dev_email
        return None
    @dev_email.setter
    def dev_email(self, value):
        self.__dev_email = None
        if is_email(value):
            self.__dev_email = value

    @property # IN -> String || OUT -> Safe String
    def ext_id(self):
        if is_string(self.__ext_id):
            return self.__ext_id
        return None
    @ext_id.setter
    def ext_id(self, value):
        self.__ext_id = None
        if is_string(value):
            name = create_safe_name(value)
            if name:
                self.__ext_id = name

    @property # IN -> String || OUT -> String
    def ext_name(self):
        if is_string(self.__ext_name):
            return self.__ext_name
        return None
    @ext_name.setter
    def ext_name(self, value):
        self.__ext_name = None
        if is_string(value):
            self.__ext_name = value

    @property # IN -> String || OUT -> String || EXTENSION_TYPES
    def ext_type(self):
        if is_string(self.__ext_type):
            if self.__ext_type in EXTENSION_TYPES:
                return self.__ext_type
        return None
    @ext_type.setter
    def ext_type(self, value):
        self.__ext_type = None
        if is_string(value):
            if value in EXTENSION_TYPES:
                self.__ext_type = value

    @property # IN -> self.ext_type [String,] || OUT -> [String,] || ADDON_TAGS or THEME_TAGS
    def ext_tags(self):
        if is_all_strs(self.__ext_tags):
            if self.ext_type == 'add-on':
                return [tag for tag in self.__ext_tags if tag in ADDON_TAGS]
            elif self.ext_type == 'theme':
                return [tag for tag in self.__ext_tags if tag in THEME_TAGS]
        return None
    @ext_tags.setter
    def ext_tags(self, value):
        self.__ext_tags = None
        if is_all_strs(value):
            if self.ext_type == 'add-on':
                self.__ext_tags = [tag for tag in value if tag in ADDON_TAGS]
            elif self.ext_type == 'theme':
                self.__ext_tags = [tag for tag in value if tag in THEME_TAGS]

    @property # IN -> (0,0,0) || OUT -> "0.0.0"
    def ext_version(self):
        if is_iterable(self.__ext_version):
            if len(self.__ext_version) == 3:
                a, b, c = self.__ext_version
                return f"{a}.{b}.{c}"
        return None
    @ext_version.setter
    def ext_version(self, value):
        self.__ext_version = None
        if is_iterable(value):
            if len(value) == 3:
                if all(isinstance(item, int) for item in value):
                    self.__ext_version = value

    @property # IN -> String || OUT -> String[:64]
    def ext_tag_line(self):
        if is_string(self.__ext_tag_line):
            return self.__ext_tag_line[:64]
        return None
    @ext_tag_line.setter
    def ext_tag_line(self, value):
        self.__ext_tag_line = None
        if is_string(value):
            self.__ext_tag_line = value

    @property # IN -> String || OUT -> String
    def ext_website(self):
        if is_website(self.__ext_website):
            return self.__ext_website
        return None
    @ext_website.setter
    def ext_website(self, value):
        self.__ext_website = None
        if is_website(value):
            self.__ext_website = value

    @property # IN -> [String,] || OUT -> [String,] || LICENSES
    def ext_licenses(self):
        if is_all_strs(self.__ext_licenses):
            return self.__ext_licenses
        return None
    @ext_licenses.setter
    def ext_licenses(self, value):
        self.__ext_licenses = None
        if is_all_strs(value):
            licenses = [item for item in value if item in LICENSES.keys()]
            if licenses:
                self.__ext_licenses = licenses

    @property # IN -> [(String Year, String Name),] || OUT -> [(String Year, String Name),]
    def ext_copyright(self):
        if is_iterable(self.__ext_copyright):
            return self.__ext_copyright
        return None
    @ext_copyright.setter
    def ext_copyright(self, value):
        self.__ext_copyright = None
        if is_iterable(value):
            for item in value:
                if len(item) == 2:
                    year, name = item
                    if is_string(year) and is_string(name):
                        if not isinstance(self.__ext_copyright, list):
                            self.__ext_copyright = []
                        self.__ext_copyright.append((year, name))

    @property # IN -> [(String Resource, String Reason),] || OUT -> [(String Resource, String Reason),] || PERMISSIONS
    def ext_permissions(self):
        if is_iterable(self.__ext_permissions):
            return self.__ext_permissions
        return None
    @ext_permissions.setter
    def ext_permissions(self, value):
        self.__ext_permissions = None
        if is_iterable(value):
            for item in value:
                if len(item) == 2:
                    resource, reason = item
                    if is_string(resource) and resource in PERMISSIONS and is_string(reason):
                        if not isinstance(self.__ext_permissions, list):
                            self.__ext_permissions = []
                        self.__ext_permissions.append((resource, reason))

    @property # IN -> [String Platform,] || OUT -> [String Platform,] || PLATFORMS
    def ext_platforms(self):
        if is_all_strs(self.__ext_platforms):
            return self.__ext_platforms
    @ext_platforms.setter
    def ext_platforms(self, value):
        self.__ext_platforms = None
        if is_all_strs(value):
            platforms = [item for item in value in item in PLATFORMS]
            if platforms:
                self.__ext_platforms = platforms

    @property # IN -> [String Wheel Path,] || OUT -> [String Wheel Path,]
    def ext_wheels(self):
        if is_all_strs(self.__ext_wheels):
            return self.__ext_wheels
        return None
    @ext_wheels.setter
    def ext_wheels(self, value):
        self.__ext_wheels = None
        if is_all_strs(value):
            self.__ext_wheels = value

    @property # IN -> [String Include Path,] || OUT -> [String Include Path,]
    def ext_path_includes(self):
        if is_all_strs(self.__ext_path_includes):
            return self.__ext_path_includes
        return None
    @ext_path_includes.setter
    def ext_path_includes(self, value):
        self.__ext_path_includes = None
        if is_all_strs(value):
            src_dir = self.src_dir
            if src_dir:
                include_paths = [item for item in value if is_path(src_dir.joinpath(item))]
                if include_paths:
                    self.__ext_path_includes = include_paths

    @property # IN -> [String Exclude Pattern,] || OUT -> [String Exclude Pattern,] || PATH_EXCLUDE_PATTERNS
    def ext_path_excludes(self):
        if is_all_strs(self.__ext_path_excludes):
            return self.__ext_path_excludes
        return None
    @ext_path_excludes.setter
    def ext_path_excludes(self, value):
        self.__ext_path_excludes = None
        if is_all_strs(value):
            excludes = [item for item in value if item in PATH_EXCLUDE_PATTERNS]
            if excludes:
                self.__ext_path_excludes = excludes


''' | Manifest File Layout
    |---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    | Blender                | DB                     | Required | Notes
    |---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    | schema_version         | mani_schema_ver        | O        | Internal version of the file format - use 1.0.0
    | maintainer             | dev_author <dev_email> | O        | Developer name <email@address.com>
    | id                     | ext_id                 | O        | Unique identifier for the extension
    | type                   | ext_type               | O        | “add-on” or “theme”
    | name                   | ext_name               | O        | Complete name of the extension
    | version                | ext_version            | O        | Version of the extension
    | tagline                | ext_tag_line           | O        | One-line short description, up to 64 characters - cannot end with punctuation
    | tags                   | ext_tags               | X        | Pick tags based on type
    | website                | ext_website            | X        | Website for the extension
    | license                | ext_licenses           | O        | List of licenses, use SPDX license identifier
    | copyright              | ext_copyright          | X        | Some licenses require a copyright, copyrights must be “Year Name” or “Year-Year Name”
    | blender_version_min    | blender_ver_min        | O        | Minimum supported Blender version - use at least 4.2.0
    | blender_version_max    | blender_ver_max        | X        | Blender version that the extension does not support, earlier versions are supported
    | permissions            | ext_permissions        | X        | Options : files, network, clipboard, camera, microphone. Each permission followed by explanation (short single-sentence, up to 64 characters, with no end punctuation)
    | platforms              | ext_platforms          | X        | List of supported platforms. If omitted, the extension will be available in all operating systems
    | wheels                 | ext_wheels             | X        | List of relative file-paths Python Wheels
    | paths                  | ext_path_includes      | X        | A list of file-paths relative to the manifest to include when building the package
    | paths_exclude_pattern  | ext_path_excludes      | X        | List of string, the pattern matching is compatible with gitignore
    |---------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''

########################•########################
"""                   FOLDERS                 """
########################•########################

def setup_build_folder():
    # Error : Requirements
    if not DB.validate_attributes(attrs=['EXT_ID', 'SRC_PARENT_DIR']):
        return False
    # Path
    DB.BUILD_FOLDER_NAME = create_safe_name(name=f"{DB.EXT_ID}_build")
    DB.BUILD_DIR = Path.joinpath(DB.SRC_PARENT_DIR, DB.BUILD_FOLDER_NAME)
    # Create
    if not DB.BUILD_DIR.exists():
        os.makedirs(DB.BUILD_DIR)
    # Error : Nonexistent
    if not DB.BUILD_DIR.exists():
        return False
    # Valid
    return True

########################•########################
"""                   FILES                   """
########################•########################

def write_manifest_file():
    # Error : Source Dir
    if not DB.validate_attributes(attrs=['SRC_DIR']):
        return False
    # Error : Required
    if not DB.validate_attributes(attrs=['MANI_SCHEMA_VER', 'DEV_AUTHOR', 'EXT_ID', 'EXT_TYPE', 'EXT_NAME', 'EXT_VERSION', 'EXT_TAG_LINE', 'EXT_LICENSES', 'BLENDER_VER_MIN']):
        return False
    # Mani File Path
    DB.MANI_FILE_PATH = Path.joinpath(DB.SRC_DIR, DB.MANI_FILE_NAME)
    # Write File Content
    with open(DB.MANI_FILE_PATH, "w") as file:
        write = file.write
        write(f'schema_version = "{DB.MANI_SCHEMA_VER}"\n')
        if DB.validate_attribute(attr='DEV_EMAIL'):
            write(f'maintainer = {DB.DEV_AUTHOR} <{DB.DEV_EMAIL}>\n')
        else:
            write(f'maintainer = {DB.DEV_AUTHOR}\n')
        write(f'id = "{DB.EXT_ID}"\n')
        write(f'type = "{DB.EXT_TYPE}"\n')
        write(f'name = "{DB.EXT_NAME}"\n')
        write(f'version = "{DB.EXT_VERSION}"\n')
        write(f'tagline = "{DB.EXT_TAG_LINE[:64]}"\n')
        if DB.validate_attributes(attrs=['EXT_ADDON_TAGS', 'EXT_THEME_TAGS']):
            tags = DB.EXT_ADDON_TAGS if DB.EXT_TYPE == 'add-on' else DB.EXT_THEME_TAGS
            write("tags = [\n")
            for item in tags:
                write(f'\t"{item}",\n')
            write("]\n")
        if DB.validate_attribute(attr='EXT_WEBSITE'):
            add(f'website = "{DB.EXT_WEBSITE}"')
        write("license = [\n")
        for item in DB.EXT_LICENSES:
            write(f'\t"{item}",\n')
        write("]\n")
        if DB.EXT_COPYRIGHT and DB.validate_attribute(attr='EXT_COPYRIGHT'):
            write("copyright = [\n")
            for item in DB.EXT_COPYRIGHT:
                write(f'\t"{item}",\n')
            write("]\n")
        write(f'blender_version_min = "{DB.BLENDER_VER_MIN}"\n')
        if DB.validate_attribute(attr='BLENDER_VER_MAX'):
            write(f'blender_version_max = "{DB.BLENDER_VER_MAX}"\n')
        if any(bool(reason_msg) for reason_msg in DB.EXT_PERMISSIONS.values()):
            write('[permissions]\n')
            for permission_type, reason_msg in DB.EXT_PERMISSIONS.items():
                if reason_msg:
                    write(f'{permission_type} = "{reason_msg}"\n')
        if DB.EXT_PLATFORMS and DB.validate_attribute(attr='EXT_PLATFORMS'):
            write("platforms = [\n")
            for item in DB.EXT_PLATFORMS:
                write(f'\t"{item}",\n')
            write("]\n")
        if DB.EXT_WHEELS and DB.validate_attribute(attr='EXT_WHEELS'):
            write("wheels = [\n")
            for item in DB.EXT_WHEELS:
                write(f'\t"{item}",\n')
            write("]\n")
        if DB.EXT_PATH_INCLUDES and DB.validate_attribute(attr='EXT_PATH_INCLUDES'):
            write("[build]")
            write("paths = [\n")
            for item in DB.EXT_PATH_INCLUDES:
                write(f'\t"{item}",\n')
            write("]\n")
        elif DB.EXT_PATH_EXCLUDES and DB.validate_attribute(attr='EXT_PATH_EXCLUDES'):
            write("[build]")
            write("paths_exclude_pattern = [\n")
            for item in DB.EXT_PATH_EXCLUDES:
                write(f'\t"{item}",\n')
            write("]\n")
    # Error : Mani File
    if not is_path(DB.MANI_FILE_PATH):
        return False
    # Valid
    return True

########################•########################
"""                  COMMANDS                 """
########################•########################

def validate_manifest():
    # Error : Requirements
    if not DB.validate_attributes(attrs=['BLENDER_EXE_PATH', 'SRC_DIR']):
        return False

    command = [
        DB.BLENDER_EXE_PATH,
        "--command", "extension validate",
        DB.SRC_DIR,
    ]
    try:
        completed_process = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Command succeeded with output: {completed_process.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Return code: {e.returncode}")
        print(f"Standard Output: {e.stdout}")
        print(f"Standard Error: {e.stderr}")


def build_extension():
    # Error : Requirements
    if not DB.validate_attributes(attrs=['BLENDER_EXE_PATH', 'SRC_DIR', 'BUILD_DIR']):
        return False

    command = [
        DB.BLENDER_EXE_PATH,
        "--command", "extension build",
        "--source-dir", DB.SRC_DIR,
        "--output-dir", DB.BUILD_DIR,
        "--output-filepath", f"{DB.EXT_ID}-{DB.EXT_VERSION}.zip",
        "--valid-tags", "",
    ]
    if DB.BUILD_SPLIT_PLATS:
        command.append("--split-platforms")
    if DB.BUILD_VERBOSE:
        command.append("--verbose")
    try:
        completed_process = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Command succeeded with output: {completed_process.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Return code: {e.returncode}")
        print(f"Standard Output: {e.stdout}")
        print(f"Standard Error: {e.stderr}")

########################•########################
"""                 INTERFACES                """
########################•########################

class VerController:
    def __init__(self, parent, label="Version", min_ver=(0,0,0), add_use_check=False):
        self.frame = tk.Frame(parent, padx=2, pady=2, borderwidth=1, relief="solid")
        self.frame.pack(fill=tk.X)

        self.var_major = tk.IntVar(value=min_ver[0])
        self.var_minor = tk.IntVar(value=min_ver[1])
        self.var_patch = tk.IntVar(value=min_ver[2])
        self.var_use   = None
        if add_use_check:
            self.var_use = tk.BooleanVar(value=False)

        self.label = tk.Label(self.frame, text=label)
        self.spin_major = tk.Spinbox(self.frame, from_=min_ver[0], to=sys.maxsize, textvariable=self.var_major, width=5)
        self.spin_minor = tk.Spinbox(self.frame, from_=min_ver[1], to=sys.maxsize, textvariable=self.var_minor, width=5)
        self.spin_patch = tk.Spinbox(self.frame, from_=min_ver[2], to=sys.maxsize, textvariable=self.var_patch, width=5)
        self.check_box = None
        if add_use_check:
            self.check_box = tk.Checkbutton(self.frame, text='Use', variable=self.var_use, command=self.com_check_box, width=5)

        self.label.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        if add_use_check:
            self.check_box.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        else:
            self.spin_major.pack(side=tk.LEFT, expand=False, fill=tk.BOTH)
            self.spin_minor.pack(side=tk.LEFT, expand=False, fill=tk.BOTH)
            self.spin_patch.pack(side=tk.LEFT, expand=False, fill=tk.BOTH)


    def com_check_box(self):
        if self.var_use.get():
            print("TRUE")
            self.spin_major.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
            self.spin_minor.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
            self.spin_patch.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        else:
            print("FALSE")
            self.spin_major.pack_forget()
            self.spin_minor.pack_forget()
            self.spin_patch.pack_forget()


    def get_version(self):
        # Check box is not used
        if self.check_box and self.var_use and not self.var_use.get():
            return None
        # Valid
        return (self.var_major.get(), self.var_minor.get(), self.var_patch.get())

########################•########################
"""                    APP                    """
########################•########################

class App:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.Y)

        # Versions
        self.ext_ver     = VerController(self.frame, label="Extension Version")
        self.b3d_ver_min = VerController(self.frame, label="Blender Min Version", min_ver=(4,2,0))
        self.b3d_ver_max = VerController(self.frame, label="Blender Max Version", min_ver=(4,2,0), add_use_check=True)

    #     # Preview
    #     self.preview_button = ttk.Button(self.frame, text="Preview", command=self.display_preview)
    #     self.preview_button.pack(pady=10)
    #     self.output_label = ttk.Label(self.frame, text="Selected Versions:")
    #     self.output_label.pack()


    # def display_preview(self):
    #     versions = f"Version 1: {self.ver1.get_version()}\nVersion 2: {self.ver2.get_version()}"
    #     self.output_label.config(text=versions)

########################•########################
"""                 CALLBACKS                 """
########################•########################

def select_folder(folder_path):
    folder = filedialog.askdirectory()
    if folder:
        folder_path.set(folder)


def build(version_vars):
    version = "{} . {} . {}".format(*[var.get() for var in version_vars])
    messagebox.showinfo("Build", f"Extension build process started!\nVersion: {version}")

########################•########################
"""                APPLICATION                """
########################•########################

if __name__ == "__main__":
    DB = DataBase()
    root = tk.Tk()
    root.title("Blender Extension Creator")
    root.geometry("400x600")
    root.resizable(False, False)
    app = App(root)
    root.mainloop()
