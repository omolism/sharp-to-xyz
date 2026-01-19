#!/usr/bin/env python3
"""
SHARP to XYZ Converter

Convert Apple SHARP 3D Gaussian Splatting PLY files to standard XYZ point cloud format.

Usage:
    python sharp_to_xyz.py input.ply [output.xyz]
    python sharp_to_xyz.py /folder/with/plys/ [output_folder/]

Author: DanciShen
License: MIT
"""

import struct
import sys
import os
import argparse
from pathlib import Path
from typing import Tuple, List, Optional

# Spherical harmonics constant for DC component (degree 0)
SH_C0 = 0.28209479177387814


def sh_to_rgb(f_dc_0: float, f_dc_1: float, f_dc_2: float) -> Tuple[int, int, int]:
    """
    Convert spherical harmonics DC component to RGB (0-255).

    The DC component of spherical harmonics represents the base color.
    Formula: color = 0.5 + SH_C0 * f_dc

    Args:
        f_dc_0: Red channel SH coefficient
        f_dc_1: Green channel SH coefficient
        f_dc_2: Blue channel SH coefficient

    Returns:
        Tuple of (R, G, B) values in range 0-255
    """
    r = max(0.0, min(1.0, 0.5 + SH_C0 * f_dc_0))
    g = max(0.0, min(1.0, 0.5 + SH_C0 * f_dc_1))
    b = max(0.0, min(1.0, 0.5 + SH_C0 * f_dc_2))
    return int(r * 255), int(g * 255), int(b * 255)


def parse_ply_header(file_path: str) -> dict:
    """
    Parse PLY file header and return metadata.

    Args:
        file_path: Path to PLY file

    Returns:
        Dictionary containing:
        - elements: List of element definitions
        - header_size: Size of header in bytes
        - format: 'binary_little_endian' or 'ascii'
    """
    with open(file_path, 'rb') as f:
        elements = []
        current_element = None
        format_type = None

        while True:
            line = f.readline()
            decoded = line.decode('utf-8').strip()

            if decoded.startswith('format'):
                format_type = decoded.split()[1]
            elif decoded.startswith('element'):
                parts = decoded.split()
                current_element = {
                    'name': parts[1],
                    'count': int(parts[2]),
                    'properties': []
                }
                elements.append(current_element)
            elif decoded.startswith('property'):
                parts = decoded.split()
                prop_type = parts[1]
                prop_name = parts[2]
                current_element['properties'].append((prop_name, prop_type))
            elif decoded == 'end_header':
                header_size = f.tell()
                break

        return {
            'elements': elements,
            'header_size': header_size,
            'format': format_type
        }


def get_type_format(prop_type: str) -> Tuple[str, int]:
    """
    Get struct format character and size for PLY property type.

    Args:
        prop_type: PLY property type string

    Returns:
        Tuple of (format_char, byte_size)
    """
    type_map = {
        'float': ('f', 4),
        'float32': ('f', 4),
        'double': ('d', 8),
        'float64': ('d', 8),
        'uchar': ('B', 1),
        'uint8': ('B', 1),
        'char': ('b', 1),
        'int8': ('b', 1),
        'ushort': ('H', 2),
        'uint16': ('H', 2),
        'short': ('h', 2),
        'int16': ('h', 2),
        'uint': ('I', 4),
        'uint32': ('I', 4),
        'int': ('i', 4),
        'int32': ('i', 4),
    }
    return type_map.get(prop_type, ('f', 4))


def convert_ply_to_xyz(
    input_path: str,
    output_path: Optional[str] = None,
    verbose: bool = True
) -> str:
    """
    Convert SHARP 3DGS PLY file to XYZ point cloud format.

    Args:
        input_path: Path to input PLY file
        output_path: Path to output XYZ file (default: same name with .xyz extension)
        verbose: Print progress information

    Returns:
        Path to output file
    """
    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + '.xyz'

    if verbose:
        print(f"Reading: {input_path}")

    # Parse header
    metadata = parse_ply_header(input_path)
    elements = metadata['elements']

    # Find vertex element
    vertex_elem = None
    for elem in elements:
        if elem['name'] == 'vertex':
            vertex_elem = elem
            break

    if vertex_elem is None:
        raise ValueError("No vertex element found in PLY file")

    vertex_count = vertex_elem['count']
    properties = vertex_elem['properties']

    if verbose:
        print(f"Vertex count: {vertex_count:,}")
        print(f"Properties: {len(properties)}")

    # Build format string and calculate sizes
    format_string = '<'
    bytes_per_vertex = 0

    for prop_name, prop_type in properties:
        fmt_char, size = get_type_format(prop_type)
        format_string += fmt_char
        bytes_per_vertex += size

    # Read binary data
    with open(input_path, 'rb') as f:
        f.seek(metadata['header_size'])
        vertex_data_size = vertex_count * bytes_per_vertex
        binary_data = f.read(vertex_data_size)

    if len(binary_data) != vertex_data_size:
        raise ValueError(f"Expected {vertex_data_size} bytes, got {len(binary_data)}")

    # Get property indices
    prop_indices = {name: i for i, (name, _) in enumerate(properties)}

    x_idx = prop_indices.get('x', 0)
    y_idx = prop_indices.get('y', 1)
    z_idx = prop_indices.get('z', 2)
    f_dc_0_idx = prop_indices.get('f_dc_0')
    f_dc_1_idx = prop_indices.get('f_dc_1')
    f_dc_2_idx = prop_indices.get('f_dc_2')

    has_color = f_dc_0_idx is not None

    if verbose:
        print(f"Has color data: {has_color}")
        print(f"Writing: {output_path}")

    # Write XYZ file
    with open(output_path, 'w') as f_out:
        for i in range(vertex_count):
            offset = i * bytes_per_vertex
            vertex_bytes = binary_data[offset:offset + bytes_per_vertex]
            vertex_data = struct.unpack(format_string, vertex_bytes)

            x = vertex_data[x_idx]
            y = vertex_data[y_idx]
            z = vertex_data[z_idx]

            if has_color:
                f_dc_0 = vertex_data[f_dc_0_idx]
                f_dc_1 = vertex_data[f_dc_1_idx]
                f_dc_2 = vertex_data[f_dc_2_idx]
                r, g, b = sh_to_rgb(f_dc_0, f_dc_1, f_dc_2)
            else:
                r, g, b = 128, 128, 128

            f_out.write(f"{x} {y} {z} {r} {g} {b}\n")

            if verbose and (i + 1) % 200000 == 0:
                print(f"  Processed {i + 1:,}/{vertex_count:,} vertices...")

    if verbose:
        print(f"Done! Output: {output_path}")

    return output_path


def batch_convert(
    input_dir: str,
    output_dir: Optional[str] = None,
    verbose: bool = True
) -> List[str]:
    """
    Convert all PLY files in a directory.

    Args:
        input_dir: Directory containing PLY files
        output_dir: Output directory (default: same as input)
        verbose: Print progress information

    Returns:
        List of output file paths
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir) if output_dir else input_path

    output_path.mkdir(parents=True, exist_ok=True)

    ply_files = list(input_path.glob('*.ply'))

    if verbose:
        print(f"Found {len(ply_files)} PLY files")

    outputs = []
    for i, ply_file in enumerate(ply_files, 1):
        if verbose:
            print(f"\n[{i}/{len(ply_files)}] Processing {ply_file.name}")

        output_file = output_path / (ply_file.stem + '.xyz')
        convert_ply_to_xyz(str(ply_file), str(output_file), verbose=verbose)
        outputs.append(str(output_file))

    return outputs


def main():
    parser = argparse.ArgumentParser(
        description='Convert SHARP 3DGS PLY files to XYZ point cloud format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.ply                    # Convert single file
  %(prog)s input.ply output.xyz         # Convert with custom output name
  %(prog)s ./ply_folder/ ./xyz_output/  # Batch convert directory
  %(prog)s input.ply -q                 # Quiet mode
        """
    )

    parser.add_argument(
        'input',
        help='Input PLY file or directory containing PLY files'
    )
    parser.add_argument(
        'output',
        nargs='?',
        help='Output XYZ file or directory (default: same location with .xyz extension)'
    )
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Suppress progress output'
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    verbose = not args.quiet

    if input_path.is_dir():
        batch_convert(str(input_path), args.output, verbose=verbose)
    elif input_path.is_file():
        convert_ply_to_xyz(str(input_path), args.output, verbose=verbose)
    else:
        print(f"Error: {args.input} does not exist", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
