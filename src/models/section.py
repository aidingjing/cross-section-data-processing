from dataclasses import dataclass
from typing import Optional


@dataclass
class SectionSurface:
    code: str
    number: Optional[str] = None
    channel: Optional[str] = None
    address: Optional[str] = None
    dmidentit: Optional[str] = None
    adcd: Optional[str] = None
    coeff: Optional[float] = None
    moditime: Optional[str] = None
    
    def to_dict(self):
        return {
            'code': self.code,
            'number': self.number,
            'channel': self.channel,
            'address': self.address,
            'dmidentit': self.dmidentit,
            'adcd': self.adcd,
            'coeff': self.coeff,
            'moditime': self.moditime
        }


@dataclass
class HSectionSurface(SectionSurface):
    vecd: Optional[str] = None
    
    def to_dict(self):
        data = super().to_dict()
        data['hecd'] = data.pop('code')
        data['vecd'] = self.vecd
        return data


@dataclass
class VSectionSurface(SectionSurface):
    cele: Optional[float] = None
    clgtd: Optional[float] = None
    clttd: Optional[float] = None
    sele: Optional[float] = None
    slgtd: Optional[float] = None
    elttd: Optional[float] = None
    eletype: Optional[str] = None
    method: Optional[str] = None
    
    def to_dict(self):
        data = super().to_dict()
        data['vecd'] = data.pop('code')
        data.update({
            'cele': self.cele,
            'clgtd': self.clgtd,
            'clttd': self.clttd,
            'sele': self.sele,
            'slgtd': self.slgtd,
            'elttd': self.elttd,
            'eletype': self.eletype,
            'method': self.method
        })
        return data
