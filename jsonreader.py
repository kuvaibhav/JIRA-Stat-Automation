
import requests
from requests.auth import HTTPBasicAuth
import json


class ReadJiraIssues:

    @staticmethod
    def fetch_jira_tickets(self):
        # url = "/rest/api/3/search"
        url = "http://ilscha03-jira-02:8080/rest/api/2/search"

        auth = HTTPBasicAuth("sball005", "Oct@2019")

        headers = {
           "Accept": "application/json"
        }

        query = {
           "jql": "project = DEL  AND labels in (UAT-issue, PROD-Issue)",
           "maxResults": 1000,

        }

        response = requests.request(
           "GET",
           url,
           headers=headers,
           params=query,
           auth=auth
        )
        # uat_issues = json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
        uat_issues = json.loads(response.text)
        # print(uat_issues)

        issues_dict = {}
        # with open('jira.json', encoding="utf-8") as fp:
        #     uat_issues = json.load(fp)
        for issue in uat_issues['issues']:
            issues_dict[issue['key']] = issue['fields']['labels']
        label_list = []
        for list_item in issues_dict.values():
            # print(list_item)
            label_list.extend(list_item)


        p1_list = []
        p2_list = []
        p3_list = []
        uc1_list = []
        uc2_list = []
        uc3_list = []
        uc4_list = []
        uc5_list = []
        uc6_list = []

        type_issue = []
        type_enhancement = []
        label_list = set(label_list)
        # {'Issue_Type_Enhancements', 'FileMgmt', 'Issue_Type_Issue', 'Report', 'UC4', 'UC3', 'UC5', 'UI', 'TDS', 'UC6',
        # 'ManualOverride', 'zprojdAlign', 'pipelines', 'PROD-Issue', 'inventory', 'UAT-issue', 'zprojAlign',
        # 'filters', 'uc5', 'P2', 'P1', 'P3'}
        for key, value in issues_dict.items():
            for label in label_list:

                if 'P1' in value:
                    p1_list.append(key)

                elif 'P2' in value:
                    p2_list.append(key)

                elif 'P3' in value:
                    p3_list.append(key)

                if 'Issue_Type_Issue' in value:
                    type_issue.append(key)

                elif 'Issue_Type_Enhancements' in value:
                    type_enhancement.append(key)

                if 'UC1' in value:
                    uc1_list.append(key)

                elif 'UC2' in value:
                    uc2_list.append(key)

                elif 'UC3' in value:
                    uc3_list.append(key)

                elif 'UC4' in value:
                    uc4_list.append(key)

                elif 'UC5' in value:
                    uc5_list.append(key)

                elif 'UC6' in value:
                    uc6_list.append(key)

        print(len(set(p1_list)))
        print(label_list)
        # '''
        print(uc4_list)
