
import requests
from requests.auth import HTTPBasicAuth
import json


class ReadJiraIssues:

    @staticmethod
    def calculate_priority(excel_row_array):
        track_priority_occurrence = False
        priority = 'NA'
        for i in range(len(excel_row_array)):
            if excel_row_array[i] == 'P1' or excel_row_array[i] == 'P2' or excel_row_array[i] == 'P3':
                track_priority_occurrence = True
                priority = excel_row_array[i]
                if track_priority_occurrence:
                    return priority
        if not track_priority_occurrence:
            raise Exception('Jira Ticket {} does not have any Priority assigned. For correct report priority'
                            'needs to be assigned'.format(excel_row_array[1]))
        return priority

    @staticmethod
    def calculate_application(excel_row_array):
        track_application_occurrence = False
        application = 'NA'
        for i in range(len(excel_row_array)):
            if excel_row_array[i] in ['UC1', 'UC2', 'UC3', 'UC4', 'UC5', 'UC6', 'uc1', 'uc2', 'uc3',
                                      'uc4', 'uc5', 'uc6']:
                track_application_occurrence = True
                application = excel_row_array[i]
                if track_application_occurrence:
                    return application
        if not track_application_occurrence:
            raise Exception('Jira Ticket {} does not have application name against it.'.
                            format(excel_row_array[1]))
        return application

    @staticmethod
    def find_if_enhancement(excel_row_array):
        """
            To find an enhancement we need to look at below occurrence:
            'Issue_Type_Issue' return False
            'Issue_Type_Enhancements' return True
            'Issue_Type_Additional_Requirements' return True
             If nothing is found look for
             Return as Issue i.e. False
        """
        for i in range(len(excel_row_array)):
            if excel_row_array[i] in ['Issue_Type_Enhancements', 'Issue_Type_Additional_Requirements']:
                return True
            elif excel_row_array[i] == 'Issue_Type_Issue':
                return False
        return False


    @staticmethod
    def fetch_jira_tickets():
        # url = "/rest/api/3/search"
        url = "http://ilscha03-jira-02:8080/rest/api/2/search"

        auth = HTTPBasicAuth("sball005", "Nov@2019")

        headers = {
           "Accept": "application/json"
        }

        query = {
           "jql": "project = DEL  AND labels in (UAT-issue, PROD-Issue)  and (resolutiondate  >=  startOfMonth()  or resolutiondate is EMPTY )",
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
        # with open('uat_jira.json','w') as fp:
        #     fp.write(json.dumps(issues_dict))
        # label_list = []
        # for list_item in issues_dict.values():
        #     # print(list_item)
        #     label_list.extend(list_item)
         for id,labels in issues_dict.items():
            jira_issue_object = {'jira_id': id, 'assigned_to': 'Deloitte',
                                 'priority': ReadJiraIssues.calculate_priority(labels),
                                 'application': ReadJiraIssues.calculate_application(labels),
                                 'isEnhancement': ReadJiraIssues.find_if_enhancement(labels), 'status': 'Open'}

        '''
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
        print("LEN")
        print(len(issues_dict))
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

        # print(len(set(p1_list)))
        # print(label_list)
        # # 
        '''
        # print(uc4_list)

if __name__ == '__main__':

    rd = ReadJiraIssues()
    rd.fetch_jira_tickets()