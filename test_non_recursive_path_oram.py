from non_recursive_path_oram import PathOramClient, PathOramServer
import os
from math import log
import time

test_dataset = 'imdb/neg'
# test initialize
# load content in dataset
files_list = os.listdir(test_dataset)
max_file_size = len(files_list)
file_size = 500
if file_size > max_file_size:
    raise Exception("file size should not be larger than max file size")
contents = []
file_block_map = dict()
for i, file_name in enumerate(files_list):
    f = open(os.path.join(test_dataset, file_name), 'rb')
    data = f.read()
    contents.append((i, data))
    file_block_map[files_list[i]] = i
    f.close()

    if i == file_size:
        break

# initialize oram
# decide level of oram
total_file_number = len(contents)
level = log(total_file_number, 2)
if level != int(level):
    level += 1
level = int(level)

print("total files", total_file_number)
print("level of oram", level)

start = time.time()
client = PathOramClient(level)
# generate dummy block
dummy_buckets = client.generate_initialize_block()
server = PathOramServer(dummy_buckets, level)
end = time.time()
print("time of initialize with dummy", end - start, 's')

start = time.time()
# write content to oram and record map between file and block_id
for i, content in enumerate(contents):
    block_id = content[0]
    data = content[1]
    client.write(block_id, data, server)
end = time.time()
print("time of write all content", end - start, "s")
print("average of write time", (end-start)/len(contents),"s")

# test first time read
start = time.time()
for content in contents:
    block_id = content[0]
    data = content[1]
    read_data = client.read(block_id, server)
    if data!=read_data:
        print("program error","can not read write data")
        print("original data:\n",data)
        print("data from oram:\n",read_data)
        raise Exception("")
end = time.time()
print("time of read all content", end-start, "s")
print("average time", (end-start)/len(contents), "s")

# test second time read

start = time.time()
for content in contents:
    block_id = content[0]
    data = content[1]
    read_data = client.read(block_id, server)
    if data!=read_data:
        print("program error","can not read write data")
        print("original data:\n",data)
        print("data from oram:\n",read_data)
        raise Exception("")
end = time.time()
print("second time of read all content", end-start, "s")
print("second average time", (end-start)/len(contents), "s")