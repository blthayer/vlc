import argparse
import dataclasses


@dataclasses.dataclass
class RTSPConnection:
    """Data needed for an RTSP Connection."""

    user: str
    password: str
    ip: str


@dataclasses.dataclass
class DisplayInfo:
    """Information about the display."""

    width: int
    height: int


SUBTYPE = {"main": 0, "sub": 1}


def main(
    connection_info: RTSPConnection,
    channels: list[int],
    display_info: DisplayInfo,
    subtype: int,
):
    # Very crude: split screen by number of channels.
    n = len(channels)
    w = display_info.width / n
    h = display_info.height / n

    vlm = ""
    for channel in channels:
        ch = f"ch{channel}"
        vlm += (
            f"new {ch} broadcast enabled\n"
            #
            f'setup {ch} input "rtsp://{connection_info.user}"'
            f":{connection_info.password}@{connection_info.ip}"
            f"/cam/realmonitor?channel={channel}&subtype={subtype}\n"
            #
            f"setup {ch} output #mosaic-bridge{{id={ch},width={w},"
            f"height={h}}}\n\n"
        )

    # TODO: Background file, automagically.
    TODO = "TODO: Background file, automagically"
    vlm += (
        "new mosaic broadcast enabled\n"
        f'setup mosaic input "file:///{TODO}"\n'
        "setup mosaic option image-duration=-1"
        "setup mosaic output #transcode{sfilter=mosaic{"
        f"width={display_info.width},height={display_info.height},"
        # TODO: cols, rows, order, aspect, picture, align, vcodec, etc.
        f""
    )


# new mosaic broadcast enabled
# setup mosaic input "file:///home/bthayer/vlc/bg.png"
# setup mosaic option image-duration=-1
# setup mosaic output #transcode{sfilter=mosaic{width=2560,height=1440,cols=2,rows=2,order="ch1,ch2,ch3,ch4",keep-aspect-ratio=enabled,keep-picture=1,mosaic-align=5},vcodec=mp4v}:bridge-in:display
#
# control mosaic play
# control ch1 play
# control ch2 play
# control ch3 play
# control ch4 play


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("user", help="User for RTSP connection.")
    parser.add_argument("password", help="Password for RTSP connection.")
    parser.add_argument("ip", help="IP address of RTSP server to connect to.")
    parser.add_argument(
        "channels", help='Comma seperated list of channels, e.g. "1,2,3,4"'
    )
    parser.add_argument(
        "subtype",
        help=f"Stream subtype (integer): {SUBTYPE}",
        type=int,
        default=1,
    )
    parser.add_argument(
        "display_width", help="Width of display in pixels", type=int
    )
    parser.add_argument(
        "display_height", help="Height of display in pixels", type=int
    )

    main()
