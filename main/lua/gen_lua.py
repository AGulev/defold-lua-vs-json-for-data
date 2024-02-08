import random
import os
import string

def generate_random_slices():
    num_slices = random.randint(5, 20)  # Randomize the number of slices
    return [round(random.uniform(0, 1), 2) for _ in range(num_slices * 2)]

def generate_random_name(length):
    # Generates a random string of the given length
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def generate_random_tile():
    return {
        generate_random_name(11): round(random.uniform(-5, 5), 2),  # go_x_offset
        generate_random_name(11): round(random.uniform(0, 200), 2),  # go_y_offset
        generate_random_name(9): round(random.uniform(1, 4), 2),  # hor_scale
        generate_random_name(15): 1,  # obj_cells_width
        generate_random_name(16): 1,  # obj_cells_height
        generate_random_name(11): f"resource_{random.randint(1000, 9999)}",  # resource_id
        generate_random_name(8): f"filename_{random.randint(1000, 9999)}",  # filename
        generate_random_name(12): random.randint(100, 600),  # sprite_width
        generate_random_name(13): random.randint(100, 400),  # sprite_height
        generate_random_name(6): generate_random_slices()  # slices
    }

def dict_to_lua_table(d):
    lua_table = "{\n"
    for key, value in d.items():
        lua_table += f"\t{key} = {dict_to_lua_value(value)},\n"
    lua_table += "}"
    return lua_table

def dict_to_lua_value(value):
    if isinstance(value, dict):
        return dict_to_lua_table(value)
    elif isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, list):
        return "{" + ", ".join(str(v) for v in value) + "}"
    else:
        return str(value)

def write_lua_file(target_size_kb):
    tiles = {}
    iteration = 0
    while True:  # Use a break condition inside the loop
        tile_name = f"tile_{random.randint(1000, 9999)}"
        tiles[tile_name] = generate_random_tile()
        
        # Serialize a simplified version of the tiles dictionary to Lua table format
        lua_content = f"local M = {{\n\ttiles = {dict_to_lua_table(tiles)}\n}}\n\nreturn M"

        with open("output.lua", "w") as file:
            file.write(lua_content)
            file.flush()  # Ensure content is flushed to disk
            os.fsync(file.fileno())  # Ensure OS flushes write buffers to disk

        current_size = os.path.getsize("output.lua")
        if current_size >= target_size_kb * 1024:  # Check if current size meets target
            break

        iteration += 1
        if iteration % 10 == 0:
            print(f"Current iteration: {iteration}, file size: {current_size / 1024:.2f} KB")

    return f"Generated Lua file 'output.lua' with size: {current_size / 1024:.2f} KB"


# Example usage:
target_size_kb = 8926.67  # Target size in KB
print(write_lua_file(target_size_kb))
