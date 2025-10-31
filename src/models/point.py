from dataclasses import dataclass
from typing import Optional


@dataclass
class SectionPoint:
    code: str
    pcode: str
    cdistance: float
    ele: float
    lgtd: float
    lttd: float
    order_no: int
    coeff: Optional[float] = None
    moditime: Optional[str] = None
    
    def to_dict(self):
        return {
            'code': self.code,
            'pcode': self.pcode,
            'cdistance': self.cdistance,
            'ele': self.ele,
            'lgtd': self.lgtd,
            'lttd': self.lttd,
            'orderNo': self.order_no,
            'coeff': self.coeff,
            'moditime': self.moditime
        }


@dataclass
class HSectionPoint(SectionPoint):
    def to_dict(self):
        data = super().to_dict()
        data['hecd'] = data.pop('code')
        return data


@dataclass
class VSectionPoint(SectionPoint):
    pname: Optional[str] = None
    channel: Optional[str] = None
    bele: Optional[float] = None
    cltype: Optional[str] = None
    
    def to_dict(self):
        data = super().to_dict()
        data['vecd'] = data.pop('code')
        data['pname'] = data.pop('pcode')
        data.update({
            'channel': self.channel,
            'bele': self.bele,
            'cltype': self.cltype
        })
        return data
