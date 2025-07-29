# -*- coding:utf-8 -*-
# @author  : Yurnu
# @time    : 2025-7-27
# @function: 实现mc颜色符号和ANSI码的转换


color_to_ansi: dict[str, str] ={
        "§0": "\033[30m",  # 黑色 / Black
        "§1": "\033[34m",  # 深蓝 / Dark Blue
        "§2": "\033[32m",  # 深绿 / Dark Green
        "§3": "\033[36m",  # 深青 / Dark Aqua
        "§4": "\033[31m",  # 深红 / Dark Red
        "§5": "\033[35m",  # 深紫 / Dark Purple
        "§6": "\033[33m",  # 金色 / Gold
        "§7": "\033[37m",  # 灰色 / Gray
        "§8": "\033[90m",  # 深灰 / Dark Gray
        "§9": "\033[94m",  # 蓝色 / Blue
        "§a": "\033[92m",  # 绿色 / Green
        "§b": "\033[96m",  # 青色 / Aqua
        "§c": "\033[91m",  # 红色 / Red
        "§d": "\033[95m",  # 紫色 / Light Purple
        "§e": "\033[93m",  # 黄色 / Yellow
        "§f": "\033[97m",  # 白色 / White
        "§r": "\033[0m",   # 重置 / Reset
        "§l": "\033[1m",   # 加粗 / Bold
        "§n": "\033[4m",   # 下划线 / Underline
        "§o": "\033[3m",   # 斜体 / Italic
        "§m": "\033[9m",   # 删除线 / Strikethrough
} # 21
text_to_color: dict[str, str] = {
    "black": "§0",
    "dark_blue": "§1",
    "dark_green": "§2",
    "dark_aqua": "§3",
    "dark_red": "§4",
    "dark_purple": "§5",
    "gold": "§6",
    "gray": "§7",
    "dark_gray": "§8",
    "blue": "§9",
    "green": "§a",
    "aqua": "§b",
    "red": "§c",
    "purple": "§d",
    "yellow": "§e",
    "white": "§f",
    "reset": "§r",
    "bold": "§l",
    "underline": "§n",
    "italic": "§o",
    "strikethrough": "§m"
}
class Color:
    # 在一个字符串中 把MC里的颜色符号全换成ANSI 并返回字符串
    @staticmethod
    def textToANSICoded(mc_text: str):
        coded_text = mc_text
        for k, v in color_to_ansi.items():
            coded_text = coded_text.replace(k, v)
        return coded_text

    # 在一个字符串中 把ANSI全换成MC里的颜色符号 并返回字符串
    @staticmethod
    def ANSICodedToMinecraftColored(ansi_text):
        colored_text = ansi_text
        for k, v in color_to_ansi.items():
            colored_text = colored_text.replace(v, k)
        return colored_text
    
    # 把颜色的英语换成mc里的颜色符号
    @staticmethod
    def getMinecraftColorCode(color_text: str):
        if color_text in text_to_color:
            return text_to_color[color_text]