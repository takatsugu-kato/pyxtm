import requests
import json
from datetime import datetime

class APIException(Exception):
    """API Exception"""
    def __init__(self, message):
        self.message = message

class ReqMethod():
    POST = "post"
    GET = "get"

class LQAType():
    LANGUAGE = "LANGUAGE"
    FILE = "FILE"

class FilesScopeType():
    JOB = "JOB"
    PROJECT = "PROJECT"

class FetchTargetFileType():
    NO_CONTENT = "NO_CONTENT"
    NON_ANALYSABLE = "NON_ANALYSABLE"
    NOT_SUPPORTED = "NOT_SUPPORTED"

class FileNameFilterType():
    CONTAINS = "CONTAINS"
    EQUALS = "EQUALS"
    STARTS_WITH = "STARTS_WITH"
    ENDS_WITH = "ENDS_WITH"

class FileType():
    TARGET = "TARGET"
    XLIFF = "XLIFF"
    XLIFF_NTP = "XLIFF_NTP"
    QA_REPORT = "QA_REPORT"
    HTML = "HTML"
    HTML_TABLE = "HTML_TABLE"
    PDF = "PDF"
    PDF_TABLE = "PDF_TABLE"
    TIPP = "TIPP"
    HTML_EXTENDED_TABLE = "HTML_EXTENDED_TABLE"
    HTML_COLOURED = "HTML_COLOURED"
    HTML_COLOURED_BY_MATCH_RATE = "HTML_COLOURED_BY_MATCH_RATE"
    PDF_EXTENDED_TABLE = "PDF_EXTENDED_TABLE"
    PDF_COLOURED = "PDF_COLOURED"
    PDF_COLOURED_BY_XLIFF_DOC_STATUS = "PDF_COLOURED_BY_XLIFF_DOC_STATUS"
    PDF_COLOURED_BY_MATCH_RATE = "PDF_COLOURED_BY_MATCH_RATE"
    TARGET_COLOURED_BY_MATCH_RATE = "TARGET_COLOURED_BY_MATCH_RATE"
    TARGET_COLOURED_BY_XLIFF_DOC_STATUS = "TARGET_COLOURED_BY_XLIFF_DOC_STATUS"
    XLIFF_DOC = "XLIFF_DOC"
    LQA_REPORT = "LQA_REPORT"
    LQA_EXTENDED_TABLE_REPORT = "LQA_EXTENDED_TABLE_REPORT"
    TARGET_PSEUDO = "TARGET_PSEUDO"
    MULTI_EXCEL = "MULTI_EXCEL"
    EXCEL_EXTENDED_TABLE = "EXCEL_EXTENDED_TABLE"

class XtmClient:
    def __init__(self, client_name:str, useid:int, password:str):
        self.token = ""
        self.token = self.__generate_token(client_name, useid, password)

    def obtain_project(self, project_id:int) -> dict:
        url = f"https://www.xtm-cloud.com/project-manager-api-rest/projects/{project_id}"
        return self.__call_rest(url, ReqMethod.GET)

    def obtain_project_lqa(self, project_ids:list, target_languages:list=None, evaluee_ids:list=None, workflow_step_ids:list=None, evaluator_ids:list=None, lqa_type:LQAType=None) -> dict:
        url = "https://www.xtm-cloud.com/project-manager-api-rest/projects/lqa"
        params = {
            "projectIds": project_ids,
            "targetLanguages": target_languages,
            "evalueeIds": evaluee_ids,
            "workflowStepIds": workflow_step_ids,
            "evaluatorIds": evaluator_ids,
            "type": lqa_type
        }

        return self.__call_rest(url, ReqMethod.GET, params=params)

    def download_project_lqa(self, project_ids:list, report_id:int=None, target_languages:list=None, evaluee_ids:list=None, workflow_step_ids:list=None, evaluator_ids:list=None, lqa_type:LQAType=None, complete_date_from:datetime=None, complete_date_to:datetime=None):
        url = "https://www.xtm-cloud.com/project-manager-api-rest/projects/lqa/download"
        params = {
            "reportID": report_id,
            "projectIds": project_ids,
            "targetLanguages": target_languages,
            "evalueeIds": evaluee_ids,
            "evaluatorIds": evaluator_ids,
            "workflowStepIds": workflow_step_ids,
            "completeDateFrom": complete_date_from,
            "completeDateTo": complete_date_to,
            "type": lqa_type,
        }
        return self.__call_rest(url, ReqMethod.GET, params=params)

    def download_project_files(self,
        project_id:int,
        file_type:FileType,
        file_scope:FilesScopeType=FilesScopeType.JOB,
        fetch_target_file_types:list=None,
        file_ids:list=None,
        file_name_filter:str=None,
        file_name_filter_type:FileNameFilterType=None,
        job_ids:list=None,
        target_languages:list=None,
    ):
        url = f"https://www.xtm-cloud.com/project-manager-api-rest/projects/{project_id}/files/download"
        params = {
            "fetchTargetFileTypes": fetch_target_file_types,
            "fileIds": file_ids,
            "fileNameFilter": file_name_filter,
            "fileNameFilterType": file_name_filter_type,
            "fileScope": file_scope,
            "fileType": file_type,
            "jobIds": job_ids,
            "targetLanguages": target_languages,
        }
        return self.__call_rest(url, ReqMethod.GET, params=params)

    def download_project_file(self, project_id, file_id, file_scope):
        url = f"https://www.xtm-cloud.com/project-manager-api-rest/projects/{project_id}/files/{file_id}/download"
        params = {
            "fileScope": file_scope
        }
        return self.__call_rest(url, ReqMethod.GET, params=params)

    def __generate_token(self, client_name:str, useid:int, password:str) -> str:
        url = "https://www.xtm-cloud.com/project-manager-api-rest/auth/token"
        payload = {
            "client" : client_name,
            "password" : password,
            "userId" : useid
        }
        res = self.__call_rest(url, ReqMethod.POST, payload)
        return res['token']

    def __call_rest(self, url:str, method:ReqMethod, body:dict=None, params:dict=None) -> dict:
        headers = {"Content-Type" : "application/json"}

        if self.token:
            headers["Authorization"] = f'XTM-Basic {self.token}'

        body = json.dumps(body).encode("utf-8")
        if method == ReqMethod.POST:
            result = requests.post(url, headers=headers, data=body, timeout=60)
        elif method == ReqMethod.GET:
            result = requests.get(url, headers=headers, data=body, params=params, timeout=60)
        else:
            raise ValueError(f"Unsupported request method: {method}")

        if result.status_code == 404:
            raise APIException(result.reason)
        if result.status_code != 200:
            raise APIException(json.loads(result.text))

        content_type = result.headers.get('Content-Type', '')
        if 'application/octet-stream' in content_type:
            return result.content
        return json.loads(result.text)
