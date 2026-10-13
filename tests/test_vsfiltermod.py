#!/usr/bin/env python3
"""Functional tests for the VSFilterMod VapourSynth interface (API 4).

Usage: python tests/test_vsfiltermod.py [path/to/VSFilterMod.dll]

Without an argument the plugin is expected to be autoloaded (e.g. from the
installed wheel) or to be found in site-packages/vapoursynth/plugins.

Requires the vapoursynth Python module (R55 or newer) and Windows.
"""
import glob
import hashlib
import os
import sys

import vapoursynth as vs

core = vs.core
HERE = os.path.dirname(os.path.abspath(__file__))
ASS = os.path.join(HERE, "vmoe-tags.ass")


def load_plugin(args):
    if args:
        core.std.LoadPlugin(args[0])
        return
    if hasattr(core, "vsfm"):
        return
    plugin_dir = os.path.join(os.path.dirname(vs.__file__), "plugins")
    for path in glob.glob(os.path.join(plugin_dir, "**", "VSFilterMod.dll"), recursive=True):
        core.std.LoadPlugin(path)
        return
    raise SystemExit("FAIL: vsfm plugin is neither autoloaded nor found below " + plugin_dir)


def check(cond, msg):
    if not cond:
        raise SystemExit("FAIL: " + msg)
    print("ok  ", msg)


def expect_error(fn, msg, contains=""):
    try:
        fn()
    except vs.Error as e:
        text = str(e).strip().splitlines()[-1]
        check(contains in text, "%s (%s)" % (msg, text))
    else:
        raise SystemExit("FAIL: no error raised: " + msg)


def digest(clip, n):
    f = clip.get_frame(n)
    h = hashlib.sha1()
    for p in range(clip.format.num_planes):
        h.update(bytes(f[p]))
    return h.hexdigest()


def main():
    load_plugin(sys.argv[1:])
    check(hasattr(core, "vsfm"), "plugin loaded (namespace vsfm)")

    # vmoe-tags.ass at 24 fps: one sample per second, frame 12 + 24 * k.
    for fmt in (vs.YUV420P8, vs.YUV420P10, vs.YUV420P16, vs.RGB24):
        src = core.std.BlankClip(width=640, height=360, length=384, fpsnum=24, fpsden=1, format=fmt,
                                 color=[32, 128, 128] if fmt == vs.YUV420P8 else None)
        out = core.vsfm.TextSubMod(src, file=ASS)
        name = core.get_video_format(fmt).name
        check(out.format.id == src.format.id and out.num_frames == 384, "%s: format and length kept" % name)
        check(digest(out, 12) != digest(src, 12), "%s: subtitles rendered" % name)

    src = core.std.BlankClip(width=640, height=360, length=384, fpsnum=24, fpsden=1, format=vs.YUV420P8, color=[32, 128, 128])
    out = core.vsfm.TextSubMod(src, file=ASS)
    check(digest(out, 12) != digest(out, 36), "Vmoe \\ortho0 and \\ortho1 render differently")
    check(digest(out, 60) != digest(out, 84), "Vmoe \\xblur and \\yblur render differently")
    blends = {digest(out, n) for n in (252, 276, 300, 324, 348, 372)}
    check(len(blends) == 6, "Vmoe \\blend: six modes, six different frames")
    accurate = core.vsfm.TextSubMod(src.resize.Point(format=vs.YUV420P16), file=ASS, accurate=1)
    check(digest(accurate, 12) != digest(src.resize.Point(format=vs.YUV420P16), 12), "YUV420P16 with accurate=1 rendered")

    expect_error(lambda: core.vsfm.TextSubMod(src.resize.Point(format=vs.YUV444P8), file=ASS), "YUV444P8 rejected", "only constant format")
    expect_error(lambda: core.vsfm.TextSubMod(src, file=os.path.join(HERE, "missing.ass")), "missing subtitle file rejected", "can't open")
    expect_error(lambda: core.vsfm.VobSub(src, file=os.path.join(HERE, "missing.idx")), "missing VobSub file rejected", "can't open")

    print("all tests passed")


if __name__ == "__main__":
    main()
