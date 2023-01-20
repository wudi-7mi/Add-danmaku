import argparse
import json
import os

from danmaku_tools.danmaku_tools import read_danmaku_file, get_value

def getxmlstat(path):
  xml_list = read_danmaku_file(path, guard=True)
  total_d = 0
  total_sc = 0
  total_gift = 0
  total_guard = 0
  guard_map = {}

  for item in xml_list:
    if item.tag == 'd':
      total_d += 1
    elif item.tag == 'sc':
      total_sc += get_value(item) * 10
    elif item.tag == 'gift':
      total_gift += get_value(item) * 10
    elif item.tag == 'guard':
      total_guard += get_value(item) * 10
      raw_data = json.loads(item.attrib['raw'])
      gift_name = raw_data['gift_name']
      if gift_name in guard_map:
        guard_map[gift_name] += 1
      else:
        guard_map[gift_name] = 1

  ret_val = {
    'dan': total_d,
    'sc': total_sc,
    'gift': total_gift,
    'guard': total_guard,
    'cate': guard_map,
  }
  print(guard_map)
  return ret_val
  

def getfolderstat(folder_path):
  total_dan = 0
  total_sc = 0
  total_gift = 0
  total_guard = 0
  guard_map = {}
  
  for file in os.listdir(folder_path):
    if file.split('.')[-1] == 'xml':
      file_name = file[:-4]
      xml_path = os.path.abspath(f'{folder_path}/{file_name}.xml')
      res = getxmlstat(xml_path)
      total_dan += res['dan']
      total_sc += res['sc']
      total_gift += res['gift']
      total_guard += res['guard']
      for item in res['cate']:
        if item in guard_map:
          guard_map[item] += res['cate']['item']
        else:
          guard_map[item] = 1
  print(f"弹幕：{total_dan}条")
  print(f"醒目留言：{total_sc}元")
  print(f"礼物：{total_gift}元")
  print(f"大航海：{total_guard}元")
  print(f"大航海类别：{guard_map}")
  print(f"总流水 {total_gift + total_guard + total_sc}元")
  ret_val = {
    'dan': total_dan,
    'sc': total_sc,
    'gift': total_gift,
    'guard': total_guard,
    'cate': guard_map,
  }
  return ret_val
  


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Get gift analytics for BiliBili Live XML')
  parser.add_argument('-folder', type=str, help='path to the danmaku folder')
  
  args = parser.parse_args()
  getfolderstat(args.folder)