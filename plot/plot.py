__author__ = 'Tyrion'

import pylab as pl


def set_chinese():
    from pylab import mpl
    mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题


def plot_figure(fun, x, y, pic_name, pic_folder, x_label, y_label, color='blue', marker_size=3, line_width=2):
    set_chinese()
    pl.xlabel(x_label)
    pl.ylabel(y_label)
    fun(x, y, 'o', color=color, markersize=marker_size, linewidth=line_width)
    pl.show()
    pl.savefig(pic_folder + pic_name)
