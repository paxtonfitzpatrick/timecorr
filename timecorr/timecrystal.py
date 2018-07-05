import numpy as np
import pandas as pd
import time


class TimeCrystal(object):


    def __init__(self, data=None, corr=None, meta=None, date_created=None):

        self.time_data = data
        self.meta = meta
        if self.meta is None:
            self.meta = {}
        if date_created is None:
            self.date_created = time.strftime("%c")
        else:
            self.date_created = date_created
        self.corr = corr

    def get_data(self):
        return self.time_data

    def get_corr(self):#, mode='within', weights_function=gaussian_weights,
        #weights_params=gaussian_params, cfun=isfc):
        #from .timecorr import timecorr as tc #cannot import globally because format_data in timecorr.py imports TimeCrystal

        if not (self.corr is None):
            return self.corr
        else:
            raise Exception('correlations have not yet been mined')

            #self.corr = tc(self.get_data(), mode=mode,
            #                     weights_function=weights_function,
            #                     weights_params=weights_params,
            #                     cfun=cfun)
            #return self.corr

    def info(self):
        print(f'Date created: {self.date_created}')
        print(f'Meta data: {self.meta}')

    def timecorr(self, **kwargs):

        from .timecorr import timecorr as tc
        from .helpers import _is_empty

        self.corr = tc(self.get_data(), **kwargs)

        if not _is_empty(kwargs):
            self.meta = kwargs
        # else:
        #     self.meta = {'mode': tc.__defaults__[2]}

    def levelup(self, **kwargs):

        from .timecorr import levelup as lu
        from .helpers import _is_empty

        self.time_data = lu(self.get_data(),**kwargs)

        if not _is_empty(kwargs):
            self.meta = kwargs

    def save(self, fname):
        np.savez(fname, data=self.time_data, corr=self.corr, meta=self.meta, date_created=self.date_created)


def load(fname):
    tc = np.load(fname, mmap_mode='r')
    return TimeCrystal(data=tc['data'], corr=tc['corr'], meta=tc['meta'], date_created=tc['date_created'])
