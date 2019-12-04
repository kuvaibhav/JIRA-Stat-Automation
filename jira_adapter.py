from .jsonreader import ReadJiraIssues # Adaptee

from .jira_dump_reader import  CalculateJIRAStats # Target


class JIRAAdapter(ReadJiraIssues):

    def __init__(self, calculate_jira_status:CalculateJIRAStats):
        self.calculate_jira_status = calculate_jira_status


