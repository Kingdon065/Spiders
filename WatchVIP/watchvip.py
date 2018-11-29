#! python3

from vip import *
import time, os
import argparse

def run():
    """
        视频网址
        爱奇艺视频网址应该是搜索后得到页面的网址，其以src=search结尾，否则会找不到相应元素
    """
    parse = argparse.ArgumentParser(
        prog='watchvip',
        description='watch vip videos',

    )
    parse.add_argument(
        'root',
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

    args = parse.parse_args()

    path = 'D:/Tools/watchvip_caches'
    filename = os.path.join(path, 'url_temp.txt')

    if args.is_list:
        os.system('cat {}'.format(filename))
        return

    if args.is_prev:
        try:
            f = open(filename, 'r')
            lines = f.readlines()
            n = len(lines)
            while True:
                args.root = lines[n - 1][23:-1]
                if args.root[0:4] == 'http':
                    break
                else:
                    n = n -1
            f.close()
        except Exception as exc:
            log.error(exc)
            return

    # 备份videoUrl
    os.makedirs(path, exist_ok=True)
    temp = open(filename, 'a+')
    localtime = time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
    temp.write('{} -- {}\n'.format(localtime, args.root))
    temp.close()

    # 工具网站
    toolUrl = 'http://app.baiyug.cn:2019/vip/?url='
    try:
        v = vipurl(args, toolUrl)
        v.title()
        v.get_address()
        v.play()
    except Exception as exc:
        log.error(exc)

if __name__ == "__main__":
    run()