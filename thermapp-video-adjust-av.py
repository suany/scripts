import av, os, sys  # pip3 install av

# TODO TODO TODO TODO TODO TODO TODO TODO
#
# This PyAV version seems to work pretty well.
#
# TODO 1: Copy audio stream also
# TODO 2: Although I set the output bit_rate to the same as input, the
#         actual output bit_rate is slightly lower, though still better
#         than default. Figure out how to fix this.
#
# TODO TODO TODO TODO TODO TODO TODO TODO

WIDTH = 384
HEIGHT = 288
BADCOL = 163

def image_edit_frame(img):
    for y in range(0, HEIGHT-1):
        img.putpixel((BADCOL, y), img.getpixel((BADCOL, y+1)))
    return img

def video_edit_frames(infile, outfile):
    in_av = av.open(infile)
    out_av = av.open(outfile, 'w')

    in_vstream = in_av.streams.video[0]

    codec_name = in_vstream.codec_context.name
    # Of several ways to get frame rate, this one works for TAPlus output
    fps = in_vstream.average_rate
    out_vstream = out_av.add_stream(codec_name, fps)
    out_vstream.width = in_vstream.codec_context.width
    out_vstream.height = in_vstream.codec_context.height
    out_vstream.pix_fmt = in_vstream.codec_context.pix_fmt
    # This does change output bitrate from default, but the actually produced
    # bitrate is lower than specified, though still higher than default.
    out_vstream.bit_rate = in_vstream.codec_context.bit_rate

    print("codec", codec_name)
    print("frame rate", fps)
    print("width", out_vstream.width)
    print("height", out_vstream.height)
    print("pix_fmt", out_vstream.pix_fmt)
    print("bit_rate", out_vstream.bit_rate)

    if out_vstream.width != WIDTH or out_vstream.height != HEIGHT:
        print("ERROR: input video dimensions not as expected")
        return False


    " DOES NOT WORK: select low crf for high quality (but larger file size)."
    #out_vstream.options = {'crf': '24'}


    for frame in in_av.decode(in_vstream):
        in_img = frame.to_image()
        out_img = image_edit_frame(in_img)
        out_frame = av.VideoFrame.from_image(out_img)
        out_packet = out_vstream.encode(out_frame)  # Encode video frame
        # "Mux" the encoded frame (add the encoded frame to MP4 file).
        out_av.mux(out_packet)

#   # Copy audio also - is this how to do it? - DOES NOT WORK
#   in_astream = in_av.streams.audio[0]
#   out_astream = out_av.add_stream(template = in_astream)
#   for packet in in_av.demux(in_astream):
#       if packet.dts is None:
#           continue
#       packet.stream = out_astream
#       out_av.mux(packet)

    # Flush the encoder
    out_packet = out_vstream.encode(None)
    out_av.mux(out_packet)

    in_av.close()
    out_av.close()

    return True

if __name__ == "__main__":
    if len(sys.argv) == 3:
        infile = sys.argv[1]
        outfile = sys.argv[2]
    elif len(sys.argv) == 2:
        infile = sys.argv[1]
        base, ext = os.path.splitext(infile)
        outfile = base + "-avadj" + ext
    else:
        print("USAGE: thermapp-video-adjust infile outfile")
        sys.exit(1)
    if not os.path.exists(infile):
        print("ERROR: infile does not exist:", infile)
        sys.exit(1)
    if os.path.exists(outfile):
        print("WARNING: outfile exists:", outfile)
        if not input("Overwrite? [y/N]") in ('y', 'Y'):
            sys.exit(1)
    video_edit_frames(infile, outfile)
