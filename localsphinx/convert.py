import contextlib
import os
import shutil
import tempfile

from sphinx.websupport import WebSupport

@contextlib.contextmanager
def mkdtemp(suffix='', prefix='tmp', parent_dir=None):
    path = tempfile.mkdtemp(suffix, prefix, parent_dir)
    try:
        yield unicode(path)
    finally:
        shutil.rmtree(path, ignore_errors=True)

def magic_convert_function(text):
    with mkdtemp() as outdir:
        with mkdtemp() as indir:
            shutil.copy('conf.py', indir)
            with open(os.path.join(indir, 'index.rst'), 'w') as infile:
                infile.write(text)

            support = WebSupport(srcdir=indir,
                                 builddir=outdir)
            print "Building Sphinx at %s & %s" % (indir, outdir)
            print "Current dir: %s" % os.listdir(indir)
            support.build()
            contents = support.get_document('index')
            return contents['body']
