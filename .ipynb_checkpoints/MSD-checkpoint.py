"""

- Author: Tolib Abdurakhmonov
- Affiliation: Institute of Physics, University of Rostock
- Email: abdurakhmonov.t.z@gmail.com

========================================
This script can be used to calculate MSD and RMSD for MD simulaions. It will only accept xyz file 
and create datafiles and also plot them if you want to stay completely in python environment, but 
you free to use any other program/language to plot.
========================================
"""

#!/usr/bin/env python3
"""
xyz_msd_rmsd.py
===============

Compute mean-square displacement (MSD) and the simple root-mean-square
deviation (RMSD) of all atoms in an XYZ trajectory with respect to the
FIRST frame, then write a data table and (optionally) a plot.

* Works with plain XYZ or extended XYZ.
* Needs only NumPy + (optionally) Matplotlib.
* Handles arbitrarily large files by streaming - memory stays small.

Usage
-----
  python xyz_msd_rmsd.py input.xyz [--out MSD_RMSD.dat] [--dt 1]
                                   [--png rmsd.png] [--skip 10]

Options
-------
  --dt   timestep size in **fs** (floating-point). If omitted, the script
         tries to read a token like "Time=0.5" or "t=0.5" in every comment
         line and will fall back to the integer frame index if nothing
         looks like a time.
  --skip analyse every n-th frame (speeds up very long runs; default 1).
"""

import sys, re, argparse
import numpy as np

def parse_xyz(fname, skip):
    """Yield (frame_idx, comment, coordinates[N,3]) from *any* XYZ/EXTXYZ."""
    with open(fname) as fh:
        fidx = 0
        while True:
            nline = fh.readline()
            if not nline:
                break                   # EOF
            nat = int(nline.split()[0])
            comment = fh.readline().rstrip()

            # read nat lines safely, forget extra columns
            xyz = np.empty((nat, 3))
            for i in range(nat):
                parts = fh.readline().split()
                if len(parts) < 4:
                    raise ValueError(f"Line {i+3} in frame {fidx} "
                                     "has < 4 columns.")
                xyz[i] = [float(parts[1]), float(parts[2]), float(parts[3])]

            if fidx % skip == 0:
                yield fidx, comment, xyz
            fidx += 1


def time_from_comment(cmt):
    """Pick first float following (Time|time|t)= or step= .  Return None if absent."""
    m = re.search(r'(?:time|Time|t|step)\s*[=:]\s*([-+]?\d*\.?\d+([eE][-+]?\d+)?)', cmt)
    return float(m.group(1)) if m else None

def compute_msd(file_in, dt, skip):
    times, msd, rmsd = [], [], []
    r0 = None
    for fidx, comment, coords in parse_xyz(file_in, skip):
        if r0 is None:
            r0 = coords.copy()
        dr2 = np.square(coords - r0).sum(axis=1)   # per atom squared disp.
        msd.append(dr2.mean())
        rmsd.append(np.sqrt(msd[-1]))
        # pick time
        t = time_from_comment(comment)
        times.append(t if t is not None else (fidx*dt if dt is not None else fidx))
    return np.asarray(times), np.asarray(msd), np.asarray(rmsd)

def main():
    ap = argparse.ArgumentParser(description="MSD/RMSD from an XYZ trajectory")
    ap.add_argument('xyz', help='input XYZ')
    ap.add_argument('--out', default='MSD_RMSD.dat', help='output data file')
    ap.add_argument('--dt', type=float, help='timestep (ps) if not in comment')
    ap.add_argument('--png', default='rmsd.png', help='plot file (omit to skip plot)')
    ap.add_argument('--skip', type=int, default=1, help='use every n-th frame')
    args = ap.parse_args()

    t, msd, rmsd = compute_msd(args.xyz, args.dt/1000, args.skip)

    # save table
    np.savetxt(args.out, np.column_stack((t, rmsd, msd)),
               header="time(ps)   RMSD(Ang)   MSD(Ang^2)")
    print(f"✔  wrote {args.out}  with {len(t)} lines")

    # optional plot
    if args.png:
        try:
            import matplotlib.pyplot as plt
            plt.figure(figsize=(5,4))
            plt.plot(t, rmsd, label='RMSD')
            plt.xlabel('time (ps)' if args.dt or np.any(np.isfinite(t)) else 'frame')
            plt.ylabel(r' RMSD / Å')
            plt.legend()
            plt.tight_layout()
            plt.savefig(args.png, dpi=300)
            print(f"✔  wrote {args.png}")
        except ImportError:
            print("Matplotlib not available – skipping plot")

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(__doc__)
    else:
        main()
