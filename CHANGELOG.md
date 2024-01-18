# Revision history for `pandocfilters`

-  v1.5.1
   - Don't raise an error if the directory used to store images already exists (#104, Augusto Zanellato).

-  v1.5.0: Last release supporting Python 2.
   - Added an environment variable `PANDOCFILTER_CLEANUP` that when `get_filename4code` is used, temporary directory will be cleaned up automatically. See #88.
   - `examples/` is no longer included in the distribution (i.e. source distribution or binary wheels found on PyPI.) This should be a backward compatible change as `examples/` is never exposed as a Python module, nor entry points.
   - Added a couple of examples.
   - See more in <https://github.com/jgm/pandocfilters/compare/1.4.3...1.5.0>.
