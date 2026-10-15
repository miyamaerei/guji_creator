# -*- coding: utf-8 -*-
"""临时包装：把 _part_grp5.py 片段接入 gen_gap01.py 的 build(g) 以跑校验。
跑完即删，不属于交付物。"""


def build(g):
    E = g["E"]; RULE = g["RULE"]; EVT = g["EVT"]; APPT = g["APPT"]; REL = g["REL"]
    CIT = g["CIT"]; OPN = g["OPN"]; MING = g["MING"]; ERA = g["ERA"]
    TME = g["TME"]; REG2 = g["REG2"]; add = g["add"]; rid = g["rid"]; tid = g["tid"]
    V = "01"
    ents = []
    _flushed = [0]

    def go():
        add("ents", V, ents[_flushed[0]:])
        _flushed[0] = len(ents)

__FRAGMENT__
