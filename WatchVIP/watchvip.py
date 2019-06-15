#! python3

from vip import *
import argparse


# 默认解析接口
toolUrl = [
    'https://660e.com/?url=',
    'https://jx.618g.com/index.php?url='
]

def run():
    """
        视频网址
        爱奇艺视频网址应该是搜索后得到页面的网址，其以src=search结尾，否则会找不到相应元素
    """
    parse = argparse.ArgumentParser(
        prog='watchvip',
        description='watch vip videos'
    )
    parse.add_argument(
        '-u',
        '--url',
        nargs=1,
        default=[''],
        metavar='url',
        help='video url'
    )
    parse.add_argument(
        '-p',
        '--previous',
        action='store_true',
        dest='is_prev',
        default=False,
        help='use previous url. Please specify a value of 0 for the url'
    )
    parse.add_argument(
        '-a',
        '--all',
        action='store_true',
        dest='is_all',
        default=False,
        help='show all videos url, default show vip videos url'
    )
    parse.add_argument(
        '-l',
        '--list',
        action='store_true',
        dest='is_list',
        default=False,
        help='show used url caches'
    )
    parse.add_argument(
        '-T',
        '--ToolUrl',
        nargs=1,
        default=toolUrl,
        metavar='tool',
        help='tool url'
    )

    args = parse.parse_args()

    if len(sys.argv) == 1:
        sys.exit()


    try:
        v = vipurl(args)
        v.play()
    except Exception as exc:
        log.error(exc)

if __name__ == "__main__":
    run()