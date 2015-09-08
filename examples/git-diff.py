#!/usr/bin/env python3

"""
    Pandoc filter to process a code block with class "git-diff" to present the
    diff of a file between two commits.

    class variables:
    * dir:          Directory from (optional, defaults to ".")
    * objects:      Which object in `dir` (optional defaults to ".")
    * commit-range: commitrange (like: "HEAD..v1.0", optional, defaults to HEAD)
    * diffoptions:  git diff options (like: -U0, optional, defaults to "")

    Example: (git -C /devel/jog diff ..23fe4 -- README.md)
    ```{.git-diff commit-range="..23fe4" dir="/devel/jog" object="README.md"}

    Example: (git diff ..v1.0)
    ```{.git-diff commit-range="..v1.0"}

    Example:
    ```{.git-diff commit-range="..v1.0" objects="README.md src/u src/c" diffoptions="-U0"}
    """

from pandocfilters import toJSONFilter, RawBlock, CodeBlock
import subprocess;

def gitdiff(key, value, format, meta):
    if key == "CodeBlock":
        [[ident, classes, keyvals], contents] = value
        if "git-diff" in classes:
            folder = "."
            commra = ""
            obj = ""
            objdiv = ""
            options = ""

            # its a diff - view
            if not "diff" in classes:
                classes.append("diff")

            for el in keyvals:
                if "commit-range" in el:
                    commra = el[1]

                if "dir" in el:
                    folder = el[1]

                if "objects" in el or "object" in el:
                    objdiv = "--"
                    obj = "%s %s" % (obj, el[1])

                if "diffoptions" == el[0]:
                    options = el[1]

            command_string = "git -C %s diff %s %s %s %s" % (folder, options, commra, objdiv, obj)
            out = ""
            try:
                l = list(filter(None, command_string.split(" ")))
                out = subprocess.check_output(l)
            except subprocess.CalledProcessError as err:
                return None

            if out != None or out != "":
                out = out.decode("utf-8");
                return [CodeBlock([ident, classes, keyvals], out), CodeBlock([ident, classes, keyvals], contents)]
            else:
                return None

if __name__ == "__main__":
    toJSONFilter(gitdiff)

