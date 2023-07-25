#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@File:     tencent_docs.py
@Time:     2022/7/12 17:34
@Author:   claudexie
@Software: PyCharm
"""
import os
import requests
import json


COLUMN = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
          'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO',
          'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ', 'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG',
          'BH', 'BI', 'BJ', 'BK', 'BL', 'BM', 'BN', 'BO', 'BP', 'BQ', 'BR', 'BS', 'BT', 'BU', 'BV', 'BW', 'BX', 'BY',
          'BZ', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'CG', 'CH', 'CI', 'CJ', 'CK', 'CL', 'CM', 'CN', 'CO', 'CP', 'CQ',
          'CR', 'CS', 'CT', 'CU', 'CV', 'CW']


def get_docs_operator():
    """
    获取腾讯文档的操作对象
    :return:
    """
    # 获取腾讯文档鉴权
    tencent_docs_token = os.environ.get("TENCENT_DOCS_TOKEN")
    try:
        docs = TencentDocs(token=tencent_docs_token)
    except Exception as error:  # pylint: disable=broad-except
        print(f"{error}， token: {tencent_docs_token} 无效，重新获取...")
        docs = TencentDocs()
    os.environ['TENCENT_DOCS_TOKEN'] = docs.token
    return docs


class TencentDocs(object):
    """
    获取控制器注册的专区、设备、设备组和资源组相关数据的类（运维相关）
    """

    def __init__(self, token: str = None):
        self.headers = {"Content-Type": "application/json"}
        # 授权码，有效时间为5分钟，且只能使用一次
        client_id = '62daceac49b5443ca98e27dd0f5fb464'
        client_secret = os.environ.get('TENCENT_DOCS_SECRET')
        refresh_token = os.environ.get('TENCENT_DOCS_REFRESH_TOKEN')
        if not token:
            token = TencentDocs.get_refresh_token(client_id, client_secret, refresh_token)
        else:
            pass
        # 验证token
        user_info = TencentDocs.get_user_info(token)
        if not user_info.get('data'):
            raise Exception(str(user_info))
        self.token = token
        self.headers['Access-Token'] = token
        self.headers['Client-Id'] = client_id
        self.headers['Open-Id'] = user_info['data']['openID']

    @staticmethod
    def _oauth_request(url_path: str):
        """
        授权接口调用
        """
        url = f"https://docs.qq.com{url_path}"
        print(f"GET {url} ")
        response = requests.get(url)
        if response.status_code == 200:
            rev_data = response.json()
            print(f"Response: {rev_data}")
            return rev_data
        else:
            raise Exception(f"{url} failed: {str(response.content)}")

    def _request(self, url_path: str, payload: dict = None, request_type: str = "GET"):
        """
        调用腾讯文档API的公共方法
        :return:
        """
        url = f"https://docs.qq.com{url_path}"
        print(f"{request_type} {url} {payload}")
        if request_type.upper() == 'GET':
            response = requests.get(url, headers=self.headers, params=json.dumps(payload))
        elif request_type.upper() == 'POST':
            response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        elif request_type.upper() == 'PUT':
            response = requests.put(url, headers=self.headers, data=json.dumps(payload))
        elif request_type.upper() == 'DELETE':
            response = requests.delete(url, headers=self.headers, data=json.dumps(payload))
        elif request_type.upper() == 'PATCH':
            response = requests.patch(url, headers=self.headers, data=json.dumps(payload))
        else:
            raise NotImplementedError(f"Unknown request type: {request_type}")
        if response.status_code == 200:
            rev_data = response.json()
            print(f"header: {response.headers}")
            print(f"Response: {rev_data}")
            return rev_data
        else:
            raise Exception(f"{url} failed: {str(response.content)}")

    @staticmethod
    def get_token(client_id: str, client_secret: str, code: str):
        """
        本接口用于通过授权码获取 Access Token 和 Refresh Token。(需要提前手动收取获取code后才能执行)
        :return:
        """
        return TencentDocs._oauth_request(f"/oauth/v2/token?client_id={client_id}&client_secret={client_secret}"
                                          f"&redirect_uri=https%3a%2f%2ftest.airflow.noc.woa.com"
                                          f"&grant_type=authorization_code&code={code}")

    @staticmethod
    def get_user_info(token: str):
        """
        本接口用于获取用户信息，同时也可以用来校验AccessToken的有效性。
        :return:
        """
        return TencentDocs._oauth_request(f"/oauth/v2/userinfo?access_token={token}")

    @staticmethod
    def get_refresh_token(client_id: str, client_secret: str, refresh_token: str):
        """
        本接口用于刷新 Access Token（30天内必须刷新一次）
        :return:
        """
        return TencentDocs._oauth_request(f"/oauth/v2/token?client_id={client_id}&client_secret={client_secret}"
                                          f"&grant_type=refresh_token&refresh_token={refresh_token}")['access_token']

    def create_file(self, title: str = "我是没有名字的文档", file_type: str = "sheet"):
        """
        本接口用于新建一个文档。
        :return:
        """
        payload = {
            "title": title,
            "type": file_type
        }
        return self._request("/openapi/drive/v2/files", payload=payload, request_type='POST')['data']

    def create_file_with_write_policy(self, title: str = "我是没有名字的文档", file_type: str = "sheet",
                                      policy: str = "publicWrite"):
        """
        本接口用于新建一个文档。
        :return:
        """
        print(f'creating file...')
        file_info = self.create_file(title=title, file_type=file_type)
        print(f'created file')
        # 开启全部人可编辑权限
        payload = {
            "policy": policy,
        }
        print(f'changing file policy...')
        self._request(f"/openapi/drive/v2/files/{file_info['ID']}/permission", payload=payload, request_type='PATCH')
        print(f'changed file policy')
        return file_info

    def change_file_name(self, file_id, new_title):
        """
        本接口用于更新文档，目前仅限于重命名。
        :param file_id:
        :param new_title:
        :return:
        """
        payload = {
            "title": new_title,
        }
        return self._request(f"/openapi/drive/v2/files/{file_id}", payload=payload, request_type='PATCH')

    def get_file_info(self, file_id: str):
        """
        本接口用于根据文档ID进行查询，返回文档的信息
        :return:
        """
        return self._request(f"/openapi/drive/v2/files/{file_id}/metadata")['data']

    def get_sheet_info(self, file_id: str):
        """
        本接口用于查询一篇在线表格中全部工作表信息。
        :param file_id:
        :return:
        """
        return self._request(f"/openapi/sheetbook/v2/{file_id}/sheets-info")['data']['sheetData']

    def tansform_fileid_and_encodedid(self, file_encoded_id: str, typenum: int = 2):
        """
        apolloxu补充
        本接口用于支持 fileID 与 encodedID 相互转换。
        1、从新建文档接口的返回值中获取到文档的 fileID。
        2、从查询导入进度接口的返回值中获取到文档的 fileID。
        3、从下面的一个文件为结果的链接中获取 encodedID：
        https://docs.qq.com/doc/DAAAAAAAAAAAA
        typenum转换类型
        1：fileID 转 encodedID
        2：encodedID 转 fileID
        """
        url = f"/openapi/drive/v2/util/converter?type={typenum}&value={file_encoded_id}"
        return self._request(url)['data']['fileID']

    def add_new_sheet(self, file_id: str, sheet_name: str, sheet_index: int = 0,
                      row_count: int = 250, column_count: int = 26):
        """
        新增一个sheet页面
        :param file_id:
        :param sheet_name:
        :param sheet_index:
        :param row_count:
        :param column_count:
        :return: sheet_id
        """
        # 开启全部人可编辑权限
        payload = {
            "addSheet": {
                "properties": {
                    "title": sheet_name,
                    "index": sheet_index,
                    "gridProperties": {
                        "rowCount": row_count,
                        "columnCount": column_count
                    }
                }
            }
        }
        print(f'adding new sheet ({sheet_name})...')
        data = self._request(f"/openapi/sheetbook/v2/{file_id}:batchUpdate", payload=payload,
                             request_type='POST')
        return data['data']['addSheet']['properties']['sheetID']

    def get_sheet_cell_data(self, file_id: str, sheet_id: str, cells: str):
        """
        获取在线表格内指定工作表中单元格的文本内容，可批量获取多个单元格的内容
        :param cells: 逗号分割
        :param file_id:
        :param sheet_id:
        :return:
        """
        return self._request(f"/openapi/sheetbook/v2/{file_id}/sheets/{sheet_id}"
                             f"?request=GetCells&cells={cells}")['data']

    def append_raw(self, file_id: str, sheet_id: str, raw_data: list):
        """
        在在线表格的最后一行添加一行内容
        :param file_id:
        :param sheet_id:
        :param raw_data:
        :return:
        """
        payload = {"appendRow": raw_data}
        return self._request(f"/openapi/sheetbook/v2/{file_id}/sheets/{sheet_id}",
                             payload=payload, request_type='POST')['data']

    def append_lines(self, file_id: str, sheet_id: str, line_list: list):
        """
        在在线表格的最后一行添加n行内容
        :param file_id:
        :param sheet_id:
        :param line_list:
        :return:
        """
        print(f"adding {len(line_list)} line to {file_id}: {sheet_id}")
        update_cells = {}
        sheet_list = self.get_sheet_info(file_id)
        current_row_count = 0
        for sheet_info in sheet_list:
            if sheet_info['sheetID'] == sheet_id:
                current_row_count = sheet_info['rowCount']
                break
        start_raw_index = current_row_count + 1
        for line in line_list:
            for index in range(0, len(line)):
                update_cells[f"{COLUMN[index]}{start_raw_index}"] = line[index]
            start_raw_index += 1
        self.update_cell(file_id, sheet_id, update_cells)

    def get_row_data(self, file_id: str, sheet_id: str, rows: str):
        """
        获取在线表格内工作表中指定行中的单元格文本内容，可批量获取多行的内容
        :param file_id:
        :param sheet_id:
        :param rows: 想要获取指定行的行号，使用逗号进行分割，A-B表示从第A行到第B行
        如5,7-10表示获取第5、7、8、9、10这五行中的单元格的内容
        :return:
        """
        return self._request(f"/openapi/sheetbook/v2/{file_id}/sheets/{sheet_id}"
                             f"?request=GetRows&rows={rows}")['data']['rows']

    def get_large_row_data(self, file_id: str, sheet_id: str, rows: str):
        """
        获取在线表格内工作表中指定行中的单元格文本内容，可批量获取多行的内容
        :param file_id:
        :param sheet_id:
        :param rows: 想要获取指定行的行号，使用逗号进行分割，A-B表示从第A行到第B行
        如5,7-10表示获取第5、7、8、9、10这五行中的单元格的内容
        :return:
        """
        start_row = int(rows.split('-')[0])
        end_row = int(rows.split('-')[1])
        data_list = []
        if int(end_row) - int(start_row) > 3000:
            for index in range(start_row, start_row, 3000):
                tem_start_row = index
                tem_end_row = index + 2999
                if tem_end_row > end_row:
                    tem_end_row = end_row
                else:
                    pass
                print(f"{tem_start_row}-{tem_end_row}")
                data = self._request(f"/openapi/sheetbook/v2/{file_id}/sheets/{sheet_id}"
                                     f"?request=GetRows&rows={rows}")['data']['rows']
                data_list.extend(data)
            return data_list
        else:
            return self._request(f"/openapi/sheetbook/v2/{file_id}/sheets/{sheet_id}"
                                 f"?request=GetRows&rows={rows}")['data']['rows']

    def update_cell(self, file_id: str, sheet_id: str, update_cells: dict):
        """
        更新在线表格内指定单元格的文本内容，可批量更新多个单元格的内容
        :param file_id:
        :param sheet_id:
        :param update_cells:
        :return:
        """
        payload = {"updateCells": update_cells}
        return self._request(f"/openapi/sheetbook/v2/{file_id}/sheets/{sheet_id}",
                             payload=payload, request_type='POST')

    def clear_area(self, file_id: str, sheet_id: str, range: str):
        """
        清空区域的内容
        :param file_id:
        :param sheet_id:
        :param range: A1:C3，表示工作表ID是BB0000的左上角的3X3的区域
        :return:
        """
        return self._request(f"/openapi/sheetbook/v2/{file_id}/values/{sheet_id}!{range}:clear", request_type='POST')

    def update_ares(self, file_id: str, sheet_id: str, range: str, values: list):
        """
        更新区域的内容
        :param file_id:
        :param sheet_id:
        :param range: A1:C3，表示工作表ID是BB0000的左上角的3X3的区域
        :param values: [[1], [2]]
        :return:
        """
        payload = {"values": values}
        return self._request(f"/openapi/sheetbook/v2/{file_id}/values/{sheet_id}!{range}", payload, request_type='PUT')


# Testing
if __name__ == '__main__':
    token = ""
    docs = TencentDocs(token)
    #docs.create_file_with_write_policy()
    # 300000000$NLrsOYBdnaed
    # docs.add_new_sheet('300000000$NPpAzxSMZMmB', "new")
    # print(docs.change_file_name('300000000$NLrsOYBdnaed', "深圳网球场预定信息动态表格"))
    print(docs.get_file_info('300000000$NLrsOYBdnaed'))
    print(docs.get_sheet_info('300000000$NLrsOYBdnaed'))
    # print(docs.append_raw("300000000$NLrsOYBdnaed", "BB08J2", ["123", "test"]))
    # docs.get_row_data("300000000$NLrsOYBdnaed", "BB08J2", "1-10")
    docs.update_cell("300000000$NLrsOYBdnaed", "BB08J2", {"C10": "大沙河\n深云文体\n深圳湾\n香蜜体育\n莲花体育\n简上"
                                                                 "\n黄木岗\n华侨城\n福田中心\n黄冈公园\n北站公园"
                                                                 "\n金地威新\n泰尼斯香蜜\n总裁俱乐部\n郑洁俱乐部"})
