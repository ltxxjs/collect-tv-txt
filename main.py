import urllib.request
import re #正则

# 定义要访问的多个URL
urls = [
    'https://m3u.ibert.me/txt/fmml_ipv6.txt',
    'https://m3u.ibert.me/txt/ycl_iptv.txt',
    'https://m3u.ibert.me/txt/y_g.txt'
]

# 定义多个对象用于存储不同内容的行文本
ys_lines = []
ws_lines = []
ty_lines = []
# favorite_lines = []

other_lines = []

ys_lines.append("央视频道,#genre#")
ws_lines.append("卫视频道,#genre#")
ty_lines.append("体育频道,#genre#")


def process_name_string(input_str):
    parts = input_str.split(',')
    processed_parts = []
    for part in parts:
        processed_part = process_part(part)
        processed_parts.append(processed_part)
    result_str = ','.join(processed_parts)
    return result_str

def process_part(part_str):
    # 处理逻辑
    if "CCTV" in part_str:
        part_str=part_str.replace("IPV6", "")  #先剔除IPV6字样
        filtered_str = ''.join(char for char in part_str if char.isdigit() or char == 'K')
        return "CCTV-"+filtered_str
        # pattern = r'CCTV-(\d+)([+\d]*).*'  # 匹配CCTV-数字后可能有+和数字_任意字符
        # #pattern = r'CCTV-(\d+)[+\d]*[「"“].*'
        # match = re.match(pattern, part_str)
        # if match:
        #     number = match.group(1)
        #     plus_part = match.group(2)
        #     modified_str = f"CCTV-{number}"
        #     if plus_part and (plus_part[0] == '+' or plus_part.isdigit()):
        #         modified_str += '+'
        #     return modified_str
    elif "卫视" in part_str:
        # 定义正则表达式模式，匹配“卫视”后面的内容
        pattern = r'卫视「.*」'
        # 使用sub函数替换匹配的内容为空字符串
        result_str = re.sub(pattern, '卫视', part_str)
        return result_str
    
    return part_str

def process_url(url):
    try:
        # 打开URL并读取内容
        with urllib.request.urlopen(url) as response:
            # 以二进制方式读取数据
            data = response.read()
            # 将二进制数据解码为字符串
            text = data.decode('utf-8')
            
            # 逐行处理内容
            lines = text.split('\n')
            for line in lines:
                if  "#genre#" not in line:
                    # 根据行内容判断存入哪个对象
                    if "CCTV" in line:
                        ys_lines.append(process_name_string(line.strip()))
                    elif "卫视" in line:
                        ws_lines.append(process_name_string(line.strip()))
                    elif "体育" in line:
                        ty_lines.append(process_name_string(line.strip()))
                    # elif "电影" in line:
                    #     obj3_lines.append(line.strip())
                    else:
                        other_lines.append(line.strip())
    except Exception as e:
        print(f"处理URL时发生错误：{e}")

# 循环处理每个URL
for url in urls:
    print(f"处理URL: {url}")
    process_url(url)

# 合并所有对象中的行文本
all_lines = ys_lines + ['\n'] + ws_lines + ['\n'] + ty_lines

# 将合并后的文本写入文件
output_file = "merged_output.txt"
others_file = "others_output.txt"
try:
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in all_lines:
            f.write(line + '\n')
    print(f"合并后的文本已保存到文件: {output_file}")

    with open(others_file, 'w', encoding='utf-8') as f:
        for line in other_lines:
            f.write(line + '\n')
    print(f"Others已保存到文件: {others_file}")

except Exception as e:
    print(f"保存文件时发生错误：{e}")