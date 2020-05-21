#!/usr/bin/env python3
# Gatema GERBER data prepare

from pathlib import Path

try:
    project_name = list(Path('../design').glob('*.pro'))[0].stem
except IndexError:
    print('Error: KiCad *.pro is not found.')
    exit(-1)

out_name = f'gatema_{project_name}'

gerber_dir = Path('../gerber')

if not gerber_dir.is_dir():
    print('Dir gerber not exists!')
    exit(-1)

for file in gerber_dir.iterdir():
    layer = file.stem.split(project_name + '-')[-1]
    suffix = None

    if file.suffix == '.gbr':

        if layer == 'TOP':
            suffix = 'top'

        elif layer == 'IN2_GND':
            suffix = 'in2'

        elif layer == 'IN3_POWER':
            suffix = 'in3'

        elif layer == 'BOT':
            suffix = 'bot'

        elif layer == 'F_Mask':
            suffix = 'smt'

        elif layer == 'B_Mask':
            suffix = 'smb'

        elif layer == 'F_SilkS':
            suffix = 'plt'

        elif layer == 'Edge_Cuts':
            suffix = 'dim'


    elif file.suffix == '.drl':
        if layer == 'PTH':
            suffix = 'pth'

        if layer == 'NPTH':
            suffix = 'mill'

    if not suffix is None:
        file.rename(
            Path(f'{gerber_dir}/{out_name}.{suffix}')
        )



