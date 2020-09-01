brand_rule_aishi = {
    1: {'S': '固态电容SolidCapacitor'},
    2: {'A0': 'A0',
        'A1': 'A1',
        'A2': 'A2'
        },
    3: {'0B': '电压编码Voltage Code(W.V) 2',
        '0E': '电压编码Voltage Code(W.V) 2.5',
        '0G': '电压编码Voltage Code(W.V) 4',
        '0J': '电压编码Voltage Code(W.V) 6.3',
        '0Q': '电压编码Voltage Code(W.V) 7',
        '1A': '电压编码Voltage Code(W.V) 10',
        '1C': '电压编码Voltage Code(W.V) 16',
        '1E': '电压编码Voltage Code(W.V) 25',
        '1V': '电压编码Voltage Code(W.V) 35',
        '1H': '电压编码Voltage Code(W.V) 50',
        },
    4: {
        'Y': '电容公差Capacitance -25～+20',
        'K': '电容公差Capacitance -10～+10',
        'M': '电容公差Capacitance -20～+20',
        'Q': '电容公差Capacitance -10～+30',
        'V': '电容公差Capacitance -10～+20',
        'A': '电容公差Capacitance -0～+20',
        'C': '电容公差Capacitance -5～+20',
        'J': '电容公差Capacitance +6～+20',
        'B': '电容公差Capacitance -10～-20',
        'W': '电容公差Capacitance -15～+15',
        'G': '电容公差Capacitance -15～+20',
        'L': '电容公差Capacitance -35～+10'},
    5: {
        '4R7': '电容量Capacitance (uF ) 4.7',
        '100': '电容量Capacitance (uF ) 10',
        '150': '电容量Capacitance (uF ) 15',
        '220': '电容量Capacitance (uF ) 22',
        '330': '电容量Capacitance (uF ) 33',
        '470': '电容量Capacitance (uF ) 47',
        '680': '电容量Capacitance (uF ) 68',
        '820': '电容量Capacitance (uF ) 82',
        '101': '电容量Capacitance (uF ) 100',
        '151': '电容量Capacitance (uF ) 150',
        '181': '电容量Capacitance (uF ) 180',
        '201': '电容量Capacitance (uF ) 200',
        '221': '电容量Capacitance (uF ) 220',
        '331': '电容量Capacitance (uF ) 330',
        '471': '电容量Capacitance (uF ) 470',
        '561': '电容量Capacitance (uF ) 560'},
    6: {
        'A09': '7.3×4.3 (L×Wmm) 0.9高度T(mm)',
        'A19': '7.3×4.3 (L×Wmm) 1.9高度T(mm)',
        'A28': '7.3×4.3 (L×Wmm) 2.8高度T(mm)'},
    7: {
        'R04': '4.0 E.S.R(mΩ)',
        'R06': '6.0 E.S.R(mΩ)',
        'R07': '7.0 E.S.R(mΩ)',
        'R09': '9.0 E.S.R(mΩ)',
        'RA0': '100 E.S.R(mΩ)',
        'RA2': '120 E.S.R(mΩ)',
        'R10': '10 E.S.R(mΩ)',
        'R12': '12 E.S.R(mΩ)',
        'R15': '15 E.S.R(mΩ)',
        'R40': '40 E.S.R(mΩ)',
        'RB0': '200 E.S.R(mΩ)',
        'RB2': '220 E.S.R(mΩ)'},
    8: {
        'XXX': '特殊编码Special Code',
        '': ''
    },
}
MIN_NUM_AISHI = 15
RE_RULE_AISHI = {
    'RE_RULE_1': r'^S$',
    'RE_RULE_2': r'^A0|A1|A2$',
    'RE_RULE_3': r'^0B|0E|0G|0J|0Q|1A|1C|1E|1V|1H$',
    'RE_RULE_4': r'^Y|K|M|Q|V|A|C|J|B|W|G|L$',
    'RE_RULE_5': r'^4R7|100|150|220|330|470|680|820|101|151|181|201|221|331|471|561$',
    'RE_RULE_6': r'^A09|A19|A28$',
    'RE_RULE_7': r'^R04|R06|R07|R09|RA0|RA2|R10|R12|R15|R40|RB0|RB2$',
    'RE_RULE_8': r'(XXX){0,1}$',
}
SECTION_NUM_AISHI = {
    # 品牌AISHI
    8: [0, 1, 3, 5, 6, 9, 12, 15, 18]
}


MIN_NUM_CCTC = 10
brand_rule_cctc = {
    1: {'TCC': 'Code of CeramicCapacitor'},
    2: {'0402': 'Chip Size 1.00×0.50mm',
        '0603': 'Chip Size 1.60×0.80mm',
        '0805': 'Chip Size 2.00×1.25mm',
        '1206': 'Chip Size 3.20×1.60mm',
        '1210': 'Chip Size 3.20×2.50mm',
        '1808': 'Chip Size 4.50×2.00mm',
        '1812': 'Chip Size 4.50×3.20mm',
        '2220': 'Chip Size 5.70×5.00mm ',
        '2225': 'Chip Size 6.40×5.70mm'},
    3: {'COG': 'Dielectrics',
        'X7R': 'Dielectrics',
        'X5R': 'Dielectrics',
        'Y5V': 'Dielectrics'},
    4: {'105': 'Capacitance 1000,000pF'},
    5: {
        'A': 'Capacitance Tolerance ±0.05pF',
        'B': 'Capacitance Tolerance ±0.1pF',
        'C': 'Capacitance Tolerance ±0.25pF ',
        'D': 'Capacitance Tolerance ±0.05pF',
        'F': 'Capacitance Tolerance ±1.0%',
        'G': 'Capacitance Tolerance ±2.0% ',
        'J': 'Capacitance Tolerance ±5.0% ',
        'K': 'Capacitance Tolerance ±10% ',
        'M': 'Capacitance Tolerance ±20%',
        'Z': 'Capacitance Tolerance -20/+80%',
    },
    6: {
      '6R3': 'Rated Voltage 6.3VDC ',
      '100': 'Rated Voltage 10VDC ',
      '160': 'Rated Voltage 16VDC ',
      '250': 'Rated Voltage 25VDC ',
      '500': 'Rated Voltage 50VDC ',
      '101': 'Rated Voltage 100VDC ',
      '201': 'Rated Voltage 200VDC ',
      '251': 'Rated Voltage 250VDC ',
      '501': 'Rated Voltage 500VDC ',
      '102': 'Rated Voltage 1000VDC ',
      '202': 'Rated Voltage 2000VDC ',
    },
    7: {
        'A': 'Thickness 0.5±0.05mm',
        'B': 'Thickness 0.60±0.10mm',
        'C': 'Thickness 0.80±0.10mm ',
        'D': 'Thickness 0.85±0.10mm',
        'E': 'Thickness 1.00±0.10mm ',
        'F': 'Thickness 1.25±0.20mm ',
        'H': 'Thickness 1.6±0.20mm ',
        'G': 'Thickness 2.0±0.20mm ',
        'M': 'Thickness 2.5±0.30mm',
    },
    8: {
        'B': 'bulk packaging in a bag',
        'T': 'tape carrier packaging ',
    },
}
RE_RULE_CCTC = {
    'RE_RULE_1': r'^TCC$',
    'RE_RULE_2': r'^0402|0603|0805|1206|1210|1808|1812|2220|2225$',
    'RE_RULE_3': r'^COG|X7R|X5R|Y5V$',
    'RE_RULE_4': r'^105$',
    'RE_RULE_5': r'^A|B|C|D|F|G|J|K|M|Z$',
    'RE_RULE_6': r'^6R3|100|160|250|500|101|251|501|102|202$',
    'RE_RULE_7': r'^A|B|C|D|E|F|H|G|M$',
    'RE_RULE_8': r'^B|T$',
}
SECTION_NUM_CCTC = {
    # 品牌CCTC
    # CL10A106MP8NNNC
    # 0123456789
    # CL 10 A 106 MP 8 N N N C
    #   [0, 2, 3, 4]
    8: [0, 3, 7, 10, 13, 14, 17, 18, 19]
}


MIN_NUM_CHINOCERA = 0
brand_rule_chinocera = {
    1: {
        'HGC': "Genernal",
        'HHV': "Mid-High Vatage"
    },
    2: {
        '0402': '1005mm',
        '0603': '1608mm',
        '0805': '2012mm',
        '1206': '3216mm',
        '1210': '3225mm',
        '1808': '4520mm',
        '1812': '4532mm',
        '1005': '0402mm',
        '0201': '0603mm'
    },
    3: {
        'R5': 'X5R',
        'R6': 'X6R',
        'S6': 'X6S',
        'R7': 'X7R',
        'S7': 'X7S',
        'T7': 'X7T',
        'R8': 'X8R',
        'G0': 'C0G',
        'H0': 'C0H'
    },
    4: {
        'R75': '0.75pF',
        '0R5': '0.5pF',
        '1R0': '1pF',
        '100': '10pF',
        '101': '100pF',
        '102': '1000pF',
        '103': '10nF',
        '104': '100nF',
        '105': '1uF',
        '106': '10uF',
        '107': '100uF'
    },
    5: {
        'A': '±0.05pF',
        'B': '±0.1pF',
        'C': '±0.25pF',
        'D': '±0.5pF',
        'F': '±1%',
        'G': '±2%',
        'J': '±5%',
        'K': '±10%',
        'L': '±15%',
        'M': '±20%',
        'S': '-20%~+50%'
    },
    6: {
        '4R0': '4 Vdc',
        '6R3': '6.3 Vdc',
        '100': '10 Vdc',
        '160': '16 Vdc',
        '250': '25 Vdc',
        '500': '50 Vdc',
        '101': '100 Vdc',
        '201': '200 Vdc',
        '251': '250 Vdc',
        '501': '500 Vdc',
        '631': '630 Vdc',
        '102': '1k Vdc',
        '152': '1.5k Vdc',
        '202': '2k Vdc',
        '252': '2.5k Vdc',
        '302': '3k Vdc',
        '402': '4k Vdc',
        '502': '5k Vdc',
        '602': '6k Vd'
    },
    7: {
        'N': 'Cu/Ni/Sn',
        'C': 'Cu/Resin/Ni/Sn'
    },
    8: {
        'T': 'Paper taping',
        'B': 'Bulk',
        'S': 'Embossedtaping'
    },
    9: {
        'A': '0.1mm',
        'B': '0.2mm',
        'C': '0.3mm',
        'D': '0.4mm',
        'E': '0.5mm',
        'F': '0.6mm',
        'G': '0.7mm',
        'H': '0.8mm',
        'J': '1.0mm',
        'L': '1.2mm',
        'P': '1.6mm',
        'S': '1.8mm',
        'U': '2.0mm',
        'V': '2.5mm',
        'W': '3.0mm'
    },
    10: {
        'J': '7Inch',
        'D': '13Inch',
        'K': '7Inch'
    },

}
RE_RULE_CHINOCERA = {
    'RE_RULE_1': r'^HHV|HGC$',
    'RE_RULE_2': r'^1005|0201|1206|0402|0603|0805|1210|1808|1812$',
    'RE_RULE_3': r'^R5|R6|S6|R7|S7|T7|R8|G0|H0$',
    'RE_RULE_4': r'^R75|0R5|1R0|100|101|102|103|104|105|106|107$',
    'RE_RULE_5': r'^A|B|C|D|F|G|J|K|L|M|S$',
    'RE_RULE_6': r'^4R0|6R3|100|160|250|500|101|201|251|501|631|102|152|202|252|302|402|502|602$',
    'RE_RULE_7': r'^N|C$',
    'RE_RULE_8': r'^T|B|S$',
    'RE_RULE_9': r'^A|B|C|D|E|F|G|H|J|L|P|S|U|V|W$',
    'RE_RULE_10': r'^J|D|K$',
}
SECTION_NUM_CHINOCERA = {
    # 品牌CHINOCERA
    10: [0, 3, 7, 9, 12, 13, 16, 17, 18, 19, 20]
}


