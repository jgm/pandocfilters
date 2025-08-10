#!/usr/bin/env python

"""
Pandoc filter to process code blocks with class "plantuml" into
plant-generated images.

Needs `plantuml.jar` from http://plantuml.com/.

The environment variable 'PANDOCFILTER_plantuml_jar_file' can be
set to /path/to/jar-file if the file does not reside in the current
working directory.

Other environment variables prefixed with 'PANDOCFILTER_plantuml_'
are passed down to the execution depending on if it is a system property (with -D) or an argument (with -P)
, e.g.
* export PANDOCFILTER_plantuml_include_dir="-Dplantuml.include.path=\"/path/to/include/\""
would add the system property `-Dplantuml.include.path=/path/to/include`
* export PANDOCFILTER_plantuml_layout_smetana="-Playout=smetana" would add the argument
the argument `-Playout=smetana`

Environment variables having values not starting with -P or -D are not passed down to execution.
"""

import os
import sys
from subprocess import call

from pandocfilters import toJSONFilter, Para, Image, get_filename4code, get_caption, get_extension


def plantuml(key, value, format, _):
    if key == 'CodeBlock':
        [[ident, classes, keyvals], code] = value

        if "plantuml" in classes:
            caption, typef, keyvals = get_caption(keyvals)

            filename = get_filename4code("plantuml", code)
            filetype = get_extension(format, "png", html="svg", latex="eps")

            src = filename + '.uml'
            dest = filename + '.' + filetype

            if not os.path.isfile(dest):
                if not code.startswith("@start"):
                    code = "@startuml\n" + code + "\n@enduml\n"
                with open(src, "w") as f:
                    f.write(code)

                # read extra arguments from environment starting with "PANDOCFILTER_plantuml" if any
                plantuml_extra_args_dash_d = list()
                plantuml_extra_args_dash_p = list()
                all_envs = os.environ
                for k, v in all_envs.items():
                    if k.startswith("PANDOCFILTER_plantuml") and k != "PANDOCFILTER_plantuml_jar_file":
                        if v.startswith("-P"):
                            plantuml_extra_args_dash_p += [f'{item}' for item in v.split()]
                        elif v.startswith("-D"):
                            plantuml_extra_args_dash_d += [f'{item}' for item in v.split()]
                        else:
                            sys.stderr.write('Did not add ' + k + '=' + os.environ.get(k) + ' to execution\n')
                call_arguments_dash_p = ", ".join(plantuml_extra_args_dash_p)
                call_arguments_dash_d = ", ".join(plantuml_extra_args_dash_d)

                if len(call_arguments_dash_p + call_arguments_dash_d) > 0:
                    call(["java",
                        call_arguments_dash_d,
                        "-jar",
                        os.environ.get("PANDOCFILTER_plantuml_jar_file", "plantuml.jar"),
                        call_arguments_dash_p,
                        "-t"+filetype,
                        src])
                    sys.stderr.write('Used extra arguments ' + str(call_arguments_dash_d) + " " + str(call_arguments_dash_p)  + '\n')
                else:
                    call(["java",
                        "-jar",
                        os.environ.get("PANDOCFILTER_plantuml_jar_file", "plantuml.jar"),
                        "-t"+filetype,
                        src])
                if "PANDOCFILTER_plantuml_jar_file" in os.environ.keys(): # is this really needed?
                    sys.stderr.write('Used jar file ' + os.environ.get("PANDOCFILTER_plantuml_jar_file") + '\n')
                sys.stderr.write('Created image ' + dest + '\n')

            return Para([Image([ident, [], keyvals], caption, [dest, typef])])

if __name__ == "__main__":
    toJSONFilter(plantuml)
