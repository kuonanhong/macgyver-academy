#!/usr/bin/env python3
"""Six standard-library teaching experiments; synthetic data, SI units.
python3 run-water-labs.py --check
python3 run-water-labs.py --output example-results.json
"""
import argparse
import json
import math
from pathlib import Path

G = 9.81


def finite_positive(*values):
    if not all(math.isfinite(v) and v > 0 for v in values):
        raise ValueError('Inputs must be finite and positive.')


def reservoir(storage, inflows, outflows, dt):
    """Piecewise constant interval means, no rain/evaporation/leakage."""
    finite_positive(dt)
    if len(inflows) != len(outflows) or not math.isfinite(storage) or storage < 0:
        raise ValueError('Equal-length flows and nonnegative initial storage required.')
    rows = []
    for i, (qin, qout) in enumerate(zip(inflows, outflows), 1):
        if not all(math.isfinite(x) and x >= 0 for x in (qin, qout)):
            raise ValueError('Finite nonnegative interval flow required.')
        after = storage + (qin - qout) * dt
        if after < 0:
            raise ValueError('Infeasible release: negative storage; no silent clipping.')
        rows.append({'time_s': i*dt, 'inflow_m3s': qin, 'outflow_m3s': qout,
                     'storage_m3': after, 'residual_m3': after-storage-(qin-qout)*dt})
        storage = after
    return rows


def channel(width, depth, roughness, slope):
    """Manning SI rectangular uniform flow, including two wetted sides."""
    finite_positive(width, depth, roughness, slope)
    area = width*depth
    radius = area/(width+2*depth)
    discharge = area*radius**(2/3)*math.sqrt(slope)/roughness
    return {'area_m2': area, 'hydraulic_radius_m': radius, 'Q_m3s': discharge,
            'Fr': discharge/area/math.sqrt(G*depth)}


def jump(depth, velocity):
    """Rectangular horizontal channel, hydrostatic ends, unit momentum factors."""
    finite_positive(depth, velocity)
    fr = velocity/math.sqrt(G*depth)
    if fr <= 1:
        raise ValueError('Upstream Froude number must exceed one.')
    q = depth*velocity
    y2 = depth*(math.sqrt(1+8*fr**2)-1)/2
    momentum1, momentum2 = depth**2/2+q*q/(G*depth), y2*y2/2+q*q/(G*y2)
    return {'Fr1': fr, 'y2_m': y2, 'head_loss_m': (y2-depth)**3/(4*depth*y2),
            'momentum_residual_m2': momentum2-momentum1}


def waves(height, period, depth):
    """Small-amplitude REGULAR deep-water waves, not significant-wave spectra."""
    finite_positive(height, period, depth)
    wavelength = G*period**2/(2*math.pi)
    if depth < wavelength/2 or height/wavelength > .05:
        raise ValueError('Requires depth >= L0/2 and H/L0 <= 0.05.')
    energy = 1025*G*height**2/8
    group_velocity = G*period/(4*math.pi)
    return {'L0_m': wavelength, 'energy_Jm2': energy, 'group_velocity_ms': group_velocity,
            'power_kWm': energy*group_velocity/1000}


def surge(wave_speed, delta_velocity, length, closure):
    """Single full freshwater pipe, rapid deceleration; no cavitation/reflections."""
    finite_positive(wave_speed, delta_velocity, length, closure)
    round_trip = 2*length/wave_speed
    if closure > round_trip:
        raise ValueError('Slow closure: Joukowsky rapid-change model not applicable.')
    return {'round_trip_s': round_trip, 'pressure_rise_MPa': wave_speed*delta_velocity/1000,
            'head_rise_m': wave_speed*delta_velocity/G}


def scale(length_ratio, prototype_flow):
    """Undistorted Froude model at equal gravitational acceleration."""
    finite_positive(length_ratio, prototype_flow)
    if length_ratio <= 1:
        raise ValueError('Prototype/model length ratio must exceed one.')
    return {'velocity_ratio': math.sqrt(length_ratio), 'time_ratio': math.sqrt(length_ratio),
            'flow_ratio': length_ratio**2.5, 'model_flow_m3s': prototype_flow/length_ratio**2.5}


def experiments():
    return {
        'reservoir': reservoir(100000, [10, 20, 40, 30, 15, 5], [8, 10, 20, 25, 20, 10], 3600),
        'channel': [dict(n=n, **channel(5, 2, n, .001)) for n in [.02, .03, .04, .05]],
        'jump': [dict(v1_ms=v, **jump(.5, v)) for v in [3, 4, 5, 6]],
        'waves': [dict(H_m=h, **waves(h, 8, 100)) for h in [1, 2, 3, 4]],
        'surge': [dict(delta_v_ms=v, **surge(1000, v, 1000, .5)) for v in [.5, 1, 1.5, 2]],
        'scale': [dict(length_ratio=r, **scale(r, 1000)) for r in [10, 25, 50, 100]],
    }


def check():
    close = lambda a, b: math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-10)
    x = experiments()
    assert x['reservoir'][-1]['storage_m3'] == 197200
    assert all(r['residual_m3'] == 0 for r in x['reservoir'])
    assert close(x['channel'][0]['Q_m3s']/x['channel'][2]['Q_m3s'], 2)
    assert all(abs(r['momentum_residual_m2']) < 1e-10 for r in x['jump'])
    assert close(x['waves'][1]['power_kWm']/x['waves'][0]['power_kWm'], 4)
    assert close(x['surge'][1]['pressure_rise_MPa'], 1)
    assert close(x['scale'][1]['model_flow_m3s'], .32)
    for fn, args in [(jump, (.5, .1)), (waves, (2, 8, 10)), (surge, (1000, 1, 1000, 3)),
                     (reservoir, (0, [0], [10], 3600)), (channel, (5, 2, 0, .001)), (scale, (1, 1000))]:
        try:
            fn(*args)
        except ValueError:
            pass
        else:
            raise AssertionError('Invalid domain was accepted: '+fn.__name__)
    return x


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = check() if args.check else experiments()
    data = {'scope': 'Original synthetic educational examples; not operational forecasts or design values.',
            'models': result}
    text = json.dumps(data, ensure_ascii=False, indent=2)+'\n'
    if args.output:
        args.output.write_text(text, encoding='utf-8')
    elif args.check:
        print('PASS: six water labs, conservation/scaling identities and six invalid-domain cases.')
    else:
        print(text, end='')


if __name__ == '__main__':
    main()
