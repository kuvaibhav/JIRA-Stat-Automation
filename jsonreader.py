
import requests
from requests.auth import HTTPBasicAuth
import json
from new_calculate_jira import CalculateJIRAStats,PopulateStats
import collections

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
        import re
        pattern = re.compile("UC\d",re.IGNORECASE)
        for i in range(len(excel_row_array)):
            if pattern.match(excel_row_array[i]):
                track_application_occurrence = True
                application = excel_row_array[i]
                if track_application_occurrence:
                    return application
        # if not track_application_occurrence:
        #     raise Exception('Jira Ticket {} does not have application name against it.'.
        #                     format(excel_row_array[1]))
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
    def report(jira_issue_list):
        jira_issues = []
        jira_enhancements = []
        for object in jira_issue_list:
            if object['isEnhancement']:
                jira_enhancements.append(object)
            else:
                jira_issues.append(object)

        all_jira = []
        all_jira.extend(jira_issues)
        all_jira.extend(jira_enhancements)
        print("Total Issue/Enhancements: {}".format(len(jira_issues)+len(jira_enhancements)))
        print(collections.Counter([jira['priority'] for jira in all_jira]))
        print("Issues : {}".format(len(jira_issues)))
        print("Enhancements : {}".format(len(jira_enhancements)))
        populate_stat_issues = PopulateStats('Issues', jira_issues)
        populate_stat_issues.print_report()
        populate_stat_enhancements = PopulateStats('Enhancements', jira_enhancements)
        populate_stat_enhancements.print_report()



    @staticmethod
    def fetch_jira_tickets():
        url = "http://ilscha03-jira-02:8080/rest/api/2/search"

        auth = HTTPBasicAuth("vlanid", "password")

        headers = {
           "Accept": "application/json"
        }

        query = {
           # "jql": "project = 'SA3 Deloitte' AND labels in (UAT-issue, PROD-Issue)  and (resolutiondate  >=  startOfMonth()  or resolutiondate is EMPTY )",
           "jql": "project = 'SA3 Deloitte' AND labels in (UAT-issue, PROD-Issue) AND resolutiondate is EMPTY AND status not in(UAT,Done)",
           "maxResults": 1000,

        }

        response = requests.request(
           "GET",
           url,
           headers=headers,
           params=query,
           auth=auth
        )
        print(response.status_code)
        # uat_issues = json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
        uat_issues = json.loads(response.text)
        # print(uat_issues)


        issues_dict = {}
        for issue in uat_issues['issues']:
            issues_dict[issue['key']] = {'labels':issue['fields']['labels'],'status':issue['fields']['status']['name']}

        jira_issue_list = []
        for id,data in issues_dict.items():
            labels = data['labels']
            status = data['status']

            jira_issue_object = {'jira_id': id, 'assigned_to': 'Deloitte',
                             'priority': ReadJiraIssues.calculate_priority(labels),
                             'application': ReadJiraIssues.calculate_application(labels),
                             'isEnhancement': ReadJiraIssues.find_if_enhancement(labels), 'status': status}
            jira_issue_list.append(jira_issue_object)

        CalculateJIRAStats.report(jira_issue_list)


if __name__ == '__main__':

    rd = ReadJiraIssues()
    rd.fetch_jira_tickets()