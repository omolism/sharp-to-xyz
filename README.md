# SHARP to XYZ Converter

<p align="center">
  <img src="https://img.shields.io/badge/Unreal%20Engine-black?style=for-the-badge&logo=unrealengine&logoColor=white" alt="Unreal Engine">
  <img src="https://img.shields.io/badge/Python-black?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/MIT-black?style=for-the-badge" alt="MIT License">
</p>

Convert [Apple SHARP](https://github.com/apple/ml-sharp) 3D Gaussian Splatting (3DGS) PLY files to standard XYZ point cloud format with RGB colors.

**Perfect for importing AI-generated 3D content into Unreal Engine.**

## Example Results

| Input Image | Unreal Engine Point Cloud |
|:-----------:|:-------------------------:|
| ![Input](images/input_original.jpg) | ![Output](images/output_unreal.png) |

## Quick Start

### 1. Install

```bash
git clone https://github.com/omolism/sharp-to-xyz.git
cd sharp-to-xyz
```

No dependencies required - uses only Python standard library.

### 2. Convert PLY to XYZ

```bash
python sharp_to_xyz.py input.ply output.xyz
```

### 3. Import to Unreal Engine

1. **Enable Plugin**: Edit → Plugins → search "LiDAR Point Cloud" → Enable → Restart
2. **Import**: Drag `.xyz` file into Content Browser
3. **Add to Scene**: Drag asset into level, adjust **Point Size** in Details panel

## Complete Workflow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Single    │     │    SHARP    │     │  sharp-to-  │     │   Unreal    │
│   Image     │ ──> │   (Apple)   │ ──> │    xyz      │ ──> │   Engine    │
│  .jpg/.png  │     │   .ply      │     │   .xyz      │     │  LiDAR PC   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

## Usage

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

## Other Applications

The XYZ format is also compatible with:
- **CloudCompare** - Open directly
- **Blender** - Via Point Cloud Visualizer addon
- **Open3D** - Python visualization

## Credits

- [Apple SHARP](https://github.com/apple/ml-sharp) - Monocular 3D Gaussian Splatting model
- [3D Gaussian Splatting](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/) - Original research paper
- [Unreal LiDAR Point Cloud Plugin](https://docs.unrealengine.com/5.0/en-US/lidar-point-cloud-plugin-in-unreal-engine/) - Official documentation
- Example image from Gentle Monster × Mugler pop-up event

## License

MIT License - see [LICENSE](LICENSE) for details.
