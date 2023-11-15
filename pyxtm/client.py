"""XTM Client"""
import json
from datetime import datetime
import requests

class APIException(Exception):
    """API Exception"""
    def __init__(self, message):
        self.message = message

class ReqMethod():
    """Request Method"""
    POST = "post"
    GET = "get"

class LQAType():
    """LQAType"""
    LANGUAGE = "LANGUAGE"
    FILE = "FILE"

class FilesScopeType():
    """FilesScopeType"""
    JOB = "JOB"
    PROJECT = "PROJECT"

class FetchTargetFileType():
    """FetchTargetFileType"""
    NO_CONTENT = "NO_CONTENT"
    NON_ANALYSABLE = "NON_ANALYSABLE"
    NOT_SUPPORTED = "NOT_SUPPORTED"

class FileNameFilterType():
    """FileNameFilterType"""
    CONTAINS = "CONTAINS"
    EQUALS = "EQUALS"
    STARTS_WITH = "STARTS_WITH"
    ENDS_WITH = "ENDS_WITH"

class FileType():
    """FileType"""
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
    """XtmClient class"""
    def __init__(self, client_name:str, user_id:int, password:str):
        self.token = ""
        self.token = self.__generate_token(client_name, user_id, password)

    def obtain_project(self, project_id:int) -> dict:
        """Obtain project

        Args:
            project_id (int): Project ID

        Returns:
            dict: https://www.xtm-cloud.com/rest-api/#tag/Projects/operation/getProject
        """
        url = f"https://www.xtm-cloud.com/project-manager-api-rest/projects/{project_id}"
        return self.__call_rest(url, ReqMethod.GET)

    def obtain_project_lqa(
        self,
        project_ids:list,
        target_languages:list=None,
        evaluee_ids:list=None,
        workflow_step_ids:list=None,
        evaluator_ids:list=None,
        lqa_type:LQAType=None
    ) -> dict:
        """Obtain project LQA

        Args:
            project_ids (list): Project IDs
            target_languages (list, optional): target_languages. Defaults to None.
            evaluee_ids (list, optional): evaluee_ids. Defaults to None.
            workflow_step_ids (list, optional): workflow_step_ids. Defaults to None.
            evaluator_ids (list, optional): evaluator_ids. Defaults to None.
            lqa_type (LQAType, optional): lqa_type. Defaults to None.

        Returns:
            dict: https://www.xtm-cloud.com/rest-api/#tag/Project-LQA/operation/getLqa
        """
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

    def generate_specific_files(
        self,
        project_id:int,
        file_type:FileType,
        job_ids:list=None,
        target_language:str=None
    ) -> dict:
        """Generate specific files

        Args:
            project_id (int): Project ID
            file_type (FileType): file_type
            job_ids (list, optional): job_ids. Defaults to None.
            target_language (str, optional): target_language. Defaults to None.

        Returns:
            dict: https://www.xtm-cloud.com/rest-api/#tag/Project-files/operation/generateFiles
        """
        url = f"https://www.xtm-cloud.com/project-manager-api-rest/projects/{project_id}/files/generate"
        params = {
            "fileType": file_type,
            "jobIds": job_ids,
            "targetLanguage": target_language,
        }
        return self.__call_rest(url, ReqMethod.POST, params=params)

    def obtain_status_of_generated_file(
        self,
        file_id:int,
        project_id:int,
        file_scope:FilesScopeType=FilesScopeType.JOB,
    ) -> dict:
        """Obtain status of generated file

        Args:
            file_id (int): File ID
            project_id (int): project_id
            file_scope (FilesScopeType, optional): file_scope. Defaults to FilesScopeType.JOB.

        Returns:
            dict: https://www.xtm-cloud.com/rest-api/#tag/Project-files/operation/fileStatus
        """
        url = f"https://www.xtm-cloud.com/project-manager-api-rest/projects/{project_id}/files/{file_id}/status"
        params = {
            "fileScope": file_scope,
        }
        return self.__call_rest(url, ReqMethod.GET, params=params)

    def download_project_lqa(
        self,
        project_ids:list,
        report_id:int=None,
        target_languages:list=None,
        evaluee_ids:list=None,
        workflow_step_ids:list=None,
        evaluator_ids:list=None,
        lqa_type:LQAType=None,
        complete_date_from:datetime=None,
        complete_date_to:datetime=None
    ) -> dict:
        """Download project LQA

        Args:
            project_ids (list): project_ids
            report_id (int, optional): report_id. Defaults to None.
            target_languages (list, optional): target_languages. Defaults to None.
            evaluee_ids (list, optional): evaluee_ids. Defaults to None.
            workflow_step_ids (list, optional): workflow_step_ids. Defaults to None.
            evaluator_ids (list, optional): evaluator_ids. Defaults to None.
            lqa_type (LQAType, optional): lqa_type. Defaults to None.
            complete_date_from (datetime, optional): complete_date_from. Defaults to None.
            complete_date_to (datetime, optional): complete_date_to. Defaults to None.

        Returns:
            dict: https://www.xtm-cloud.com/rest-api/#tag/Project-LQA/operation/downloadLqa
        """
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

    def download_project_files(
        self,
        project_id:int,
        file_type:FileType,
        file_scope:FilesScopeType=FilesScopeType.JOB,
        fetch_target_file_types:list=None,
        file_ids:list=None,
        file_name_filter:str=None,
        file_name_filter_type:FileNameFilterType=None,
        job_ids:list=None,
        target_languages:list=None,
    ) -> str:
        """Download project files

        Args:
            project_id (int): project_id
            file_type (FileType): file_type
            file_scope (FilesScopeType, optional): file_scope. Defaults to FilesScopeType.JOB.
            fetch_target_file_types (list, optional): fetch_target_file_types. Defaults to None.
            file_ids (list, optional): file_ids. Defaults to None.
            file_name_filter (str, optional): file_name_filter. Defaults to None.
            file_name_filter_type (FileNameFilterType, optional): file_name_filter_type. Defaults to None.
            job_ids (list, optional): job_ids. Defaults to None.
            target_languages (list, optional): target_languages. Defaults to None.

        Returns:
            binaly data: The response is generated in the application/octet-stream format as a ZIP file.
        """
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

    def download_project_file(self, project_id:int, file_id:int, file_scope:FilesScopeType=FilesScopeType.JOB) -> str:
        """Download project file

        Args:
            project_id (int): project_id
            file_id (int): file_id
            file_scope (FilesScopeType, optional): file_scope. Defaults to FilesScopeType.JOB.

        Returns:
            binaly data: The response is generated in the application/octet-stream format as a target extension file (xlsx, xliff).
        """
        url = f"https://www.xtm-cloud.com/project-manager-api-rest/projects/{project_id}/files/{file_id}/download"
        params = {
            "fileScope": file_scope
        }
        return self.__call_rest(url, ReqMethod.GET, params=params)

    def wait_for_file_completion(
        self,
        file_id: int,
        project_id: int,
        file_scope: FilesScopeType = FilesScopeType.JOB,
        max_attempts: int = 10,
    ) -> dict:
        for _ in range(max_attempts):
            status_response = self.obtain_status_of_generated_file(file_id, project_id, file_scope)
            status = status_response.get("status")

            if status == "FINISHED":
                return status_response

        raise APIException(f"File status did not reach 'FINISHED' after {max_attempts} attempts.")

    def __generate_token(self, client_name:str, user_id:int, password:str) -> str:
        """__generate_token

        Args:
            client_name (str): client_name
            user_id (int): user_id
            password (str): password

        Returns:
            str: token
        """
        url = "https://www.xtm-cloud.com/project-manager-api-rest/auth/token"
        payload = {
            "client" : client_name,
            "password" : password,
            "userId" : user_id
        }
        res = self.__call_rest(url, ReqMethod.POST, payload)
        return res['token']

    def __call_rest(self, url:str, method:ReqMethod, body:dict=None, params:dict=None) -> dict:
        """__call_rest

        Args:
            url (str): url
            method (ReqMethod): method
            body (dict, optional): body. Defaults to None.
            params (dict, optional): params. Defaults to None.

        Raises:
            ValueError: _description_
            APIException: _description_
            APIException: _description_

        Returns:
            dict: _description_
        """
        headers = {"Content-Type" : "application/json"}

        if self.token:
            headers["Authorization"] = f'XTM-Basic {self.token}'

        body = json.dumps(body).encode("utf-8")
        if method == ReqMethod.POST:
            result = requests.post(url, headers=headers, data=body, params=params, timeout=60)
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
