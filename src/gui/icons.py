
#----------------------------------------------------------------------
# ICONS
import wx
from wx.lib.embeddedimage import PyEmbeddedImage as PEI

DARKMODE = False
icon_r = 230
icon_g = 230
icon_b = 230


class PyEmbeddedImage(PEI):
    def __init__(self, data):
        super().__init__(data)

    def GetBitmap(self, use_theme=True, resize=None):
        image = PEI.GetImage(self)
        if DARKMODE and use_theme:
            image.Replace(0, 0, 0, icon_r, icon_g, icon_b)
        if resize is not None:
            image = image.Scale(*resize)
        return wx.Bitmap(image)

icon_UR = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAAAXNSR0IArs4c6QAAAARnQU1B'
    b'AACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAAGYktHRAD/AP8A/6C9p5MAAAAHdElN'
    b'RQfhBw0DMQ8FIsIwAAABaUlEQVQ4T82TO4vCQBSFzy5YRCOEICIEAhZpFP+Avyq1pT/FNp2d'
    b'hUkRsbH2VSipRFF8FSq+rjPDoAnswg4I7gdDDmfC4d6bmy9i4I18y+fb+B+Bm80Gv01KKXAw'
    b'GKBSqcA0TTiOg263K29ijEYjWi6XdL1eqd/v03a7pePxKPThcKD9fi/05XKhUqnEy3qeQqFA'
    b'p9OJf9cn0HWd6vU6rVYr8VKj0aBeryd0GIbkeZ7Qw+HwGRQ/vKA4aLfbNJlM6Hw+U6vVotls'
    b'RrvdTmg2K1osFkLzam3bToQZhiG6icOH+2c6nQ7lcjkRls1mqdlsypsXyovNZokoimBZFtLp'
    b'tHRfKK/NfD6H67oYj8fSSaIcyBti88b9fpdOks//y9PpFOVy+eelZigHapqGarUKtjLSSfL5'
    b'ltmfgUwmA9/3pZNEOZAtNmq1GorFonSSKLd8u92wXq/FDFOplHRfKFfIFzqfzyMIAunEAR5b'
    b'Qz1TAK0tXAAAAABJRU5ErkJggg==')

icon_up = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAAAXNSR0IArs4c6QAAAARnQU1B'
    b'AACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAAGYktHRAD/AP8A/6C9p5MAAAAHdElN'
    b'RQfhBh4SKDBKbF6TAAAAsklEQVQ4T+2TwQ3DIAxFTXdgD1ZhAhCLMRJ7MAQURxRRsF2k5tBD'
    b'n/QV5JiXw1dUbcAHYoyAayGEPhFAIUcppaaU8INX8IwzCVGYcx6yV3AmIQq11psQZxKs0BhT'
    b'lVKbEGf4joMUeu830RrnXN9+ZxO2RkkBFdxdGcK10dOszQ8h1ehp5uaHkGr0NHPzl5Br9DRz'
    b'82CtZZeoOYZ7hy72X26X+omGuQaP/ryNv/B7fl0I8ASb6RkI5xlSYwAAAABJRU5ErkJggg==')

icon_UL = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAAAXNSR0IArs4c6QAAAARnQU1B'
    b'AACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAAGYktHRAD/AP8A/6C9p5MAAAAHdElN'
    b'RQfhBw0DNzTic4ySAAABbklEQVQ4T72UvYrCQBSFZxe1kEQsLKzS2ImPYZXnyKP4DL5EOjsL'
    b'O60idsEfUNCAoIJRwf8kZzN3r2DWLCSs7AdDhjOXM/fezMwHQsQb+eTv2/gfw+v1Ksbjsbhc'
    b'LqykQPbwmV6vh3K5LPuKYrGIVqvFK8mIGAZBgEqlQmaPoaoqjscjBoMB+v0+xclNbdumeafT'
    b'wWw2w+12Q7vdjhput9uI2WNMJhPouo56vU5x1WoVhmHQPJ/Po9FoYL1ef8eT+kStVouYlUol'
    b'2n2xWGA+n1PMdDrFcrmk+XA4xGazged5lPWLoRRlBtJM0zR0u11eScaLoeR+v9POp9OJleTE'
    b'GlLqYYayyWmJNTwcDjBNE6vVipXkxB7sTCYjwrMocrkcKylg4whvL/l8PsOyLOz3e1aS8+td'
    b'Dv+yCG8IKylg4wh/KTn2gfV9X+x2O1EoFEQ2m2U1GbElu64rms2mcByHlRRQnj8YjUZQFIVe'
    b'knQAX2UyeADJo3o0AAAAAElFTkSuQmCC')

icon_right = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAAAXNSR0IArs4c6QAAAARnQU1B'
    b'AACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAAGYktHRAD/AP8A/6C9p5MAAAAHdElN'
    b'RQfhBh4SKDBKbF6TAAAArElEQVQ4T8WVjQ2FIAyE4e3AHqzCBDAZjMQeDEEfTY5EYw0/IfFL'
    b'LmJbL2K1KhrgnMNqjqGhUoqstTgbM2WotSZjDJVSqNaKjMyU4VU5Z2Rklg1ZKSVkn2wZskII'
    b'qLjTcvIFXfz8pDhLalaLy8UzkprV4nLxqnqzNAJHiDGqH9ZHwI6ft7+jvuW2lgtmtNWU5dcG'
    b'x1ckI5b3HhV3vv/0jgyH4+Pr6IBd+wUQ/QG28O4GJuoU/AAAAABJRU5ErkJggg==')

icon_LR = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAAAXNSR0IArs4c6QAAAARnQU1B'
    b'AACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAAGYktHRAD/AP8A/6C9p5MAAAAHdElN'
    b'RQfhBw0DNxTZHaxaAAABdUlEQVQ4T62UP6rCQBDG5z0LwSgEtLCSgJXiMaxyDs/gCXISj2Bn'
    b'ISmMnaQL/gEFLUJQ0CAoopJ5u8PE5wZBF/zBwvIxfDszzA6gJsPhEIvFIs5mM1ZUfkETy7Kg'
    b'2+1CuVxmReVHuvL9I263GxyPRzBNE3K5HKv/aGfoui5UKhWYz+esZKDCNQjDEHu9HsZxzIqK'
    b'doaGYUCj0YB8Ps9KBjb+mMFgIHuOQRCwoqJteDgccDQa4fl8ZkVFu+Tr9QpRFMH9fmclAxt/'
    b'zNdLlqVOp1MU88iKipah53lYq9Uow2az+TJLkKLoB+52O3pZImdtuVzSfb1e42azQdE7FANN'
    b'ZulptVoU84zQAbfbLTqOg4VCgcROp0MZSNrtNtq2jYvFQjFLz36/p7gUkE2Wr69WK9okEpn1'
    b'eDym+2QyQd/38XQ6YalUUszq9TomSUJxKVo97Pf7KJYCmVWr1cejz2hvm8vlAqKvtMZefT9t'
    b'w3do/5R3fNkQ4A8hbi5O82i8ZgAAAABJRU5ErkJggg==')


icon_LL = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAAAXNSR0IArs4c6QAAAARnQU1B'
    b'AACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAAGYktHRAD/AP8A/6C9p5MAAAAHdElN'
    b'RQfhBw0DNyNhoAlVAAABbUlEQVQ4T72UvarCQBCFJwmxkAiJWFiJkE7yGj5KXsTHSGlrZ2dh'
    b'5U8jllGbNKIJohC1UFFhbnbuKOayxYoXP9jscEIOM2zOAkro9XoIABiGISvqaOKRfZzjdrvB'
    b'fr+HcrkMhmGwqobOe47VagVBEECapqy8AfX5h36/j8ViEefzOSvqSEf+BOnIs9kMfN+HJElY'
    b'UUdqKA5kPB7D+XxmRZ3vjDydTqHZbMJyuWRFHamhrutQKBRA0zRW1JGOfDqdYL1eQ71eB9M0'
    b'WVVEGL7S7XaxVCpR9CqVCg6HQ36jRs4wO1W0bZvMHqtWq2HWMeV7s9lglh6qD4cDxnFM9fV6'
    b'xSiKKBA5w8VikTN7LJEYsXc6HRwMBlRPJhNst9tU73Y7bLVaaFlW3vByuWC1Wn0aidVoNDC7'
    b'LOjmOR6P1K2oxTTZ/0r1/X7H7Xb72xB7PRmNRui6Lpl5nvf2FSY9ZSGJtDiOw4o630nKJ/yz'
    b'IcAPUHwS0OLE48IAAAAASUVORK5CYII=')

icon_left = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAAAXNSR0IArs4c6QAAAARnQU1B'
    b'AACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAAGYktHRAD/AP8A/6C9p5MAAAAHdElN'
    b'RQfhBh4SKDBKbF6TAAAAmklEQVQ4T62VgQ3AEBBF6Q72sIoJWEyMZA9DuLqmEmlPr9V7yQ+J'
    b'n584HAUfcM6dszmvA621oBRvf3TUWqGUAsYY0Fr/D8w5HyGjOKaOlNItbDnQe0+GoThujl58'
    b'Sr2Oj8IQqvjLwkCq+MuKMdILi9raFtsoiPiWMVD8UEZErs2VEAJtbuKYOkSfXke0OSDi7WtE'
    b'pMFe4b8AgB2kL/31Q2vxXgAAAABJRU5ErkJggg==')

icon_down = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAAAAACo4kLRAAAACXBIWXMAAAsTAAALEwEAmpwY'
    b'AAAAB3RJTUUH4QgSAAc7JebJsQAAAGhJREFUGNPFzsENgCAMheFXd2APVnECdTEdiT0Ygt9D'
    b'IdDEuz21X5q8Z0iSTD5+bfqYf1H72tM6kS1+WUaQIiYQ1IgVBK2sVhoI4Jn2QEeOYScTewXL'
    b'rOgVEhFrDw7YigcDYIyM266xvsSUaE4W9c7bAAAAAElFTkSuQmCC')

icon_CC = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAAAXNSR0IArs4c6QAAAARnQU1B'
    b'AACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAAGYktHRAD/AP8A/6C9p5MAAAAHdElN'
    b'RQfhBw4CFDvfEiO7AAABsElEQVQ4T62VvYrCUBCFT9aoYOWD+AYKlha2gq0gNmKnIlgLWoj4'
    b'AorvYC02WggWIghWWgtWiv8/d++dzAajSXaV/eASZhIn5849EzUhwT/yxdePUXo2mw1HXFAl'
    b'c7kcms0mJd+hWCwiGo3idDpRbCq83W7QNI2j31EiDocDkskkMpkM/H6/ecNCuVwWlUqFI2cK'
    b'hYIIh8PifD5zxsDSQxljt9uRWjculwvi8TgSiQS8Xi9nGaPuK9Vq1VZpqVQSsVhMXK9XzljR'
    b'ue4L6/WalM5mM7RaLepvKpVCJBJBMBiEx+PhJ5/gwrZMp1Mhm618SkvXdcq54erDdrtt2kEh'
    b't4lOp8ORPa4F37GRCSu1Rfbv7S07znK9XsdisUA2m6Vt3u93pNNpLJdLDAYD1Go1ftKK4ymr'
    b'fgUCAYRCISr+Q7fbxWQygTQ0fD4fZx8gnQ80Gg3ymhvKg/1+X8g5FlI5Zw1eDmW1WmG/39PU'
    b'OKE8qFQOh0Mcj0fOMkZdIeSXhpbi+a1OqDkejUYin8+bvzEVzudzWoq/2kXN8Xg8Rq/Xw3a7'
    b'pZx5ynz5yHuPB/TPfwHAN0ixPaqOEC/nAAAAAElFTkSuQmCC')

icons8_fantasy_50 = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAABmJLR0QA/wD/AP+gvaeTAAAE"
    b"70lEQVRogc3Za4hVVRQH8N/MpIVRoVZkDTUfggqLHn4ow6BQw0J6IPYCbUhTZ3ylidHLHtS3"
    b"oj5UUlAgRUlKlJEaFdHL6kNZJFlRaQ8ijfxQpviYuX3Y+3DO3HvPnfuc8Q+He+7ea++z/mev"
    b"vdba63BkYOZwK9AMHIu/MaaRSdqbo0tDmCmQuGa4FWkUH6KAt4ZbkXI4BUdVIXcm+gUiBzC6"
    b"3ge2yrRG4hvcqjKhbrRlxlw7yLzHYC5Oa1C/mvCS8KZ/wCx0FPW349co84LK5nUSHsAuvN0K"
    b"ZSvhfKnZFLAdN0ut4Eop0bE4qNS8zsaz2JeZ55Ih0L0EmzMKJNc2wVOtjf/vibIb4/9uXI43"
    b"0Vc0dtgcwuSowG4swM9Fih1GZ5Ttjm37M/378Xq878eEoVO9FF9EReZiRPzdGds2Z+RGC6ZV"
    b"wB+4T9gbj8e214ZM4xzcJN0jyf4YKazQ1UWyT2B27IdThf3Rh/Narukg6MCPApnB3Gsxnonj"
    b"Xmm2UrWiA1dgi6DQxzWM7ZKa2sVN16wKdAibfLXg97Ob+zuMw3S8j++xRrrhs3gyM25flLus"
    b"xbobIcSF5/CXUnf7IM6Nso8W9RewB5eWmfN6weUezshuxwqc3GwS47G1jHJbcWGR7COx7xDm"
    b"4Sy8Edv2CrlXOXRildTbJbnZOlylNGuoG+2YKmzKbBzYg6cEQg9JY8eNmbEdeDH2rcmZfxx6"
    b"8J6BL6sPH2FGs4hkMQaL8ZXSVTqMW8qMGR/7v860nYFlgoPIRvhDeBe9gnseEkzAT9K3NytH"
    b"7u4osyHTlqxSEuE3CNF/bIt0rYj7pSS6c2R6hPSjz0CvdEEce9AQp+3FuFdKYk6OTK9Aol8g"
    b"VHw+SvbEshbpOCgSU+kXvFM5LDSQxIlCUrkIR0eZ6XGeHao7cTYVy6UkFubIzJOSSGSWSffE"
    b"LtyFUfg2tg1pyWiFlMTiHJnF0gPX1kz7ttj2i5TQ7/gk3m9pjcqlSFaigE+Vrwcska7Ewfh7"
    b"uhDVC/hNMKEZgisudt8TW8oA8w10lQU8byCZLIkerI9yy6Vn9ocz8m1CipKNR6+2ksRtgmfq"
    b"x1JMwr8GkllaRIIQ3ZMguDfO0VVm/jZchy+FYFhOpmHMyZDoybRnyXymlAShVPqf9G1nT4vl"
    b"0CacZ2Y3Q/Es8kgkmCQ1szyZdVIiw1LIHowEwZwqkSAonxQnRubItAxzDU4iSTsquWFCnNiL"
    b"x5qpYDWolcQdVcy5Fuc0RbsqcbvaSCytct68w1SCTuWPwnUhuyfy0o4s0TwSx+GGGp+9Ssii"
    b"G0Y2L2p0JXrweQ3PbheOtzs1+OWgVhJLKsw1UaiiFOKYUVU8f5rUPU+rTuVSNIvEKLysNG/a"
    b"IRyeKiFJYwrxvmbMVxuJSi42Qa0r0iVUSvridUCN6UnWxVazsSuZUzF6hZQlD+2YIiSHSZVx"
    b"IzZJixfvCIG04kFrgdpWYlG1DCKOF4raxShXt+qLBC6K1yYDqyk745hOBnqCBULRmLASq3NI"
    b"PB3vlwg1q1rwjxAAW4bJaluJPJNrFO2Cd1ovNa1NUtM6EPumyXHHybfuFTkPGAoSxehSx2bf"
    b"LRA5oUxflkRvk5SsFjW73+T7xcqi9uEkQR0BcapU4ZXC97w7Db5vWo26UpQkfmSjbz0uttmo"
    b"K2mcjA/wp1AFn9JkpepBU9P4Ix7/A6+u1m3fs0SBAAAAAElFTkSuQmCC"
)

#----------------------------------------------------------------------
