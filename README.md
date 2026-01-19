# SHARP to XYZ Converter

<p align="center">
  <img src="https://img.shields.io/badge/Unreal%20Engine-5.x-0E1128?style=for-the-badge&logo=unrealengine&logoColor=white" alt="Unreal Engine 5">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License">
</p>

Convert [Apple SHARP](https://github.com/apple/ml-sharp) 3D Gaussian Splatting (3DGS) PLY files to standard XYZ point cloud format with RGB colors.

**Perfect for importing AI-generated 3D content into Unreal Engine.**

## Example Results

| Input Image | Unreal Engine Point Cloud |
|:-----------:|:-------------------------:|
| ![Input](images/input_original.jpg) | ![Output](images/output_unreal.png) |

## Features

- Convert SHARP 3DGS PLY files to ASCII XYZ format
- Automatic spherical harmonics to RGB color conversion
- Single file and batch directory processing
- Zero dependencies (pure Python standard library)
- Direct import into Unreal Engine LiDAR Point Cloud plugin

## Installation

```bash
git clone https://github.com/omolism/sharp-to-xyz.git
cd sharp-to-xyz
```

No additional dependencies required - uses only Python standard library.

## Quick Start

```bash
# Convert PLY to XYZ
python sharp_to_xyz.py input.ply output.xyz
```

## Unreal Engine Integration

### Prerequisites

1. Unreal Engine 5.x
2. LiDAR Point Cloud Plugin (built-in)

### Step 1: Enable LiDAR Point Cloud Plugin

1. Open your Unreal project
2. Go to **Edit → Plugins**
3. Search for **"LiDAR Point Cloud"**
4. Check **Enabled**
5. Restart the editor

### Step 2: Import XYZ Point Cloud

1. Drag your `.xyz` file into the **Content Browser**
2. The import dialog will appear automatically
3. Keep default settings and click **Import**
4. A `ULidarPointCloud` asset is created with full RGB color support

### Step 3: Add to Scene

1. Drag the point cloud asset into your level
2. Adjust transform as needed
3. Configure rendering settings in Details panel:
   - **Point Size**: Adjust for density
   - **Rendering Mode**: Points, Sprites, or Meshes

### Supported Import Settings

| Setting | Recommended Value |
|---------|-------------------|
| Import Format | XYZ RGB |
| Scale | 100 (cm to m conversion) |
| Point Size | 1.0 - 5.0 |

## Complete Workflow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Single    │     │    SHARP    │     │  sharp-to-  │     │   Unreal    │
│   Image     │ ──> │   (Apple)   │ ──> │    xyz      │ ──> │   Engine    │
│  .jpg/.png  │     │   .ply      │     │   .xyz      │     │  LiDAR PC   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

### Full Pipeline Example

```bash
# 1. Generate 3DGS with SHARP
conda activate sharp
sharp predict -i photo.jpg -o ./output/

# 2. Convert to XYZ
python sharp_to_xyz.py ./output/photo.ply ./output/photo.xyz

# 3. Import to Unreal Engine
# Drag .xyz into Content Browser (LiDAR Point Cloud plugin required)
```

## Usage

### Command Line

```bash
# Convert single file
python sharp_to_xyz.py input.ply

# Convert with custom output name
python sharp_to_xyz.py input.ply output.xyz

# Batch convert directory
python sharp_to_xyz.py ./ply_folder/ ./xyz_output/

# Quiet mode
python sharp_to_xyz.py input.ply -q
```

### Python API

```python
from sharp_to_xyz import convert_ply_to_xyz, batch_convert

# Single file
convert_ply_to_xyz('input.ply', 'output.xyz')

# Batch convert
batch_convert('./ply_folder/', './xyz_output/')
```

## Output Format

ASCII text with space-separated values:

```
X Y Z R G B
-2.181 -1.207 3.250 80 70 58
-3.590 -2.076 5.153 61 55 40
...
```

## Performance

| Points | Conversion Time | Output Size |
|--------|----------------|-------------|
| 1.18M | ~10 seconds | ~80 MB |
| 500K | ~4 seconds | ~34 MB |
| 100K | ~1 second | ~7 MB |

## How It Works

SHARP stores colors as spherical harmonics (SH) coefficients. This tool extracts the DC component and converts to RGB:

```python
SH_C0 = 0.28209479177387814

def sh_to_rgb(f_dc_0, f_dc_1, f_dc_2):
    r = 0.5 + SH_C0 * f_dc_0
    g = 0.5 + SH_C0 * f_dc_1
    b = 0.5 + SH_C0 * f_dc_2
    return clamp(r, g, b)
```

## Other Applications

The XYZ format is also compatible with:
- **CloudCompare** - Open directly
- **Blender** - Via Point Cloud Visualizer addon
- **Open3D** - Python visualization

## Credits

- [Apple SHARP](https://github.com/apple/ml-sharp) - Monocular 3D Gaussian Splatting model
- [3D Gaussian Splatting](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/) - Original research paper
- [Unreal LiDAR Point Cloud Plugin](https://docs.unrealengine.com/5.0/en-US/lidar-point-cloud-plugin-in-unreal-engine/) - Official documentation

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions welcome! Please open an issue or pull request.

## Citation

```bibtex
@software{sharp_to_xyz,
  title = {SHARP to XYZ Converter},
  author = {DanciShen},
  year = {2026},
  url = {https://github.com/omolism/sharp-to-xyz}
}
```
