import os
import btc_utils
import block_query

print("Welcome to create cnf script")
should_query = input("Please enter 'yes' | 'YES' | 'y' if you'd like to query blocks and create a txt file which contains them, or any key if not\n")
if(should_query == 'yes' or should_query == 'YES' or should_query == 'y'):
    block_query.query_blocks()
blocks_file = input("Please enter the name of the file which contains your blocks (!without file extension)\n")
scoin_c = "scoin.c"
nonce_range = input("Please enter the range of the nonces to search, as decimal number (e.g: 1k == 1000, etc...)\n")
nonce_range = int(nonce_range) // 2 # It will encode a nonce range twice this size, as: start = nonce - nonce_range ; end = nonce + nonce_range | If entered 1000 then 1000 // 2 == 500...
directory_name = input("Enter directory name which will contain the generated CNF files (if it doesn't exist, a new dir will be created)\n")

scoin_lines = []
blocks_lines = []
generate_cnf_command = "cbmc " + scoin_c + " -DCBMC --dimacs --outfile {}"

# Lines to replace (starting from 0-based index)
start_line = 216  # Line 217 in the file
end_line = 235  # Line 236 in the file
verify_hash_line = 236 # Line 237 in the file

# Program start
if not os.path.exists(directory_name):
    os.mkdir(directory_name)
    print(f"Directory '{directory_name}' created.")
else:
    print(f"Directory '{directory_name}' already exists.")

# Read the blocks and store them
with open(blocks_file + ".txt", "r") as file:
    blocks_lines = file.readlines()

# Read scoin.c
with open(scoin_c, "r") as file:
    scoin_lines = file.readlines()

for i in range(len(blocks_lines)//20):
    if(len(blocks_lines) < i*20+1): break
    # Change BLOCK and verifyHash in scoin.c
    scoin_lines[start_line:end_line+1] = blocks_lines[i*20:(i+1)*20]
    block_name = blocks_lines[i*20].split(" ")[2]
    block_name = block_name.split("[")[0]
    scoin_lines[verify_hash_line] = "int main(int argc, void *argv[]){verifyhash(&" + block_name + "[0]); return 0;}"

    # Change nonce range assumption - line 126 in scoin.c
    nonce = int(blocks_lines[(i*20)+19].split("}")[0], 0)
    nonce_start = nonce - nonce_range
    nonce_end = nonce + nonce_range
    scoin_lines[125] = "__CPROVER_assume(*u_nonce > " + str(nonce_start) + " && *u_nonce < " + str(nonce_end) + ");\n"

    # Change leading zeros assumption and assertion
    bits_without_0x = blocks_lines[(i*20)+18].split("0x")[1][0:8]
    bits_without_0x_swapped = btc_utils.byteswap_hex_btc_to_little_endian(bits_without_0x)
    number_of_leading_zeros = btc_utils.get_number_of_leading_zeros(bits_without_0x_swapped)
    is_odd_leading_zeros = number_of_leading_zeros % 2 == 1

    assumption_lines = []
    assumption_lines.append("__CPROVER_assume(\n")
    state_element = 7
    state_shift = 0
    for i in range(1, number_of_leading_zeros//2+1):
        current_shift = state_shift * 8
        state_shift += 1
        if(i == number_of_leading_zeros//2-1 and not is_odd_leading_zeros):
            assumption_lines.append("(unsigned char)((state[" + str(state_element) + "] >> " + str(current_shift) + ") & 0xff) == 0x00);\n")
            if(i % 4 == 0):
                state_element -= 1
                state_shift = 0
            break
        elif(i == number_of_leading_zeros//2 and is_odd_leading_zeros):
            assumption_lines.append("(unsigned char)((state[" + str(state_element) + "] >> " + str(current_shift) + ") & 0xff) == 0x00);\n")
        else:
            assumption_lines.append("(unsigned char)((state[" + str(state_element) + "] >> " + str(current_shift) + ") & 0xff) == 0x00 &&\n")
        
        if(i % 4 == 0):
            state_element -= 1
            state_shift = 0

    # add assertion
    assumption_lines.append("int flag = 0;\n")
    current_shift = state_shift * 8
    if(is_odd_leading_zeros):
        assumption_lines.append("if ((unsigned char)(((state[" + str(state_element) + "] >> " + str(current_shift) + ") & 0xff) >> 4 & 0xf) != 0x0)\n")
    else:
        assumption_lines.append("if ((unsigned char)((state[" + str(state_element) + "] >> " + str(current_shift) + ") & 0xff) != 0x00)\n")
    assumption_lines.append("{\n")
    assumption_lines.append("   flag = 1;\n")
    assumption_lines.append("}\n")
    assumption_lines.append("assert(flag == 1);\n")

    j = 0
    for i in range(152, 198):
        if(len(assumption_lines) > j):
            scoin_lines[i] = assumption_lines[j]
            j += 1
            continue
        elif(scoin_lines[i] == "\n"):
            break
        else:
            scoin_lines[i] = "\n"

    
    # Write the new c file back to scoin.c
    with open(scoin_c, "w") as file:
        file.writelines(scoin_lines)
    
    # Execute cnf generation
    btc_utils.execute_command(generate_cnf_command.format(directory_name + "/" + block_name + ".cnf"))


print("CNF files generation ended")