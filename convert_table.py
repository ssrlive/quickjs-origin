import re
import os

def convert_table():
    input_path = r"c:\Users\Administrator\Desktop\quickjs\libunicode-table.h"
    output_path = r"c:\Users\Administrator\Desktop\quickjs\rust_quickjs\src\libunicode_table.rs"
    
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("#![allow(dead_code)]\n")
        f.write("#![allow(non_upper_case_globals)]\n\n")
        
        for line in lines:
            line = line.rstrip()
            if line.startswith("#"):
                continue
            if line.strip() == "":
                f.write("\n")
                continue
                
            # Match array declaration
            # static const uint32_t case_conv_table1[378] = {
            match = re.match(r'static\s+const\s+(\w+)\s+(\w+)\[(\d*)\]\s*=\s*\{', line)
            if match:
                ctype = match.group(1)
                name = match.group(2)
                size = match.group(3)
                
                rust_type = "u32"
                if ctype == "uint32_t":
                    rust_type = "u32"
                elif ctype == "uint16_t":
                    rust_type = "u16"
                elif ctype == "uint8_t":
                    rust_type = "u8"
                elif ctype == "int32_t":
                    rust_type = "i32"
                elif ctype == "int16_t":
                    rust_type = "i16"
                elif ctype == "int8_t":
                    rust_type = "i8"
                
                rust_name = name.upper()
                
                if size:
                    f.write(f"pub const {rust_name}: [{rust_type}; {size}] = [\n")
                else:
                    # If size is missing, we might have a problem. 
                    # But looking at the file, they seem to have sizes.
                    # If not, we'd need to count elements.
                    # For now, let's assume size is there or handle it manually if it fails.
                    f.write(f"pub const {rust_name}: [{rust_type}; _] = [\n") 
            elif line == "};":
                f.write("];\n")
            else:
                # Data lines
                f.write(line + "\n")

if __name__ == "__main__":
    convert_table()
