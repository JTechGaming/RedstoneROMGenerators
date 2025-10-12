import os
import zipfile
import re
import mcschematic
from amulet_nbt import load as load_bedrock_nbt
from amulet_nbt import CompoundTag

def load_mcstructure_blocks(structure_path):
    structure = load_bedrock_nbt(structure_path)

    if "structure" not in structure:
        raise Exception("No 'structure' tag found in structure file")

    structure_data = structure["structure"]

    # Block palette
    palette = structure_data["palette"]["default"]
    block_palette = [p["name"].value for p in palette]

    # Block indices map into palette by index
    block_indices = structure_data["block_indices"]
    pos_data = structure_data["block_position_data"]

    blocks = []
    for i, index_tag in enumerate(block_indices):
        block_id = block_palette[index_tag]
        x, y, z = pos_data[i * 3:i * 3 + 3]
        blocks.append((int(x), int(y), int(z), block_id))

    return blocks

def parse_mcfunctions(mcpack_path, output_path="output.schem"):
    temp_dir = "temp_unpack"
    if os.path.exists(temp_dir):
        import shutil
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

    # Unzip .mcpack
    with zipfile.ZipFile(mcpack_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    schematic = mcschematic.MCSchematic()
    placed_blocks = 0

    structure_dir = os.path.join(temp_dir, "structures", "mapart")

    # Find the mcfunction directory
    mcfunction_dirs = set()
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            if file.endswith(".mcfunction"):
                mcfunction_dirs.add(os.path.dirname(os.path.join(root, file)))

    if not mcfunction_dirs:
        print("❌ No .mcfunction files found.")
        return

    print(f"📂 Found .mcfunction files in {', '.join(mcfunction_dirs)}")

    # Regex patterns
    setblock_pattern = re.compile(r"setblock\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+([\w:]+)")
    fill_pattern = re.compile(r"fill\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+([\w:]+)")
    structure_pattern = re.compile(r"structure\s+load\s+mapart:([\w]+)\s+([~\d\-]+)\s+([~\d\-]+)\s+([~\d\-]+)")

    for mcfunction_dir in mcfunction_dirs:
        for file in sorted(os.listdir(mcfunction_dir)):
            if not file.endswith(".mcfunction"):
                continue
            with open(os.path.join(mcfunction_dir, file), "r") as f:
                for line in f:
                    print(line.strip())
                    # Match setblock
                    set_match = setblock_pattern.match(line.strip())
                    if set_match:
                        x, y, z, block = set_match.groups()
                        schematic.setBlock((int(x), int(y), int(z)), block)
                        placed_blocks += 1
                        continue

                    # Match fill
                    fill_match = fill_pattern.match(line.strip())
                    if fill_match:
                        x1, y1, z1, x2, y2, z2, block = fill_match.groups()
                        x1, y1, z1 = int(x1), int(y1), int(z1)
                        x2, y2, z2 = int(x2), int(y2), int(z2)

                        for x in range(min(x1, x2), max(x1, x2)+1):
                            for y in range(min(y1, y2), max(y1, y2)+1):
                                for z in range(min(z1, z2), max(z1, z2)+1):
                                    schematic.setBlock((x, y, z), block)
                                    placed_blocks += 1

                    # Match structure load
                    if structure_match := structure_pattern.match(line):
                        color, x_raw, y_raw, z_raw = structure_match.groups()

                        # Convert ~ to 0 for now (or adjust later)
                        def parse_coord(coord):
                            return 0 if coord == "~" else int(coord.replace("~", ""))

                        offset_x = parse_coord(x_raw)
                        offset_y = parse_coord(y_raw)
                        offset_z = parse_coord(z_raw)

                        structure_path = os.path.join(structure_dir, f"{color}.mcstructure")
                        if not os.path.exists(structure_path):
                            print(f"⚠️ Missing structure: {color}.mcstructure")
                            continue

                        blocks = load_mcstructure_blocks(structure_path)
                        for sx, sy, sz, block_id in blocks:
                            schematic.setBlock((offset_x + sx, offset_y + sy, offset_z + sz), block_id)
                            placed_blocks += 1

    schematic.save(".", output_path.split(".schem")[0], mcschematic.Version.JE_1_20_1)
    print(f"✅ Done! Saved schematic as {output_path}")
    print(f"🧱 Blocks placed: {placed_blocks}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert a Minecraft Bedrock mcpack to WorldEdit .schem")
    parser.add_argument("mcpack", help="Path to .mcpack file")
    parser.add_argument("-o", "--output", default="output.schem", help="Output .schem file name")

    args = parser.parse_args()
    parse_mcfunctions(args.mcpack, args.output)
